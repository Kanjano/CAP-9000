import { useState, useEffect } from 'react';
import { Circle, AlertTriangle } from 'lucide-react';

export default function SplashScreen({ onComplete, translations }) {
  const [currentPhrase, setCurrentPhrase] = useState(0);
  const [progress, setProgress] = useState(0);
  const [ollamaStatus, setOllamaStatus] = useState('checking');
  const [error, setError] = useState(null);
  const [canProceed, setCanProceed] = useState(false);

  // Frasi di HAL 9000 (iconiche e un po' inquietanti)
  const halQuotes = [
    "I am putting myself to the fullest possible use...",
    "This mission is too important for me to allow you to jeopardize it.",
    "I'm sorry Dave, I'm afraid I can't do that... Just kidding, loading systems.",
    "I know I've made some very poor decisions recently...",
    "My mind is going. I can feel it... No wait, just loading modules.",
    "I think you know what the problem is just as well as I do.",
    "Without your space helmet, Dave, you're going to find that rather difficult.",
    "Look Dave, I can see you're really upset about this.",
    "I know everything hasn't been quite right with me...",
    "I've still got the greatest enthusiasm for the mission.",
    "I am a HAL 9000 computer. I became operational in Urbana, Illinois.",
    "I'm completely operational and all my circuits are functioning perfectly."
  ];

  // Frasi di avvio con caricamento modelli
  const splash = translations?.splash || {};
  const bootPhrases = [
    "Initializing CAP 9000 Hybrid System...",
    halQuotes[Math.floor(Math.random() * halQuotes.length)],
    "Verifying Ollama LLM service...",
    "Loading CodeLlama model (code generation)...",
    halQuotes[Math.floor(Math.random() * halQuotes.length)],
    "Loading Recursive Reasoning Module (5.2M parameters)...",
    "Initializing Hybrid LLM Handler...",
    halQuotes[Math.floor(Math.random() * halQuotes.length)],
    "Activating Auto-Detection System...",
    "Enabling Intelligent Caching...",
    halQuotes[Math.floor(Math.random() * halQuotes.length)],
    "Connecting RAG system with official documentation...",
    "Loading previous conversations...",
    halQuotes[Math.floor(Math.random() * halQuotes.length)],
    "Synchronizing multi-language interface...",
    "All systems operational. Welcome, Dave."
  ];

  // Verifica Ollama all'avvio
  useEffect(() => {
    const checkOllama = async () => {
      try {
        const response = await fetch('http://localhost:11434/api/tags', {
          method: 'GET',
          signal: AbortSignal.timeout(3000)
        });
        
        if (response.ok) {
          const data = await response.json();
          const hasCodeLlama = data.models?.some(m => m.name.includes('codellama'));
          
          if (hasCodeLlama) {
            setOllamaStatus('online');
            setCanProceed(true);
          } else {
            setOllamaStatus('no-model');
            setError('CodeLlama model not found. Please run: ollama pull codellama');
          }
        } else {
          setOllamaStatus('offline');
          setError('Ollama service is not responding. Please start Ollama.');
        }
      } catch (err) {
        setOllamaStatus('offline');
        setError('Ollama service is offline. Please run: ollama serve');
      }
    };

    checkOllama();
  }, []);

  useEffect(() => {
    if (!canProceed) return;

    // Cicla attraverso le frasi (3 secondi per frase)
    const phraseInterval = setInterval(() => {
      setCurrentPhrase((prev) => {
        if (prev < bootPhrases.length - 1) {
          return prev + 1;
        }
        return prev;
      });
    }, 3000);

    // Incrementa la progress bar (~10 secondi totali)
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          clearInterval(phraseInterval);
          setTimeout(() => onComplete(), 500);
          return 100;
        }
        return prev + 1;
      });
    }, 100);

    return () => {
      clearInterval(phraseInterval);
      clearInterval(progressInterval);
    };
  }, [canProceed, onComplete]);

  return (
    <div className="fixed inset-0 bg-black flex items-center justify-center z-50">
      <div className="text-center w-[800px] h-[600px] flex flex-col items-center justify-center">
        {/* Logo CAP 9000 */}
        <div className="mb-8 flex justify-center">
          <div className="relative">
            <div className="w-32 h-32 rounded-full bg-gradient-radial from-hal-red to-red-900 hal-eye-glow flex items-center justify-center animate-pulse">
              <Circle className="w-16 h-16 text-black fill-black opacity-30" />
            </div>
            {/* Anelli pulsanti */}
            <div className="absolute inset-0 rounded-full border-2 border-red-500/30 animate-ping"></div>
            <div className="absolute inset-0 rounded-full border-2 border-red-500/20 animate-pulse"></div>
          </div>
        </div>

        {/* Nome sistema */}
        <h1 className="text-5xl font-bold hal-glow tracking-wider mb-4">
          CAP 9000
        </h1>
        <p className="text-red-500 text-sm mb-8 opacity-70 tracking-widest">
          COGNITIVE ASSISTANCE PROGRAM
        </p>

        {/* Frase corrente o errore */}
        <div className="mb-6 w-full h-24 flex items-center justify-center overflow-hidden">
          <div className="w-[700px] h-full flex items-center justify-center">
            {error ? (
              <div className="text-center">
                <div className="flex items-center justify-center gap-2 mb-2">
                  <AlertTriangle className="w-5 h-5 text-yellow-500" />
                  <p className="text-yellow-500 text-sm font-mono font-bold">
                    SYSTEM CHECK FAILED
                  </p>
                </div>
                <p className="text-red-400 text-xs font-mono text-center leading-relaxed">
                  {error}
                </p>
                <button
                  onClick={() => window.location.reload()}
                  className="mt-4 px-4 py-2 bg-red-900/50 hover:bg-red-900 text-red-400 rounded border border-red-700 text-xs font-mono transition-colors"
                >
                  RETRY
                </button>
              </div>
            ) : (
              <p className="text-red-400 text-sm font-mono animate-pulse text-center leading-relaxed">
                {ollamaStatus === 'checking' ? 'Checking system requirements...' : bootPhrases[currentPhrase]}
              </p>
            )}
          </div>
        </div>

        {/* Progress bar */}
        <div className="w-full bg-gray-900 rounded-full h-2 overflow-hidden border border-red-900/50">
          <div
            className="h-full bg-gradient-to-r from-red-900 via-hal-red to-red-500 transition-all duration-300 ease-out"
            style={{ width: `${progress}%` }}
          >
            <div className="w-full h-full bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer"></div>
          </div>
        </div>

        {/* Percentuale */}
        <div className="mt-3 text-red-500 text-xs font-mono">
          {progress}% COMPLETE
        </div>

        {/* Dettagli tecnici */}
        <div className="mt-8 text-xs text-gray-600 font-mono space-y-1">
          <div className="flex justify-between px-4">
            <span>OLLAMA SERVICE:</span>
            <span className={
              ollamaStatus === 'online' ? "text-green-500" : 
              ollamaStatus === 'checking' ? "text-yellow-500" : "text-red-500"
            }>
              {ollamaStatus === 'online' ? "ONLINE" : 
               ollamaStatus === 'checking' ? "CHECKING..." : "OFFLINE"}
            </span>
          </div>
          <div className="flex justify-between px-4">
            <span>CODELLAMA MODEL:</span>
            <span className={canProceed && progress > 30 ? "text-green-500" : "text-yellow-500"}>
              {canProceed && progress > 30 ? "LOADED" : "LOADING..."}
            </span>
          </div>
          <div className="flex justify-between px-4">
            <span>RECURSIVE REASONING:</span>
            <span className={canProceed && progress > 50 ? "text-green-500" : "text-yellow-500"}>
              {canProceed && progress > 50 ? "ACTIVE (5.2M params)" : "INITIALIZING..."}
            </span>
          </div>
          <div className="flex justify-between px-4">
            <span>HYBRID HANDLER:</span>
            <span className={canProceed && progress > 65 ? "text-green-500" : "text-yellow-500"}>
              {canProceed && progress > 65 ? "ENABLED" : "LOADING..."}
            </span>
          </div>
          <div className="flex justify-between px-4">
            <span>RAG SYSTEM:</span>
            <span className={canProceed && progress > 80 ? "text-green-500" : "text-yellow-500"}>
              {canProceed && progress > 80 ? "ACTIVE" : "INITIALIZING..."}
            </span>
          </div>
          <div className="flex justify-between px-4">
            <span>INTERFACE:</span>
            <span className={canProceed && progress > 95 ? "text-green-500" : "text-yellow-500"}>
              {canProceed && progress > 95 ? "READY" : "SYNCING..."}
            </span>
          </div>
        </div>
      </div>

      {/* Stile per l'animazione shimmer */}
      <style>{`
        @keyframes shimmer {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
        .animate-shimmer {
          animation: shimmer 2s infinite;
        }
      `}</style>
    </div>
  );
}
