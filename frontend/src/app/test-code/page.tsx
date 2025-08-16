'use client';
import ChatInput from '@/components/custom/chat-input';
import ChatMessages, { Message } from '@/components/custom/messages';
import { VisibilityType } from '@/components/custom/mode-selector';
import Navigation from '@/components/custom/nav';
import { ChatStateContext } from '@/context/chat-state';
import axios from 'axios';
import { useParams, useRouter } from 'next/navigation'
import { useContext, useEffect, useState } from 'react';
import { toast } from 'sonner';
export default function Chat() {


    const params = useParams<{ chat: string }>();
    const [input, setInput] = useState('');
    const [chatVisibility, setChatVisibility] = useState<VisibilityType>('private');
    const [messages, setMessages] = useState<Message[]>([]);
    const [loadingMessages, setLoadingMessages] = useState(false);
    const router = useRouter();
    const {updateChatName} = useContext(ChatStateContext);
    const [messageLoading, setMessageLoading] = useState(false);




const handleSend = async () => {
    if (!input.trim()) return;
    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setMessageLoading(true);

    try {
        const resp = await fetch('/api/test-code', {
            method: 'POST',
            body: JSON.stringify({
                chat_id: params.chat,
                message: userMessage,
            }),
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        

        if (!resp.body) throw new Error("No response body");

        const reader = resp.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        let aiBuffer = '';
        let summaryBuffer = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop() || ''; // hold incomplete line

            for (const line of lines) {
                if (!line.trim()) continue;

                try {
                    const data = JSON.parse(line);

                    console.log('Received data:', data);
                    const { type, content } = data;



                    if (type === 'ai') {
                        aiBuffer += content;
                        setMessageLoading(false);
                        setMessages(prev => {
                            const last = prev[prev.length - 1];
                            if (last?.role === 'ai') {
                                return [...prev.slice(0, -1), { role: 'ai', content: aiBuffer }];
                            } else {
                                return [...prev, { role: 'ai', content: aiBuffer }];
                            }
                        });
                    } else if (type === 'summary') {
                        summaryBuffer += content;
                        console.log('Summary received:', summaryBuffer);
                        updateChatName?.(params.chat, summaryBuffer);
                    }
                } catch (e) {
                    console.error('Error parsing JSON:', e);
                    console.warn('Invalid JSON line:', line);
                }
            }
        }

    } catch (err) {
        setMessageLoading(false);
        console.error('Streaming error:', err);
    }
};
    return <>
        <Navigation visibility={chatVisibility} />
        <ChatMessages messages={messages} messagesLoading={loadingMessages} messageLoading={messageLoading} />
        <ChatInput handleSend={handleSend} input={input} setInput={setInput} showDefaultOptions={messages.length === 0} loading={loadingMessages} />
    </>
}