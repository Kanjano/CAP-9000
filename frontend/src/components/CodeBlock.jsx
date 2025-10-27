import { useState, useEffect } from 'react';
import { Copy, Check } from 'lucide-react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/cjs/styles/prism';

// Import specific language support for better highlighting
import { highlight, languages } from 'prismjs';
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-java';
import 'prismjs/components/prism-c';
import 'prismjs/components/prism-cpp';
import 'prismjs/components/prism-go';
import 'prismjs/components/prism-bash';
import 'prismjs/components/prism-json';

export default function CodeBlock({ code, language = '' }) {
  const [copied, setCopied] = useState(false);
  const [detectedLanguage, setDetectedLanguage] = useState('text');

  // Map of common language aliases to Prism.js language names
  const languageMap = {
    py: 'python',
    js: 'javascript',
    jsx: 'javascript',
    ts: 'typescript',
    tsx: 'typescript',
    c: 'c',
    cpp: 'cpp',
    h: 'c',
    hpp: 'cpp',
    java: 'java',
    go: 'go',
    sh: 'bash',
    zsh: 'bash',
    json: 'json',
  };

  useEffect(() => {
    // Try to detect language from the provided language prop or file extension
    const lang = language.toLowerCase();
    if (languageMap[lang] || languages[lang]) {
      setDetectedLanguage(languageMap[lang] || lang);
    } else if (language.includes('python')) {
      setDetectedLanguage('python');
    } else if (language.includes('java')) {
      setDetectedLanguage('java');
    } else if (language.includes('javascript')) {
      setDetectedLanguage('javascript');
    } else if (language.includes('c++') || language.includes('cpp')) {
      setDetectedLanguage('cpp');
    } else if (language.includes('c ')) {
      setDetectedLanguage('c');
    } else if (language.includes('go')) {
      setDetectedLanguage('go');
    } else {
      setDetectedLanguage('text');
    }
  }, [language]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  // Tema VS Code Dark+ autentico - colori IDE realistici
  const customVSCTheme = {
    'code[class*="language-"]': {
      color: '#d4d4d4',
      background: '#1e1e1e',
      fontFamily: '"Fira Code", "Cascadia Code", "JetBrains Mono", Consolas, "Courier New", monospace',
      fontSize: '0.875rem',
      textAlign: 'left',
      whiteSpace: 'pre',
      wordSpacing: 'normal',
      wordBreak: 'normal',
      lineHeight: '1.6',
      tabSize: 4,
    },
    'pre[class*="language-"]': {
      color: '#d4d4d4',
      background: '#1e1e1e',
      padding: 0,
      margin: 0,
      overflow: 'auto',
      fontSize: '0.875rem',
      lineHeight: '1.6',
    },
    'comment': { color: '#6a9955', fontStyle: 'italic' },
    'prolog': { color: '#6a9955' },
    'doctype': { color: '#6a9955' },
    'cdata': { color: '#6a9955' },
    'punctuation': { color: '#d4d4d4' },
    'property': { color: '#9cdcfe' },
    'tag': { color: '#569cd6' },
    'boolean': { color: '#569cd6' },
    'number': { color: '#b5cea8' },
    'constant': { color: '#4fc1ff' },
    'symbol': { color: '#4fc1ff' },
    'deleted': { color: '#f44747' },
    'selector': { color: '#d7ba7d' },
    'attr-name': { color: '#9cdcfe' },
    'string': { color: '#ce9178' },
    'char': { color: '#ce9178' },
    'builtin': { color: '#4ec9b0' },
    'inserted': { color: '#b5cea8' },
    'operator': { color: '#d4d4d4' },
    'entity': { color: '#d7ba7d' },
    'url': { color: '#3b8eea' },
    'variable': { color: '#9cdcfe' },
    'atrule': { color: '#c586c0' },
    'attr-value': { color: '#ce9178' },
    'function': { color: '#dcdcaa' },
    'class-name': { color: '#4ec9b0' },
    'keyword': { color: '#569cd6' },
    'regex': { color: '#d16969' },
    'important': { color: '#569cd6', fontWeight: 'bold' },
    'bold': { fontWeight: 'bold' },
    'italic': { fontStyle: 'italic' },
    'namespace': { opacity: 0.7 },
  };

  return (
    <div className="relative group my-4 rounded-lg overflow-hidden bg-[#1e1e1e] border border-[#3e3e42]">
      {/* Language label and copy button container - ChatGPT style */}
      <div className="flex items-center justify-between bg-[#2f2f2f] px-4 py-2.5 border-b border-gray-800/50">
        <span className="text-xs text-gray-300 font-medium tracking-wide uppercase">
          {detectedLanguage || 'code'}
        </span>
        <button
          onClick={handleCopy}
          className="flex items-center gap-2 px-3 py-1.5 text-xs font-medium text-gray-300 bg-transparent hover:bg-gray-700/50 rounded-md transition-all duration-200 active:scale-95 focus:outline-none focus:ring-2 focus:ring-gray-500/50"
          title={copied ? "Copiato!" : "Copia codice"}
          aria-label="Copia codice negli appunti"
        >
          {copied ? (
            <>
              <Check className="w-3.5 h-3.5 text-green-400" />
              <span className="text-green-400">Copiato!</span>
            </>
          ) : (
            <>
              <Copy className="w-3.5 h-3.5" />
              <span>Copia codice</span>
            </>
          )}
        </button>
      </div>
      
      {/* Code content with syntax highlighting */}
      <div className="overflow-x-auto">
        <SyntaxHighlighter
          language={detectedLanguage}
          style={customVSCTheme}
          customStyle={{
            margin: 0,
            padding: '1.25rem 1.5rem',
            background: '#1e1e1e',
            borderRadius: 0,
            fontSize: '0.875rem',
            lineHeight: '1.6',
          }}
          showLineNumbers={code.split('\n').length > 5}
          wrapLines={true}
          wrapLongLines={false}
          lineNumberStyle={{
            color: '#858585',
            paddingRight: '1.5em',
            userSelect: 'none',
            minWidth: '2.5em',
            textAlign: 'right',
            borderRight: '1px solid #3e3e42',
            marginRight: '1em',
          }}
        >
          {code}
        </SyntaxHighlighter>
      </div>
    </div>
  );
}
