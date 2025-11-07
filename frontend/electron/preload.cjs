const { contextBridge, ipcRenderer } = require('electron');

console.log('Preload script loaded');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  sendQuery: (data) => {
    console.log('Sending query via IPC:', data);
    return ipcRenderer.invoke('send-query', data);
  },
  onQueryChunk: (callback) => {
    // Rimuovi listener precedenti per evitare duplicati
    ipcRenderer.removeAllListeners('query-chunk');
    ipcRenderer.on('query-chunk', (event, chunk) => callback(chunk));
  },
  sendQueryStream: (data, onChunk, onComplete, onError) => {
    console.log('Sending streaming query via IPC:', data);
    ipcRenderer.invoke('send-query-stream', data).then(onComplete).catch(onError);
    
    // Listen for streaming chunks
    const handler = (event, chunk) => onChunk(chunk);
    ipcRenderer.on('query-stream-chunk', handler);
    
    // Cleanup listener
    return () => ipcRenderer.removeListener('query-stream-chunk', handler);
  }
});

console.log('electronAPI exposed to window');
