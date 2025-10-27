const { contextBridge, ipcRenderer } = require('electron');

console.log('Preload script loaded');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  sendQuery: (data) => {
    console.log('Sending query via IPC:', data);
    return ipcRenderer.invoke('send-query', data);
  }
});

console.log('electronAPI exposed to window');
