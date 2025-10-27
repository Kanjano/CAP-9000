import { useState, useEffect, useRef } from 'react'
import { Send, Circle, Globe, Menu } from 'lucide-react'
import { translations, languageNames } from './i18n/translations'
import MessageContent from './components/MessageContent'
import ConversationSidebar from './components/ConversationSidebar'
import { conversationStorage } from './utils/conversationStorage'

function App() {
  const [uiLang, setUiLang] = useState('en')
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [language, setLanguage] = useState('Python')
  const [isTyping, setIsTyping] = useState(false)
  const [languages, setLanguages] = useState(['Python', 'Java', 'JavaScript', 'C', 'C++', 'Go'])
  const [conversations, setConversations] = useState([])
  const [currentConversationId, setCurrentConversationId] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const messagesEndRef = useRef(null)

  const t = translations[uiLang]

  // Load conversations on mount
  useEffect(() => {
    console.log('App mounted. electronAPI available:', !!window.electronAPI);
    const savedConversations = conversationStorage.getAll();
    setConversations(savedConversations);
    
    const currentId = conversationStorage.getCurrentId();
    if (currentId && savedConversations.find(c => c.id === currentId)) {
      loadConversation(currentId);
    } else {
      // Create new conversation
      createNewConversation();
    }
  }, []);

  // Update greeting when UI language changes
  useEffect(() => {
    if (messages.length === 1 && messages[0].role === 'assistant') {
      setMessages([{ role: 'assistant', content: t.greeting }]);
    }
  }, [uiLang]);

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
    const newConv = conversationStorage.create('New Conversation', language, uiLang);
    newConv.messages = [{ role: 'assistant', content: t.greeting }];
    conversationStorage.save(newConv);
    conversationStorage.setCurrentId(newConv.id);
    
    setCurrentConversationId(newConv.id);
    setMessages(newConv.messages);
    setLanguage(newConv.language);
    setUiLang(newConv.uiLang);
    setConversations(conversationStorage.getAll());
    setSidebarOpen(false);
  };

  const loadConversation = (id) => {
    const conv = conversationStorage.get(id);
    if (conv) {
      setCurrentConversationId(conv.id);
      setMessages(conv.messages);
      setLanguage(conv.language);
      setUiLang(conv.uiLang);
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
      conv.uiLang = uiLang;
      
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
      // Use Electron IPC if available, otherwise fallback to fetch
      console.log('Checking electronAPI:', window.electronAPI);
      if (window.electronAPI) {
        console.log('Using Electron IPC');
        const data = await window.electronAPI.sendQuery({
          query: currentQuery,
          language: language,
          uiLanguage: uiLang
        })
        console.log('Received response:', data);
        console.log('Response content:', data.response);
        console.log('Response type:', typeof data.response);
        
        const responseContent = data.response || t.processingError;
        console.log('Adding message with content:', responseContent);
        
        setTimeout(() => {
          setIsTyping(false)
          setMessages(prev => {
            const newMessages = [...prev, { 
              role: 'assistant', 
              content: responseContent
            }];
            console.log('New messages array length:', newMessages.length);
            return newMessages;
          })
        }, 500)
      } else {
        console.log('Using fetch fallback');
        const response = await fetch('/api/query', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: currentQuery,
            language: language,
            uiLanguage: uiLang
          })
        })

        const data = await response.json()
        
        setTimeout(() => {
          setMessages(prev => [...prev, { 
            role: 'assistant', 
            content: data.response || t.processingError
          }])
          setIsTyping(false)
        }, 500)
      }
    } catch (error) {
      setTimeout(() => {
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: t.connectionError
        }])
        setIsTyping(false)
      }, 500)
    }
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

          {/* Right: Language Selectors */}
          <div className="flex items-center gap-4">
            {/* UI Language */}
            <div className="flex items-center gap-2">
              <Globe className="w-4 h-4 text-red-500" />
              <select 
                value={uiLang}
                onChange={(e) => setUiLang(e.target.value)}
                className="bg-black border border-red-900 text-red-400 px-2 py-1 rounded text-sm focus:outline-none focus:border-hal-red"
              >
                {Object.entries(languageNames).map(([code, name]) => (
                  <option key={code} value={code}>{name}</option>
                ))}
              </select>
            </div>

            {/* Programming Language */}
            <select 
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-black border border-red-900 text-red-400 px-3 py-1 rounded text-sm focus:outline-none focus:border-hal-red"
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
