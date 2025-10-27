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

  // ChatGPT-inspired dark theme
  const customVSCTheme = {
    ...vscDarkPlus,
    'pre[class*="language-"]': {
      ...vscDarkPlus['pre[class*="language-"]'],
      background: '#0d0d0d',
      borderRadius: 0,
      padding: '0',
      margin: '0',
      overflow: 'auto',
      fontSize: '0.875rem',
      lineHeight: '1.6',
    },
    'code[class*="language-"]': {
      ...vscDarkPlus['code[class*="language-"]'],
      fontFamily: '"Söhne Mono", Monaco, "Andale Mono", "Ubuntu Mono", monospace',
      background: '#0d0d0d',
    },
  };

  return (
    <div className="relative group my-4 rounded-lg overflow-hidden bg-[#0d0d0d] border border-gray-800/50">
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
            background: '#0d0d0d',
            borderRadius: 0,
            fontSize: '0.875rem',
            lineHeight: '1.6',
          }}
          showLineNumbers={code.split('\n').length > 5}
          wrapLines={true}
          wrapLongLines={false}
          lineNumberStyle={{
            color: '#4a5568',
            paddingRight: '1.5em',
            userSelect: 'none',
            minWidth: '2.5em',
            textAlign: 'right',
            borderRight: '1px solid #2d3748',
            marginRight: '1em',
          }}
        >
          {code}
        </SyntaxHighlighter>
      </div>
    </div>
  );
}
