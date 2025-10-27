import { useState, useEffect } from 'react';
import { Circle } from 'lucide-react';

export default function SplashScreen({ onComplete }) {
  const [currentPhrase, setCurrentPhrase] = useState(0);
  const [progress, setProgress] = useState(0);

  // Frasi di avvio in stile CAP 9000
  const bootPhrases = [
    "Inizializzazione sistemi CAP 9000...",
    "Caricamento moduli di intelligenza artificiale...",
    "Verifica integrità neural network...",
    "Connessione a Ollama LLM in corso...",
    "Calibrazione assistente di programmazione...",
    "Attivazione knowledge base linguaggi...",
    "Sincronizzazione interfaccia utente...",
    "Preparazione ambiente di sviluppo...",
    "Sistema CAP 9000 quasi pronto...",
    "Tutti i sistemi operativi. Benvenuto."
  ];

  useEffect(() => {
    // Cicla attraverso le frasi
    const phraseInterval = setInterval(() => {
      setCurrentPhrase((prev) => {
        if (prev < bootPhrases.length - 1) {
          return prev + 1;
        }
        return prev;
      });
    }, 800);

    // Incrementa la progress bar
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          clearInterval(phraseInterval);
          setTimeout(() => onComplete(), 500);
          return 100;
        }
        return prev + 2;
      });
    }, 80);

    return () => {
      clearInterval(phraseInterval);
      clearInterval(progressInterval);
    };
  }, [onComplete]);

  return (
    <div className="fixed inset-0 bg-black flex items-center justify-center z-50">
      <div className="text-center max-w-2xl px-8">
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

        {/* Frase corrente */}
        <div className="mb-6 h-6">
          <p className="text-red-400 text-sm font-mono animate-pulse">
            {bootPhrases[currentPhrase]}
          </p>
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
            <span>NEURAL NETWORK:</span>
            <span className={progress > 30 ? "text-green-500" : "text-yellow-500"}>
              {progress > 30 ? "ONLINE" : "LOADING..."}
            </span>
          </div>
          <div className="flex justify-between px-4">
            <span>OLLAMA SERVICE:</span>
            <span className={progress > 60 ? "text-green-500" : "text-yellow-500"}>
              {progress > 60 ? "CONNECTED" : "CONNECTING..."}
            </span>
          </div>
          <div className="flex justify-between px-4">
            <span>INTERFACE:</span>
            <span className={progress > 90 ? "text-green-500" : "text-yellow-500"}>
              {progress > 90 ? "READY" : "INITIALIZING..."}
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
