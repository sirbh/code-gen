'use client';

import { createContext, useEffect, useState } from 'react';
import axios from 'axios';

export const ChatStateContext = createContext<{
    chats: { chat_id: string, info: { name: string } }[];
    loading: boolean;
    updateChatName?: (chatId: string, newName: string) => void;
    addChat?: (chat: { chat_id: string, info: { name: string } }) => void;
}>({
    chats: [],
    loading: false,
    updateChatName: (chatId: string, newName: string) => {
        console.log(`Update chat name called for ${chatId} to ${newName}`);
    },
    addChat: (chat) => {
        console.log(`Add chat called for ${chat.chat_id} with name ${chat.info.name}`);
    }
});


export default function ChatStateContextProvider({ children }: { children: React.ReactNode }) {
    const [chats, setChats] = useState<{ chat_id: string, info: { name: string } }[]>([]);
    const [loading, setLoading] = useState(false);

    const updateChatName = (chatId: string, newName: string) => {
        setChats(prevChats =>
            prevChats.map(chat =>
                chat.chat_id === chatId ? { ...chat, info: { ...chat.info, name: newName } } : chat
            )
        );
    };

    const addChat = (chat: { chat_id: string, info: { name: string } }) => {
        setChats(prevChats => [...prevChats, chat]);
    };

    const fetchChatHistory = async () => {
        try {
            setLoading(true);
            const res = await axios.get('/api/user-chats', {
                withCredentials: true,
            });
            setChats(res.data.chats);
        } catch (error) {
            console.error("Error fetching chat history:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchChatHistory();
    }, []);


    return (
        <ChatStateContext value={{ chats, loading, updateChatName, addChat }}>
            {children}
        </ChatStateContext>
    );
}
