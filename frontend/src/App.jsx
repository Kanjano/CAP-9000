import { useState, useEffect, useRef } from 'react'
import { Send, Circle, Menu } from 'lucide-react'
import { translations, languageNames } from './i18n/translations'
import MessageContent from './components/MessageContent'
import ConversationSidebar from './components/ConversationSidebar'
import SplashScreen from './components/SplashScreen'
import { conversationStorage } from './utils/conversationStorage'

function App() {
  const [isLoading, setIsLoading] = useState(true)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [language, setLanguage] = useState('Python')
  const [isTyping, setIsTyping] = useState(false)
  const [languages, setLanguages] = useState(['Python', 'Java', 'JavaScript', 'C', 'C++', 'Go'])
  const [conversations, setConversations] = useState([])
  const [currentConversationId, setCurrentConversationId] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const messagesEndRef = useRef(null)

  // Lingua rilevata automaticamente dal backend
  const t = translations['en']  // Fallback, la lingua vera viene rilevata dal backend

  // Load conversations on mount - DOPO splash screen
  useEffect(() => {
    if (!isLoading) {
      console.log('App ready. Loading conversations...');
      const savedConversations = conversationStorage.getAll();
      console.log('Found saved conversations:', savedConversations.length);
      setConversations(savedConversations);
      
      const currentId = conversationStorage.getCurrentId();
      if (currentId && savedConversations.find(c => c.id === currentId)) {
        console.log('Loading conversation:', currentId);
        loadConversation(currentId);
      } else {
        console.log('Creating new conversation');
        createNewConversation();
      }
    }
  }, [isLoading]);  // Trigger quando splash finisce

  // Rimosso: lingua rilevata automaticamente dal backend

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Auto-save conversation when messages change
  useEffect(() => {
    if (currentConversationId && messages.length > 0) {
      saveCurrentConversation();
    }
  }, [messages]);

  const createNewConversation = () => {
    const newConv = conversationStorage.create('New Conversation', language, 'en');  // Default en, lingua rilevata automaticamente
    newConv.messages = [{ role: 'assistant', content: t.greeting }];
    conversationStorage.save(newConv);
    conversationStorage.setCurrentId(newConv.id);
    
    setCurrentConversationId(newConv.id);
    setMessages(newConv.messages);
    setLanguage(newConv.language);
    // uiLang rimosso: rilevato automaticamente
    setConversations(conversationStorage.getAll());
    setSidebarOpen(false);
  };

  const loadConversation = (id) => {
    const conv = conversationStorage.get(id);
    if (conv) {
      setCurrentConversationId(conv.id);
      setMessages(conv.messages);
      setLanguage(conv.language);
      // uiLang rimosso: rilevato automaticamente
      conversationStorage.setCurrentId(conv.id);
      setSidebarOpen(false);
    }
  };

  const saveCurrentConversation = () => {
    if (!currentConversationId) return;
    
    const conv = conversationStorage.get(currentConversationId);
    if (conv) {
      conv.messages = messages;
      conv.language = language;
      conv.uiLang = 'en';  // Default, lingua rilevata automaticamente
      
      // Auto-generate title from first user message
      if (conv.title === 'New Conversation' && messages.length >= 2) {
        conv.title = conversationStorage.generateTitle(messages);
      }
      
      conversationStorage.save(conv);
      setConversations(conversationStorage.getAll());
    }
  };

  const deleteConversation = (id) => {
    conversationStorage.delete(id);
    const remaining = conversationStorage.getAll();
    setConversations(remaining);
    
    if (id === currentConversationId) {
      if (remaining.length > 0) {
        loadConversation(remaining[0].id);
      } else {
        createNewConversation();
      }
    }
  };

  const exportConversation = (id) => {
    conversationStorage.export(id);
  };

  const importConversation = async (file) => {
    try {
      const conv = await conversationStorage.import(file);
      setConversations(conversationStorage.getAll());
      loadConversation(conv.id);
    } catch (error) {
      console.error('Import failed:', error);
      alert('Failed to import conversation. Please check the file format.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    const currentQuery = input
    setInput('')
    setIsTyping(true)

    try {
      // Usa streaming per risposte progressive
      if (window.electronAPI && window.electronAPI.sendQueryStream) {
        console.log('Using streaming query');
        
        // Aggiungi messaggio vuoto che verrà riempito progressivamente
        const messageIndex = messages.length + 1;
        setMessages(prev => [...prev, { role: 'assistant', content: '' }]);
        setIsTyping(false); // Non mostra typing indicator, mostra direttamente il testo
        
        let accumulatedContent = '';
        
        const cleanup = window.electronAPI.sendQueryStream(
          {
            query: currentQuery,
            language: language
            // uiLanguage rimosso: rilevato automaticamente dal backend
          },
          // onChunk - riceve ogni pezzo di testo
          (chunk) => {
            if (chunk.content && !chunk.done) {
              accumulatedContent += chunk.content;
              setMessages(prev => {
                const newMessages = [...prev];
                newMessages[messageIndex] = {
                  role: 'assistant',
                  content: accumulatedContent
                };
                return newMessages;
              });
            }
          },
          // onComplete
          () => {
            console.log('Streaming complete');
            cleanup && cleanup();
          },
          // onError
          (error) => {
            console.error('Streaming error:', error);
            setMessages(prev => {
              const newMessages = [...prev];
              newMessages[messageIndex] = {
                role: 'assistant',
                content: t.connectionError
              };
              return newMessages;
            });
            cleanup && cleanup();
          }
        );
      } else {
        // Fallback senza streaming
        console.log('Using non-streaming query');
        const data = await window.electronAPI.sendQuery({
          query: currentQuery,
          language: language
          // uiLanguage rimosso: rilevato automaticamente dal backend
        });
        
        setTimeout(() => {
          setIsTyping(false);
          setMessages(prev => [...prev, { 
            role: 'assistant', 
            content: data.response || t.processingError
          }]);
        }, 500);
      }
    } catch (error) {
      console.error('Query error:', error);
      setTimeout(() => {
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: t.connectionError
        }]);
        setIsTyping(false);
      }, 500);
    }
  }

  // Mostra splash screen durante il caricamento
  if (isLoading) {
    return <SplashScreen onComplete={() => setIsLoading(false)} />;
  }

  return (
    <div className="min-h-screen bg-hal-bg flex">
      {/* Conversation Sidebar */}
      <ConversationSidebar
        conversations={conversations}
        currentId={currentConversationId}
        onSelect={loadConversation}
        onNew={createNewConversation}
        onDelete={deleteConversation}
        onExport={exportConversation}
        onImport={importConversation}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        translations={t}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
      {/* Header - Fixed */}
      <div className="flex-shrink-0 bg-hal-panel border-b border-red-900 p-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          {/* Left: Menu + Title */}
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="lg:hidden text-red-500 hover:text-red-400 p-2"
            >
              <Menu className="w-5 h-5" />
            </button>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-radial from-hal-red to-red-900 hal-eye-glow flex items-center justify-center">
                <Circle className="w-5 h-5 text-black fill-black opacity-30" />
              </div>
              <div>
                <h1 className="text-xl font-bold hal-glow tracking-wider">CAP 9000</h1>
                <p className="text-red-500 text-xs opacity-70">{t.systemName}</p>
              </div>
            </div>
          </div>

          {/* Right: Programming Language Selector Only */}
          <div className="flex items-center gap-2">
            <span className="text-red-500 text-xs opacity-70">Language:</span>
            <select 
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-black border border-red-900 text-red-400 px-3 py-1.5 rounded text-sm focus:outline-none focus:border-hal-red"
            >
              {languages.map(lang => (
                <option key={lang} value={lang}>{lang}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Chat Container - Scrollable */}
      <div className="flex-1 overflow-hidden flex flex-col max-w-4xl mx-auto w-full">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto">
          {console.log('Rendering messages, count:', messages.length)}
          {messages.map((message, index) => {
            console.log(`Rendering message ${index}:`, message.role, message.content.substring(0, 50));
            return (
              <div
                key={index}
                className={`w-full ${
                  message.role === 'user' 
                    ? 'bg-transparent' 
                    : 'bg-[#2f2f2f]/40'
                }`}
              >
                <div className="max-w-3xl mx-auto px-6 py-8">
                  <div className="flex gap-6">
                    {/* Avatar */}
                    <div className="flex-shrink-0">
                      {message.role === 'user' ? (
                        <div className="w-8 h-8 rounded-sm bg-red-900/80 flex items-center justify-center text-white text-sm font-bold">
                          U
                        </div>
                      ) : (
                        <div className="w-8 h-8 rounded-sm bg-gradient-radial from-hal-red to-red-900 hal-eye-glow flex items-center justify-center">
                          <Circle className="w-4 h-4 text-black fill-black opacity-30" />
                        </div>
                      )}
                    </div>
                    
                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="text-xs text-red-400/80 mb-3 font-medium tracking-wide">
                        {message.role === 'user' ? t.userLabel : t.halLabel}
                      </div>
                      <div className="text-gray-100 max-w-none">
                        <MessageContent content={message.content} />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
          
          {isTyping && (
            <div className="w-full bg-[#2f2f2f]/40">
              <div className="max-w-3xl mx-auto px-6 py-8">
                <div className="flex gap-6">
                  <div className="w-8 h-8 rounded-sm bg-gradient-radial from-hal-red to-red-900 hal-eye-glow flex items-center justify-center">
                    <Circle className="w-4 h-4 text-black fill-black opacity-30" />
                  </div>
                  <div className="flex-1">
                    <div className="text-xs text-red-400/80 mb-3 font-medium tracking-wide">{t.halLabel}</div>
                    <div className="flex gap-1">
                      <span className="w-2 h-2 bg-red-500 rounded-full animate-bounce"></span>
                      <span className="w-2 h-2 bg-red-500 rounded-full animate-bounce delay-100"></span>
                      <span className="w-2 h-2 bg-red-500 rounded-full animate-bounce delay-200"></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Form */}
        <div className="flex-shrink-0 border-t border-red-900 p-4 bg-hal-panel">
          <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
            <div className="flex gap-3">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={t.inputPlaceholder}
                className="flex-1 bg-black border border-gray-700 text-gray-200 px-4 py-3 rounded-lg focus:outline-none focus:border-red-700 transition-colors placeholder-gray-600"
              />
              <button
                type="submit"
                disabled={!input.trim() || isTyping}
                className="bg-red-800 hover:bg-red-700 disabled:bg-gray-800 disabled:opacity-50 text-white px-6 py-3 rounded-lg transition-colors flex items-center gap-2"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Footer */}
      <div className="flex-shrink-0 text-center text-red-900 text-xs py-2 bg-hal-panel border-t border-red-900">
        <p>{t.footer}</p>
      </div>
      </div>
    </div>
  )
}

export default App
