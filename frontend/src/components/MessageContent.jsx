import CodeBlock from './CodeBlock';

export default function MessageContent({ content }) {
  // Parse content to extract code blocks
  const parseContent = (text) => {
    const parts = [];
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    let lastIndex = 0;
    let match;

    while ((match = codeBlockRegex.exec(text)) !== null) {
      // Add text before code block
      if (match.index > lastIndex) {
        parts.push({
          type: 'text',
          content: text.slice(lastIndex, match.index)
        });
      }

      // Add code block
      parts.push({
        type: 'code',
        language: match[1] || '',
        content: match[2].trim()
      });

      lastIndex = match.index + match[0].length;
    }

    // Add remaining text
    if (lastIndex < text.length) {
      parts.push({
        type: 'text',
        content: text.slice(lastIndex)
      });
    }

    return parts.length > 0 ? parts : [{ type: 'text', content: text }];
  };

  const parts = parseContent(content);

  return (
    <div>
      {parts.map((part, index) => {
        if (part.type === 'code') {
          return (
            <div key={index} className="my-4">
              <CodeBlock
                code={part.content}
                language={part.language}
              />
            </div>
          );
        } else {
          // Processa il testo per mantenere i ritorni a capo e la formattazione
          const formattedContent = part.content
            .split('\n')
            .map((line, i) => {
              // Mantieni le righe vuote come <br />
              if (line.trim() === '') {
                return <br key={i} />;
              }
              return (
                <p key={i} className="text-gray-100 leading-7 mb-3">
                  {line}
                </p>
              );
            });
            
          return (
            <div key={index} className="text-base">
              {formattedContent}
            </div>
          );
        }
      })}
    </div>
  );
}
