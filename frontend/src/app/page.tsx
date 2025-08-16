'use client';
import ChatInput from '@/components/custom/chat-input';
import ChatMessages, { Message } from '@/components/custom/messages';
import { VisibilityType } from '@/components/custom/mode-selector';
import Navigation from '@/components/custom/nav';
import { ChatStateContext } from '@/context/chat-state';
import axios from 'axios';
import { useParams, useRouter, useSearchParams } from 'next/navigation'
import { useContext, useEffect, useState } from 'react';
import { toast } from 'sonner';
export default function Chat() {


    const params = useParams<{ chat: string }>();
    const [input, setInput] = useState('');
    const [chatUrl,setChatUrl] = useState('/api/chat');
    const [chatVisibility, setChatVisibility] = useState<VisibilityType>('private');
    const [messages, setMessages] = useState<Message[]>([]);
    const [loadingMessages, setLoadingMessages] = useState(false);
    const router = useRouter();
    const searchParams = useSearchParams();
    const phase = searchParams.get("phase");
    const { updateChatName } = useContext(ChatStateContext);
    const [messageLoading, setMessageLoading] = useState(false);

    const setQueryParam = (key: string, value: string) => {
        const params = new URLSearchParams(searchParams.toString());
        params.set(key, value);
        setChatUrl(`/api/test-code`);
        // Updates the URL with new query param
        router.replace(`?${params.toString()}`);
    }



    async function getChatHistory() {
        setLoadingMessages(true);
        try {
            const res = await axios.get(`/api/chat`, {
                withCredentials: true,
            });

            setMessages(res.data.messages)
            setChatVisibility(res.data.visibility);
            setLoadingMessages(false);
            toast.success("Chat loaded successfully");
        } catch (error) {
            console.error("Error fetching chat history:", error);
            toast.error("Failed to load chat");
            router.push('/');
        }
    }

    useEffect(() => {
        console.log('Fetching chat history for:', params.chat);
        getChatHistory();
    }, []);

    useEffect(() => {
        if(!phase) return;
        if (phase==='testing') {
            setChatUrl(`/api/test-code`);
        }
    }, [phase]);

    const handleSend = async (url: string) => {

        const userMessage = input;
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setMessageLoading(true);

        try {
            const resp = await fetch(url, {
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

            setMessageLoading(false);

        } catch (err) {
            setMessageLoading(false);
            console.error('Streaming error:', err);
        }
    };
    return <>
        <Navigation visibility={chatVisibility} onClickHandler={() => { setQueryParam('phase','testing') }} />
        <ChatMessages messages={messages} messagesLoading={loadingMessages} messageLoading={messageLoading} />
        <ChatInput handleSend={() => { handleSend(chatUrl) }} input={input} setInput={setInput} showDefaultOptions={messages.length === 0} messageLoading={messageLoading} loading={loadingMessages} />
    </>
}