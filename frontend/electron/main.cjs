const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let flaskProcess;

// Start Flask backend
function startFlaskServer() {
  const pythonPath = process.platform === 'win32' ? 'python' : 'python3';
  const appPath = path.join(__dirname, '..', '..', 'app.py');
  
  flaskProcess = spawn(pythonPath, [appPath], {
    cwd: path.join(__dirname, '..', '..')
  });

  flaskProcess.stdout.on('data', (data) => {
    console.log(`Flask: ${data}`);
  });

  flaskProcess.stderr.on('data', (data) => {
    console.error(`Flask Error: ${data}`);
  });

  // Wait for Flask to start
  return new Promise((resolve) => {
    setTimeout(resolve, 2000);
  });
}

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

// Handle IPC from renderer
ipcMain.handle('send-query', async (event, data) => {
  try {
    const fetch = (await import('node-fetch')).default;
    const response = await fetch('http://127.0.0.1:5001/api/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });
    
    return await response.json();
  } catch (error) {
    console.error('Query error:', error);
    return {
      response: "I'm afraid I can't do that. An error occurred processing your request.",
      error: true
    };
  }
});

// Handle streaming query
ipcMain.handle('send-query-stream', async (event, data) => {
  try {
    const fetch = (await import('node-fetch')).default;
    const response = await fetch('http://127.0.0.1:5001/api/query/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });
    
    const reader = response.body;
    let buffer = '';
    
    reader.on('data', (chunk) => {
      buffer += chunk.toString();
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            event.sender.send('query-stream-chunk', data);
          } catch (e) {
            console.error('Parse error:', e);
          }
        }
      }
    });
    
    return new Promise((resolve, reject) => {
      reader.on('end', () => resolve({ done: true }));
      reader.on('error', reject);
    });
    
  } catch (error) {
    console.error('Streaming query error:', error);
    return {
      error: true,
      message: error.message
    };
  }
});

app.whenReady().then(async () => {
  await startFlaskServer();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (flaskProcess) {
    flaskProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('quit', () => {
  if (flaskProcess) {
    flaskProcess.kill();
  }
});
