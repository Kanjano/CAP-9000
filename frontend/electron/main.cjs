const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const PythonBridge = require('./python-bridge.cjs');

let mainWindow;
let pythonBridge;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    backgroundColor: '#000000',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.cjs'),
      // Disabilita funzionalità browser non necessarie
      webSecurity: true,
      allowRunningInsecureContent: false
    },
    icon: path.join(__dirname, 'icon.png'),
    title: 'CAP 9000 - Code Assistant',
    // Ottimizzazioni desktop
    show: false, // Non mostrare finestra finché non è pronta
    autoHideMenuBar: true // Nascondi menu bar di default
  });

  // Load the app (Desktop-only - no browser fallback)
  const indexPath = path.join(__dirname, '..', 'dist', 'index.html');
  console.log('Loading desktop app from:', indexPath);
  
  mainWindow.loadFile(indexPath).then(() => {
    console.log('Desktop app loaded successfully');
    mainWindow.show(); // Mostra finestra solo quando pronta
  }).catch((err) => {
    console.error('Failed to load desktop app:', err);
    app.quit();
  });
  
  // Open DevTools in development
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }

  // Log any console messages from renderer
  mainWindow.webContents.on('console-message', (event, level, message, line, sourceId) => {
    console.log(`Renderer console [${level}]:`, message);
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Handle IPC from renderer - Direct Python Bridge (no HTTP)
ipcMain.handle('send-query', async (event, data) => {
  try {
    return await pythonBridge.query(data);
  } catch (error) {
    console.error('Query error:', error);
    return {
      response: "I'm afraid I can't do that. An error occurred processing your request.",
      error: true,
      source: 'error'
    };
  }
});

// Handle stats request
ipcMain.handle('get-stats', async (event) => {
  try {
    return await pythonBridge.getStats();
  } catch (error) {
    console.error('Stats error:', error);
    return {
      error: true,
      message: error.message
    };
  }
});

app.whenReady().then(async () => {
  // Start Python Bridge instead of Flask
  pythonBridge = new PythonBridge();
  await pythonBridge.start();
  
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (pythonBridge) {
    pythonBridge.stop();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('quit', () => {
  if (pythonBridge) {
    pythonBridge.stop();
  }
});
