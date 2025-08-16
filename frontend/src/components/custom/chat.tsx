import { useState } from "react";
import { Card, CardContent } from "../ui/card";
import { Input } from "../ui/input";
import { Button } from "../ui/button";




type Message = {
    role: 'user' | 'ai';
    content: string;
};

export default function Chat() {

    const [messages, setMessages] = useState<Message[]>([
        { role: 'ai', content: 'Hi there! How can I help you today?' },
        { role: 'user', content: 'What is the weather like in Paris?' },
        { role: 'ai', content: 'Currently, it’s sunny and 24°C in Paris.' },
        { role: 'ai', content: 'Hi there! How can I help you today?' },
        { role: 'user', content: 'What is the weather like in Paris?' },
        { role: 'ai', content: 'Currently, it’s sunny and 24°C in Paris.' },
        { role: 'ai', content: 'Hi there! How can I help you today?' },
        { role: 'user', content: 'What is the weather like in Paris?' },
        { role: 'ai', content: 'Currently, it’s sunny and 24°C in Paris.' },
    ]);
    const [input, setInput] = useState('');

    const handleSend = () => {
        if (!input.trim()) return;
        setMessages([...messages, { role: 'user', content: input }]);
        setInput('');
    };

    const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') handleSend();
    };

    return (
        <>

            <div className="flex-1 w-full max-w-2xl mx-auto flex flex-col gap-4 px-2 pt-6 pb-20 overflow-y-auto">
                {messages.map((msg, idx) => (
                    <Card
                        key={idx}
                        className={`max-w-[80%] p-1 ${msg.role === 'user'
                            ? 'self-end'
                            : 'self-start bg-transparent shadow-none border-none'
                            }`}
                    >
                        <CardContent className="p-4 text-lg whitespace-pre-wrap">
                            {msg.content}
                        </CardContent>
                    </Card>
                ))}
            </div>

            {/* Input area */}

        </>

    )
}