'use client';
import { Card, CardContent } from "../ui/card";
import MarkdownRenderer from "./markdown-render";
import { useEffect, useRef } from "react";





export type Message = {
    role: 'user' | 'ai';
    content: string;
};

interface IMessagesProps {
    messages: Message[];
    messagesLoading: boolean;
    messageLoading: boolean;
}

export default function Messages({ messages, messagesLoading, messageLoading }: IMessagesProps) {

    const bottomRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);


    // const [messages, setMessages] = useState<Message[]>([
    //     { role: 'ai', content: 'Hi there! How can I help you today?' },
    //     { role: 'user', content: 'What is the weather like in Paris?' },
    //     { role: 'ai', content: 'Currently, it’s sunny and 24°C in Paris.' },
    //     { role: 'ai', content: 'Hi there! How can I help you today?' },
    //     { role: 'user', content: 'What is the weather like in Paris?' },
    //     { role: 'ai', content: 'Currently, it’s sunny and 24°C in Paris.' },
    //     { role: 'ai', content: 'Hi there! How can I help you today?' },
    //     { role: 'user', content: 'What is the weather like in Paris?' },
    //     { role: 'ai', content: 'Currently, it’s sunny and 24°C in Paris.' },
    // ]);
    // const [input, setInput] = useState('');

    // const handleSend = () => {
    //     if (!input.trim()) return;
    //     setMessages([...messages, { role: 'user', content: input }]);
    //     setInput('');
    // };

    // const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    //     if (e.key === 'Enter') handleSend();
    // };


    if (messagesLoading) {
        return (
            <div className="flex items-center justify-center h-full">
            </div>
        );
    }


    return (
        <>
            <div className="w-full h-full overflow-y-auto">
                <div className="flex-1 w-full max-w-2xl mx-auto flex flex-col gap-4 px-2 pt-8 pb-0 ">

                    {/* {messages.length === 0 && (
                        <div className="text-muted-foreground">
                            <h1 className="text-3xl">Hi! I am your medical assistant </h1>
                            <p className="text-lg">How can I help you today!</p>
                        </div>
                    )} */}
                    {messages.map((msg, idx) => (
                        <Card
                            key={idx}
                            className={`${msg.role=='ai'?'':'max-w-[80%]'} p-1 ${msg.role === 'user'
                                ? 'self-end'
                                : 'self-start bg-transparent shadow-none border-none'
                                }`}
                        >
                            <CardContent className="p-4 text-lg whitespace-pre-wrap">
                                <MarkdownRenderer content={msg.content} />
                            </CardContent>
                        </Card>
                    ))}
 
                    <div ref={bottomRef} className="p-6 h-4 w-full" >
                       {messageLoading && (
           
                           <div className="self-start h-4 w-4 bg-gray-200 rounded-full animate-spin self-center">
                              
                           </div>
  
                       )}
                    </div>
                </div>
            </div>
        </>

    )
}