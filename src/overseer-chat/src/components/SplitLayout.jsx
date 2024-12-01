// src/components/SplitLayout.jsx
import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Send, PanelRightOpen, PanelRightClose, WifiOff } from 'lucide-react';

const WEBSOCKET_RETRY_DELAY = 1000;

const SplitLayout = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [socket, setSocket] = useState(null);
    const [isConnected, setIsConnected] = useState(false);
    const [currentModel, setCurrentModel] = useState('');
    const [isPanelOpen, setIsPanelOpen] = useState(true);
    const reconnectTimeoutRef = useRef(null);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    const connect = useCallback(() => {
        try {
            const ws = new WebSocket('ws://localhost:8000/overseer');
            ws.onopen = () => {
                setIsConnected(true);
                if (reconnectTimeoutRef.current) {
                    clearTimeout(reconnectTimeoutRef.current);
                    reconnectTimeoutRef.current = null;
                }
            };

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.answer) {
                    setMessages(prev => [...prev, {
                        type: 'assistant',
                        content: data.answer,
                    }]);
                }
                if (data.permission_model) {
                    setCurrentModel(data.permission_model);
                }
            };

            ws.onclose = () => {
                setIsConnected(false);
                reconnectTimeoutRef.current = setTimeout(connect, WEBSOCKET_RETRY_DELAY);
            };

            ws.onerror = (error) => {
                ws.close();
            };

            setSocket(ws);
        } catch (error) {
            setIsConnected(false);
        }
    }, []);

    useEffect(() => {
        connect();
        return () => {
            if (socket) socket.close();
            if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
        };
    }, [connect]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!input.trim() || !isConnected) return;

        setMessages(prev => [...prev, { type: 'user', content: input }]);
        try {
            socket.send(JSON.stringify({ question: input }));
            setInput('');
        } catch (error) {
            setMessages(prev => [...prev, {
                type: 'system',
                content: 'Failed to send message. Please try again.'
            }]);
        }
    };

    const togglePanel = () => setIsPanelOpen(!isPanelOpen);

    return (
        <div className="h-screen w-screen flex bg-gray-900 text-gray-100">
            {/* Left Panel */}
            <div className={`flex flex-col ${isPanelOpen ? 'w-1/2' : 'w-[85%]'} transition-all duration-300`}>
                {/* Header */}
                <div className="h-16 p-4 border-b border-gray-700 flex items-center">
                    <div className="flex items-center gap-6">
                        <div className="flex items-center gap-3">
                            <img
                                src="/RelFGA-logo.png"
                                alt="Logo"
                                className="h-16 w-auto" // Zwiększone z h-8 na h-12
                                onError={(e) => {
                                    e.target.onerror = null;
                                    e.target.src = 'https://via.placeholder.com/48x48?text=Logo';
                                }}
                            />
                            <span className="text-xl font-semibold">RelFGA overseer</span>
                        </div>
                        <div className={`inline-flex items-center gap-2 px-3 py-1 rounded ${
                            isConnected ? 'bg-green-600' : 'bg-red-600'
                        }`}>
                            {isConnected ? 'Connected' : 'Disconnected'}
                            {!isConnected && <WifiOff className="w-4 h-4" />}
                        </div>
                    </div>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-4">
                    {messages.map((message, index) => (
                        <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'} mb-4`}>
                            <div className={`p-3 rounded-lg max-w-[80%] ${
                                message.type === 'user'
                                    ? 'bg-blue-600'
                                    : message.type === 'system'
                                    ? 'bg-red-900'
                                    : 'bg-gray-700'
                            }`}>
                                <p className="break-words">{message.content}</p>
                            </div>
                        </div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input */}
                <div className="h-20 p-4 border-t border-gray-700">
                    <form onSubmit={handleSubmit} className="flex gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder={isConnected ? "Type your message..." : "Connecting..."}
                            disabled={!isConnected}
                            className="flex-1 p-2 rounded bg-gray-800 border border-gray-600 text-gray-100 placeholder-gray-400
                                     focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-900 disabled:cursor-not-allowed"
                        />
                        <button
                            type="submit"
                            disabled={!isConnected}
                            className="p-2 bg-blue-600 rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500
                                     disabled:bg-gray-700 disabled:cursor-not-allowed transition-colors"
                        >
                            <Send className="w-5 h-5" />
                        </button>
                    </form>
                </div>
            </div>

            {/* Right Panel */}
            <div className={`flex flex-col border-l border-gray-700 ${
                isPanelOpen ? 'w-1/2' : 'w-[15%]'
            } transition-all duration-300`}>
                <div className="h-16 border-b border-gray-700 flex items-center relative">
                    {/* Tytuł wycentrowany */}
                    <div className="absolute w-full text-center">
                        <h2 className={`text-xl font-semibold transition-opacity duration-300 ${
                            isPanelOpen ? 'opacity-100' : 'opacity-0'
                        }`}>
                            Permission Model
                        </h2>
                    </div>
                    {/* Przycisk w prawym rogu */}
                    <div className="absolute right-4">
                        <button
                            onClick={togglePanel}
                            className="p-2 hover:bg-gray-700 rounded-full transition-colors"
                        >
                            {isPanelOpen ? <PanelRightClose className="w-6 h-6" /> : <PanelRightOpen className="w-6 h-6" />}
                        </button>
                    </div>
                </div>

                <div className={`flex-1 overflow-y-auto p-4 ${
                    isPanelOpen ? 'opacity-100' : 'opacity-0'
                } transition-opacity duration-300`}>
                    <pre className="font-mono bg-gray-800 p-4 rounded-lg text-sm whitespace-pre-wrap">
                        {currentModel || 'No model loaded'}
                    </pre>
                </div>
            </div>
        </div>
    );
};

export default SplitLayout;