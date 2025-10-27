// Gestione conversazioni nel localStorage

const STORAGE_KEY = 'hal9000_conversations';
const CURRENT_CONVERSATION_KEY = 'hal9000_current_conversation';

export const conversationStorage = {
  // Ottieni tutte le conversazioni
  getAll() {
    try {
      const data = localStorage.getItem(STORAGE_KEY);
      return data ? JSON.parse(data) : [];
    } catch (error) {
      console.error('Error loading conversations:', error);
      return [];
    }
  },

  // Ottieni una conversazione specifica
  get(id) {
    const conversations = this.getAll();
    return conversations.find(conv => conv.id === id);
  },

  // Salva una conversazione
  save(conversation) {
    try {
      const conversations = this.getAll();
      const index = conversations.findIndex(conv => conv.id === conversation.id);
      
      if (index >= 0) {
        // Aggiorna esistente
        conversations[index] = {
          ...conversation,
          updatedAt: new Date().toISOString()
        };
      } else {
        // Crea nuova
        conversations.push({
          ...conversation,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        });
      }
      
      localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
      return true;
    } catch (error) {
      console.error('Error saving conversation:', error);
      return false;
    }
  },

  // Elimina una conversazione
  delete(id) {
    try {
      const conversations = this.getAll();
      const filtered = conversations.filter(conv => conv.id !== id);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));
      return true;
    } catch (error) {
      console.error('Error deleting conversation:', error);
      return false;
    }
  },

  // Crea una nuova conversazione
  create(title, language = 'Python', uiLang = 'en') {
    return {
      id: Date.now().toString(),
      title: title || 'New Conversation',
      language,
      uiLang,
      messages: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
  },

  // Ottieni ID conversazione corrente
  getCurrentId() {
    return localStorage.getItem(CURRENT_CONVERSATION_KEY);
  },

  // Imposta conversazione corrente
  setCurrentId(id) {
    localStorage.setItem(CURRENT_CONVERSATION_KEY, id);
  },

  // Genera titolo automatico dai primi messaggi
  generateTitle(messages) {
    if (messages.length === 0) return 'New Conversation';
    
    const userMessage = messages.find(m => m.role === 'user');
    if (userMessage) {
      const title = userMessage.content.substring(0, 50);
      return title.length < userMessage.content.length ? title + '...' : title;
    }
    
    return 'New Conversation';
  },

  // Esporta conversazione come JSON
  export(id) {
    const conversation = this.get(id);
    if (!conversation) return null;
    
    const dataStr = JSON.stringify(conversation, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `hal9000_${conversation.title.replace(/[^a-z0-9]/gi, '_')}_${conversation.id}.json`;
    link.click();
    
    URL.revokeObjectURL(url);
    return true;
  },

  // Importa conversazione da JSON
  import(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      
      reader.onload = (e) => {
        try {
          const conversation = JSON.parse(e.target.result);
          
          // Valida struttura
          if (!conversation.id || !conversation.messages) {
            reject(new Error('Invalid conversation format'));
            return;
          }
          
          // Genera nuovo ID per evitare conflitti
          conversation.id = Date.now().toString();
          conversation.importedAt = new Date().toISOString();
          
          this.save(conversation);
          resolve(conversation);
        } catch (error) {
          reject(error);
        }
      };
      
      reader.onerror = () => reject(new Error('Failed to read file'));
      reader.readAsText(file);
    });
  }
};
