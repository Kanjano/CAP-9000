/**
 * Python Bridge per comunicazione diretta Electron <-> Python
 * Elimina overhead HTTP Flask
 */

const { spawn } = require('child_process');
const path = require('path');

class PythonBridge {
  constructor() {
    this.pythonPath = process.platform === 'win32' ? 'python' : 'python3';
    this.scriptPath = path.join(__dirname, '..', '..', 'python_bridge.py');
    this.process = null;
    this.responseHandlers = {};
    this.isReady = false;
    this.buffer = '';
  }

  async start() {
    return new Promise((resolve, reject) => {
      console.log('Starting Python Bridge...');
      console.log('Script path:', this.scriptPath);
      
      this.process = spawn(this.pythonPath, [this.scriptPath], {
        cwd: path.join(__dirname, '..', '..'),
        stdio: ['pipe', 'pipe', 'pipe']
      });

      // Handle stdout (JSON responses)
      this.process.stdout.on('data', (data) => {
        this.buffer += data.toString();
        const lines = this.buffer.split('\n');
        this.buffer = lines.pop() || '';
        
        for (const line of lines) {
          if (!line.trim()) continue;
          
          try {
            const response = JSON.parse(line);
            
            // Check for ready signal
            if (response.status === 'ready') {
              console.log('Python Bridge ready');
              this.isReady = true;
              resolve();
              continue;
            }
            
            // Handle response
            this.handleResponse(response);
          } catch (e) {
            console.error('Parse error:', e);
            console.error('Line:', line);
          }
        }
      });

      // Handle stderr (logs)
      this.process.stderr.on('data', (data) => {
        console.log(`Python: ${data.toString().trim()}`);
      });

      // Handle process exit
      this.process.on('close', (code) => {
        console.log(`Python Bridge exited with code ${code}`);
        this.isReady = false;
      });

      this.process.on('error', (err) => {
        console.error('Python Bridge error:', err);
        reject(err);
      });

      // Timeout if not ready in 10s
      setTimeout(() => {
        if (!this.isReady) {
          reject(new Error('Python Bridge timeout'));
        }
      }, 10000);
    });
  }

  async query(data) {
    if (!this.isReady) {
      throw new Error('Python Bridge not ready');
    }

    return new Promise((resolve, reject) => {
      const requestId = Date.now() + Math.random();
      
      this.responseHandlers[requestId] = {
        resolve,
        reject,
        timeout: setTimeout(() => {
          if (this.responseHandlers[requestId]) {
            delete this.responseHandlers[requestId];
            reject(new Error('Query timeout (120s)'));
          }
        }, 120000) // 120s timeout
      };

      const request = {
        id: requestId,
        type: 'query',
        data: data
      };

      try {
        this.process.stdin.write(JSON.stringify(request) + '\n');
      } catch (e) {
        clearTimeout(this.responseHandlers[requestId].timeout);
        delete this.responseHandlers[requestId];
        reject(e);
      }
    });
  }

  async getStats() {
    if (!this.isReady) {
      throw new Error('Python Bridge not ready');
    }

    return new Promise((resolve, reject) => {
      const requestId = Date.now() + Math.random();
      
      this.responseHandlers[requestId] = {
        resolve,
        reject,
        timeout: setTimeout(() => {
          if (this.responseHandlers[requestId]) {
            delete this.responseHandlers[requestId];
            reject(new Error('Stats timeout'));
          }
        }, 5000)
      };

      const request = {
        id: requestId,
        type: 'stats',
        data: {}
      };

      try {
        this.process.stdin.write(JSON.stringify(request) + '\n');
      } catch (e) {
        clearTimeout(this.responseHandlers[requestId].timeout);
        delete this.responseHandlers[requestId];
        reject(e);
      }
    });
  }

  handleResponse(response) {
    const handler = this.responseHandlers[response.id];
    if (handler) {
      clearTimeout(handler.timeout);
      handler.resolve(response.data);
      delete this.responseHandlers[response.id];
    }
  }

  stop() {
    if (this.process) {
      // Send exit signal
      try {
        this.process.stdin.write(JSON.stringify({
          id: Date.now(),
          type: 'exit',
          data: {}
        }) + '\n');
      } catch (e) {
        console.error('Error sending exit signal:', e);
      }
      
      // Force kill after 2s
      setTimeout(() => {
        if (this.process) {
          this.process.kill();
        }
      }, 2000);
    }
  }
}

module.exports = PythonBridge;
