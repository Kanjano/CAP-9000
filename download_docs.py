#!/usr/bin/env python3
"""
Script per scaricare documentazioni ufficiali in locale
Eseguire una volta durante il setup per avere docs offline
"""

import os
import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path

class DocumentationDownloader:
    def __init__(self, docs_dir="local_docs"):
        self.docs_dir = Path(docs_dir)
        self.docs_dir.mkdir(exist_ok=True)
        
    def download_python_docs(self):
        """Scarica documentazione Python essenziale"""
        print("📚 Downloading Python documentation...")
        
        python_docs = {
            'tutorial': 'https://docs.python.org/3/tutorial/index.html',
            'library': 'https://docs.python.org/3/library/index.html',
            'reference': 'https://docs.python.org/3/reference/index.html',
            'pep8': 'https://peps.python.org/pep-0008/',
        }
        
        python_dir = self.docs_dir / "python"
        python_dir.mkdir(exist_ok=True)
        
        for name, url in python_docs.items():
            try:
                print(f"  → Downloading {name}...")
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    # Salva HTML
                    (python_dir / f"{name}.html").write_text(response.text, encoding='utf-8')
                    
                    # Estrai testo pulito
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = soup.get_text(separator='\n', strip=True)
                    (python_dir / f"{name}.txt").write_text(text, encoding='utf-8')
                    print(f"    ✓ Saved {name}")
                    time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"    ✗ Error downloading {name}: {e}")
        
        print("  ✓ Python docs downloaded\n")
    
    def download_java_docs(self):
        """Scarica documentazione Java essenziale"""
        print("📚 Downloading Java documentation...")
        
        java_docs = {
            'tutorial': 'https://docs.oracle.com/javase/tutorial/',
            'api': 'https://docs.oracle.com/en/java/javase/17/docs/api/index.html',
        }
        
        java_dir = self.docs_dir / "java"
        java_dir.mkdir(exist_ok=True)
        
        for name, url in java_docs.items():
            try:
                print(f"  → Downloading {name}...")
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    (java_dir / f"{name}.html").write_text(response.text, encoding='utf-8')
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = soup.get_text(separator='\n', strip=True)
                    (java_dir / f"{name}.txt").write_text(text, encoding='utf-8')
                    print(f"    ✓ Saved {name}")
                    time.sleep(1)
            except Exception as e:
                print(f"    ✗ Error downloading {name}: {e}")
        
        print("  ✓ Java docs downloaded\n")
    
    def download_javascript_docs(self):
        """Scarica documentazione JavaScript essenziale"""
        print("📚 Downloading JavaScript documentation...")
        
        js_docs = {
            'guide': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide',
            'reference': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference',
        }
        
        js_dir = self.docs_dir / "javascript"
        js_dir.mkdir(exist_ok=True)
        
        for name, url in js_docs.items():
            try:
                print(f"  → Downloading {name}...")
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    (js_dir / f"{name}.html").write_text(response.text, encoding='utf-8')
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = soup.get_text(separator='\n', strip=True)
                    (js_dir / f"{name}.txt").write_text(text, encoding='utf-8')
                    print(f"    ✓ Saved {name}")
                    time.sleep(1)
            except Exception as e:
                print(f"    ✗ Error downloading {name}: {e}")
        
        print("  ✓ JavaScript docs downloaded\n")
    
    def download_cpp_docs(self):
        """Scarica documentazione C++ essenziale"""
        print("📚 Downloading C++ documentation...")
        
        cpp_docs = {
            'language': 'https://en.cppreference.com/w/cpp/language',
            'container': 'https://en.cppreference.com/w/cpp/container',
            'algorithm': 'https://en.cppreference.com/w/cpp/algorithm',
        }
        
        cpp_dir = self.docs_dir / "cpp"
        cpp_dir.mkdir(exist_ok=True)
        
        for name, url in cpp_docs.items():
            try:
                print(f"  → Downloading {name}...")
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    (cpp_dir / f"{name}.html").write_text(response.text, encoding='utf-8')
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = soup.get_text(separator='\n', strip=True)
                    (cpp_dir / f"{name}.txt").write_text(text, encoding='utf-8')
                    print(f"    ✓ Saved {name}")
                    time.sleep(1)
            except Exception as e:
                print(f"    ✗ Error downloading {name}: {e}")
        
        print("  ✓ C++ docs downloaded\n")
    
    def download_go_docs(self):
        """Scarica documentazione Go essenziale"""
        print("📚 Downloading Go documentation...")
        
        go_docs = {
            'effective_go': 'https://go.dev/doc/effective_go',
            'tour': 'https://go.dev/tour/welcome/1',
        }
        
        go_dir = self.docs_dir / "go"
        go_dir.mkdir(exist_ok=True)
        
        for name, url in go_docs.items():
            try:
                print(f"  → Downloading {name}...")
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    (go_dir / f"{name}.html").write_text(response.text, encoding='utf-8')
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = soup.get_text(separator='\n', strip=True)
                    (go_dir / f"{name}.txt").write_text(text, encoding='utf-8')
                    print(f"    ✓ Saved {name}")
                    time.sleep(1)
            except Exception as e:
                print(f"    ✗ Error downloading {name}: {e}")
        
        print("  ✓ Go docs downloaded\n")
    
    def create_index(self):
        """Crea un indice delle documentazioni scaricate"""
        print("📋 Creating documentation index...")
        
        index = {
            'downloaded_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'languages': {}
        }
        
        for lang_dir in self.docs_dir.iterdir():
            if lang_dir.is_dir():
                lang_name = lang_dir.name
                files = [f.name for f in lang_dir.iterdir() if f.suffix in ['.txt', '.html']]
                index['languages'][lang_name] = {
                    'files': files,
                    'count': len(files)
                }
        
        index_file = self.docs_dir / "index.json"
        index_file.write_text(json.dumps(index, indent=2), encoding='utf-8')
        print(f"  ✓ Index created at {index_file}\n")
        
        return index
    
    def download_all(self):
        """Scarica tutte le documentazioni"""
        print("=" * 60)
        print("CAP 9000 - Documentation Downloader")
        print("=" * 60)
        print()
        
        try:
            self.download_python_docs()
            self.download_java_docs()
            self.download_javascript_docs()
            self.download_cpp_docs()
            self.download_go_docs()
            
            index = self.create_index()
            
            print("=" * 60)
            print("✓ Download completed!")
            print("=" * 60)
            print(f"\nDocumentation saved in: {self.docs_dir.absolute()}")
            print(f"Total languages: {len(index['languages'])}")
            for lang, info in index['languages'].items():
                print(f"  • {lang.upper()}: {info['count']} files")
            print("\n✓ You can now use CAP 9000 completely offline!")
            
        except Exception as e:
            print(f"\n✗ Error during download: {e}")
            print("Note: Some docs may still be available from hardcoded fallback")

if __name__ == "__main__":
    downloader = DocumentationDownloader()
    downloader.download_all()
