/**
 * Script per download automatico documentazioni durante installazione
 * Integrato nell'installer di CAP 9000
 */

const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

class DocsInstaller {
    constructor(installDir) {
        this.installDir = installDir || process.cwd();
        this.docsDir = path.join(this.installDir, 'local_docs');
        
        // Dimensioni approssimative per linguaggio
        this.docsSizes = {
            python: 8,    // MB
            java: 6,
            javascript: 7,
            cpp: 9,
            go: 5,
            total: 35     // MB totali
        };
    }

    getRequiredSpace() {
        return this.docsSizes.total;
    }

    async downloadDocs(progressCallback) {
        return new Promise((resolve, reject) => {
            if (progressCallback) {
                progressCallback({ 
                    stage: 'docs-download', 
                    progress: 0, 
                    message: 'Downloading official documentation...' 
                });
            }

            // Verifica se Python è disponibile
            exec('python3 --version', (error) => {
                if (error) {
                    // Prova con python
                    exec('python --version', (error2) => {
                        if (error2) {
                            reject(new Error('Python not found. Please install Python 3.'));
                            return;
                        }
                        this.runDownloadScript('python', progressCallback, resolve, reject);
                    });
                } else {
                    this.runDownloadScript('python3', progressCallback, resolve, reject);
                }
            });
        });
    }

    runDownloadScript(pythonCmd, progressCallback, resolve, reject) {
        const scriptPath = path.join(this.installDir, 'download_docs.py');
        
        if (!fs.existsSync(scriptPath)) {
            reject(new Error('download_docs.py not found'));
            return;
        }

        const process = exec(`${pythonCmd} "${scriptPath}"`, {
            cwd: this.installDir
        });

        let currentLang = '';
        let completedLangs = 0;
        const totalLangs = 5; // python, java, js, cpp, go

        process.stdout.on('data', (data) => {
            const output = data.toString();
            
            // Parse output per progress
            if (output.includes('Downloading')) {
                const match = output.match(/Downloading (\w+) documentation/);
                if (match) {
                    currentLang = match[1];
                }
            }
            
            if (output.includes('✓') && output.includes('docs downloaded')) {
                completedLangs++;
                const progress = (completedLangs / totalLangs) * 100;
                
                if (progressCallback) {
                    progressCallback({
                        stage: 'docs-download',
                        progress: progress,
                        message: `Downloaded ${currentLang} documentation (${completedLangs}/${totalLangs})`
                    });
                }
            }
        });

        process.stderr.on('data', (data) => {
            console.error('Docs download error:', data.toString());
        });

        process.on('close', (code) => {
            if (code === 0) {
                if (progressCallback) {
                    progressCallback({
                        stage: 'docs-download',
                        progress: 100,
                        message: 'Documentation downloaded successfully'
                    });
                }
                resolve(true);
            } else {
                reject(new Error(`Documentation download failed with code ${code}`));
            }
        });
    }

    async verifyDocs() {
        const indexPath = path.join(this.docsDir, 'index.json');
        
        if (!fs.existsSync(indexPath)) {
            return false;
        }

        try {
            const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
            return index.languages && Object.keys(index.languages).length >= 5;
        } catch (error) {
            return false;
        }
    }
}

module.exports = DocsInstaller;

// CLI usage
if (require.main === module) {
    const installer = new DocsInstaller();
    
    console.log('CAP 9000 - Documentation Setup');
    console.log('==============================\n');
    console.log(`Required disk space: ${installer.getRequiredSpace()} MB\n`);
    
    installer.downloadDocs((status) => {
        const bar = '█'.repeat(Math.floor(status.progress / 5)) + '░'.repeat(20 - Math.floor(status.progress / 5));
        process.stdout.write(`\r[${bar}] ${status.progress.toFixed(0)}% - ${status.message}`);
    }).then(() => {
        console.log('\n\n✓ Documentation setup completed!');
        return installer.verifyDocs();
    }).then((verified) => {
        if (verified) {
            console.log('✓ Documentation verified successfully');
        } else {
            console.log('⚠ Documentation verification failed');
        }
        process.exit(0);
    }).catch((error) => {
        console.error('\n\n✗ Documentation setup failed:', error.message);
        console.log('\nNote: CAP 9000 will work with built-in fallback documentation.');
        process.exit(1);
    });
}
