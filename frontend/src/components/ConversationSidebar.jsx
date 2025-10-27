import { useState } from 'react';
import { MessageSquare, Plus, Trash2, Download, Upload, X } from 'lucide-react';

export default function ConversationSidebar({ 
  conversations, 
  currentId, 
  onSelect, 
  onNew, 
  onDelete,
  onExport,
  onImport,
  isOpen,
  onClose,
  translations
}) {
  const [deleteConfirm, setDeleteConfirm] = useState(null);

  const handleDelete = (id) => {
    if (deleteConfirm === id) {
      onDelete(id);
      setDeleteConfirm(null);
    } else {
      setDeleteConfirm(id);
      setTimeout(() => setDeleteConfirm(null), 3000);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return translations.justNow;
    if (diffMins < 60) return translations.minutesAgo.replace('{n}', diffMins);
    if (diffHours < 24) return translations.hoursAgo.replace('{n}', diffHours);
    if (diffDays < 7) return translations.daysAgo.replace('{n}', diffDays);
    return date.toLocaleDateString();
  };

  return (
    <>
      {/* Overlay per mobile */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed lg:relative top-0 left-0 h-full w-80 bg-hal-panel border-r-2 border-red-900 
        flex flex-col z-50 transition-transform duration-300
        ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        {/* Header */}
        <div className="p-4 border-b border-red-900 flex items-center justify-between">
          <h2 className="text-red-500 font-bold flex items-center gap-2">
            <MessageSquare className="w-5 h-5" />
            {translations.conversations}
          </h2>
          <button
            onClick={onClose}
            className="lg:hidden text-red-500 hover:text-red-400"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* New conversation button */}
        <div className="p-4 border-b border-red-900">
          <button
            onClick={onNew}
            className="w-full bg-red-900 hover:bg-red-800 text-white px-4 py-2 rounded flex items-center justify-center gap-2 transition-colors"
          >
            <Plus className="w-4 h-4" />
            {translations.newConversation}
          </button>
        </div>

        {/* Conversations list */}
        <div className="flex-1 overflow-y-auto p-2">
          {conversations.length === 0 ? (
            <div className="text-center text-red-400 opacity-60 py-8 px-4">
              {translations.noConversations}<br />
              {translations.startNew}
            </div>
          ) : (
            conversations.map(conv => (
              <div
                key={conv.id}
                className={`
                  mb-2 p-3 rounded cursor-pointer transition-all group
                  ${conv.id === currentId 
                    ? 'bg-red-900 border-2 border-red-700' 
                    : 'bg-black border border-red-900 hover:border-red-700'
                  }
                `}
                onClick={() => onSelect(conv.id)}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1 min-w-0">
                    <div className="text-red-200 text-sm font-medium truncate">
                      {conv.title}
                    </div>
                    <div className="text-red-400 text-xs opacity-60 mt-1">
                      {conv.language} • {formatDate(conv.updatedAt)}
                    </div>
                    <div className="text-red-400 text-xs opacity-40 mt-1">
                      {conv.messages.length} {translations.messages}
                    </div>
                  </div>
                  
                  {/* Actions */}
                  <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onExport(conv.id);
                      }}
                      className="p-1 hover:bg-red-800 rounded"
                      title={translations.exportTooltip}
                    >
                      <Download className="w-3 h-3 text-red-400" />
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDelete(conv.id);
                      }}
                      className={`p-1 rounded ${
                        deleteConfirm === conv.id 
                          ? 'bg-red-600 hover:bg-red-700' 
                          : 'hover:bg-red-800'
                      }`}
                      title={deleteConfirm === conv.id ? translations.deleteConfirm : translations.deleteTooltip}
                    >
                      <Trash2 className="w-3 h-3 text-red-400" />
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Import button */}
        <div className="p-4 border-t border-red-900">
          <label className="w-full bg-black hover:bg-red-950 text-red-400 px-4 py-2 rounded flex items-center justify-center gap-2 transition-colors cursor-pointer border border-red-900">
            <Upload className="w-4 h-4" />
            {translations.importConversation}
            <input
              type="file"
              accept=".json"
              onChange={(e) => {
                if (e.target.files[0]) {
                  onImport(e.target.files[0]);
                  e.target.value = '';
                }
              }}
              className="hidden"
            />
          </label>
        </div>
      </div>
    </>
  );
}
