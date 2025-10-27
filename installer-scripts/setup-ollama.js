/**
 * Script per download e installazione automatica di Ollama
 * Eseguito durante l'installazione di CAP 9000
 */

const { exec } = require('child_process');
const https = require('https');
const fs = require('fs');
const path = require('path');
const os = require('os');

class OllamaInstaller {
    constructor() {
        this.platform = os.platform();
        this.arch = os.arch();
        this.tempDir = path.join(os.tmpdir(), 'cap9000-setup');
        
        // Dimensioni approssimative
        this.sizes = {
            ollama: {
                darwin: 500, // MB
                win32: 450,
                linux: 400
            },
            model: {
                'codellama': 3800, // MB (~3.8 GB)
                'codellama:7b': 3800,
                'codellama:13b': 7000,
                'qwen2.5-coder:7b': 4500
            }
        };
    }

    getRequiredSpace() {
        const ollamaSize = this.sizes.ollama[this.platform] || 500;
        const modelSize = this.sizes.model['codellama'] || 3800;
        const docsSize = 50; // MB per documentazioni
        const appSize = 200; // MB per CAP 9000
        
        return {
            ollama: ollamaSize,
            model: modelSize,
            docs: docsSize,
            app: appSize,
            total: ollamaSize + modelSize + docsSize + appSize
        };
    }

    async checkOllamaInstalled() {
        return new Promise((resolve) => {
            exec('ollama --version', (error) => {
                resolve(!error);
            });
        });
    }

    async downloadOllama(progressCallback) {
        if (!fs.existsSync(this.tempDir)) {
            fs.mkdirSync(this.tempDir, { recursive: true });
        }

        let downloadUrl;
        let filename;

        switch (this.platform) {
            case 'darwin':
                downloadUrl = 'https://ollama.ai/download/Ollama-darwin.zip';
                filename = 'Ollama-darwin.zip';
                break;
            case 'win32':
                downloadUrl = 'https://ollama.ai/download/OllamaSetup.exe';
                filename = 'OllamaSetup.exe';
                break;
            case 'linux':
                // Linux usa script di installazione
                return this.installOllamaLinux(progressCallback);
            default:
                throw new Error(`Platform ${this.platform} not supported`);
        }

        const filepath = path.join(this.tempDir, filename);

        return new Promise((resolve, reject) => {
            const file = fs.createWriteStream(filepath);
            
            https.get(downloadUrl, (response) => {
                const totalSize = parseInt(response.headers['content-length'], 10);
                let downloadedSize = 0;

                response.on('data', (chunk) => {
                    downloadedSize += chunk.length;
                    const progress = (downloadedSize / totalSize) * 100;
                    if (progressCallback) {
                        progressCallback({
                            stage: 'download',
                            progress: progress,
                            downloaded: downloadedSize,
                            total: totalSize
                        });
                    }
                });

                response.pipe(file);

                file.on('finish', () => {
                    file.close();
                    resolve(filepath);
                });
            }).on('error', (err) => {
                fs.unlink(filepath, () => {});
                reject(err);
            });
        });
    }

    async installOllamaLinux(progressCallback) {
        return new Promise((resolve, reject) => {
            if (progressCallback) {
                progressCallback({ stage: 'install', progress: 0 });
            }

            exec('curl -fsSL https://ollama.ai/install.sh | sh', (error, stdout, stderr) => {
                if (error) {
                    reject(error);
                    return;
                }
                
                if (progressCallback) {
                    progressCallback({ stage: 'install', progress: 100 });
                }
                
                resolve(true);
            });
        });
    }

    async installOllama(installerPath, progressCallback) {
        return new Promise((resolve, reject) => {
            if (progressCallback) {
                progressCallback({ stage: 'install', progress: 0 });
            }

            let command;
            
            switch (this.platform) {
                case 'darwin':
                    // macOS: Unzip e copia in /Applications
                    command = `unzip -q "${installerPath}" -d "${this.tempDir}" && cp -R "${this.tempDir}/Ollama.app" /Applications/`;
                    break;
                case 'win32':
                    // Windows: Esegui installer silenzioso
                    command = `"${installerPath}" /S`;
                    break;
                default:
                    reject(new Error('Platform not supported'));
                    return;
            }

            exec(command, (error, stdout, stderr) => {
                if (error) {
                    reject(error);
                    return;
                }
                
                if (progressCallback) {
                    progressCallback({ stage: 'install', progress: 100 });
                }
                
                resolve(true);
            });
        });
    }

    async startOllama() {
        return new Promise((resolve, reject) => {
            let command;
            
            switch (this.platform) {
                case 'darwin':
                    command = 'open -a Ollama';
                    break;
                case 'win32':
                    command = 'start ollama serve';
                    break;
                case 'linux':
                    command = 'systemctl start ollama';
                    break;
                default:
                    reject(new Error('Platform not supported'));
                    return;
            }

            exec(command, (error) => {
                if (error) {
                    reject(error);
                    return;
                }
                
                // Attendi che Ollama sia pronto
                setTimeout(() => resolve(true), 3000);
            });
        });
    }

    async downloadModel(modelName = 'codellama', progressCallback) {
        return new Promise((resolve, reject) => {
            const process = exec(`ollama pull ${modelName}`);
            
            let lastProgress = 0;
            
            process.stdout.on('data', (data) => {
                const output = data.toString();
                
                // Parse output per progress
                const match = output.match(/(\d+)%/);
                if (match) {
                    const progress = parseInt(match[1]);
                    if (progress !== lastProgress && progressCallback) {
                        lastProgress = progress;
                        progressCallback({
                            stage: 'model-download',
                            progress: progress,
                            model: modelName
                        });
                    }
                }
            });

            process.on('close', (code) => {
                if (code === 0) {
                    resolve(true);
                } else {
                    reject(new Error(`Model download failed with code ${code}`));
                }
            });
        });
    }

    async fullSetup(progressCallback) {
        try {
            // 1. Check se Ollama è già installato
            if (progressCallback) {
                progressCallback({ stage: 'check', progress: 0, message: 'Checking Ollama installation...' });
            }
            
            const isInstalled = await this.checkOllamaInstalled();
            
            if (!isInstalled) {
                // 2. Download Ollama
                if (progressCallback) {
                    progressCallback({ stage: 'download', progress: 0, message: 'Downloading Ollama...' });
                }
                
                const installerPath = await this.downloadOllama(progressCallback);
                
                // 3. Install Ollama
                if (progressCallback) {
                    progressCallback({ stage: 'install', progress: 0, message: 'Installing Ollama...' });
                }
                
                await this.installOllama(installerPath, progressCallback);
            }
            
            // 4. Start Ollama
            if (progressCallback) {
                progressCallback({ stage: 'start', progress: 0, message: 'Starting Ollama service...' });
            }
            
            await this.startOllama();
            
            // 5. Download model
            if (progressCallback) {
                progressCallback({ stage: 'model', progress: 0, message: 'Downloading CodeLlama model...' });
            }
            
            await this.downloadModel('codellama', progressCallback);
            
            // 6. Complete
            if (progressCallback) {
                progressCallback({ stage: 'complete', progress: 100, message: 'Setup completed!' });
            }
            
            return true;
            
        } catch (error) {
            if (progressCallback) {
                progressCallback({ stage: 'error', progress: 0, message: error.message });
            }
            throw error;
        }
    }
}

module.exports = OllamaInstaller;

// CLI usage
if (require.main === module) {
    const installer = new OllamaInstaller();
    
    console.log('CAP 9000 - Ollama Setup');
    console.log('======================\n');
    
    const space = installer.getRequiredSpace();
    console.log(`Required disk space:`);
    console.log(`  - Ollama: ${space.ollama} MB`);
    console.log(`  - CodeLlama Model: ${space.model} MB`);
    console.log(`  - Documentation: ${space.docs} MB`);
    console.log(`  - CAP 9000 App: ${space.app} MB`);
    console.log(`  - TOTAL: ${space.total} MB (~${(space.total / 1024).toFixed(1)} GB)\n`);
    
    installer.fullSetup((status) => {
        const bar = '█'.repeat(Math.floor(status.progress / 5)) + '░'.repeat(20 - Math.floor(status.progress / 5));
        process.stdout.write(`\r[${bar}] ${status.progress.toFixed(0)}% - ${status.message || status.stage}`);
    }).then(() => {
        console.log('\n\n✓ Setup completed successfully!');
        process.exit(0);
    }).catch((error) => {
        console.error('\n\n✗ Setup failed:', error.message);
        process.exit(1);
    });
}
