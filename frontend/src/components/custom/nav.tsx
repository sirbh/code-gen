"use client";

import { Circle, CircleAlert, PlusIcon } from "lucide-react";
import { Button } from "../ui/button";
import { Tooltip, TooltipContent, TooltipTrigger } from "../ui/tooltip";
import { VisibilityType } from "./mode-selector";
// import { SideMenuToggle } from "./side-menu-toggle";
import { ThemeSelector } from "./theme-selector";
import axios from "axios";
import { usePathname, useRouter } from "next/navigation";
import { toast } from "sonner";
import { useState } from "react";
import { set } from "date-fns";
import { ro } from "date-fns/locale";
// import { usePathname, useRouter } from "next/navigation";


interface INavigationProps {
    visibility?: VisibilityType;
    onClickHandler?: () => void;
}
export default function Navigation({ visibility, onClickHandler }: INavigationProps) {

    const [loading, setLoading] = useState(false);
    const router = useRouter();

    // const { open } = useSidebar();
    // const router = useRouter();
    const pathname = usePathname();

    console.log("Current pathname:", pathname);
    
    const handleSend = async (url:string) => {

    setLoading(true);

    try {
        const resp = await fetch(url, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        

        if (!resp.body) throw new Error("No response body");

        const reader = resp.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';


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
                    const { type } = data;



                    if (type === 'generated') {
                        setLoading(false);
                        toast.success('Server code generated successfully!');
                        router.push('/test-code'); // Redirect to test code page
                    } 
                } catch (e) {
                    console.error('Error parsing JSON:', e);
                    setLoading(false);
                    toast.error('Error parsing response from server.');
                }
            }
        }

    } catch (err) {
        setLoading(false);
        toast.error('Error generating server code. Please try again.');
    }
};

    const clickHandler = async () => {
        console.log("Button clicked, current pathname:", pathname);
        onClickHandler?.();
        
        // handleSend('/api/generate-server-code')
    }

    const resetHandler = async () => {
       try {
        await axios.get('/api/reset');
        toast.success('Chat reset successfully!');
        window.location.href = "/";
       } catch (error) {
           console.error("Error resetting chat:", error);
           toast.error('Error resetting chat. Please try again.');
       }
    }

    return (
        <div className="top-0 z-50 w-full border-b bg-transparent ">
            <div className="px-8 py-3 relative flex align-centre justify-between">
                <div className="flex justify-start items-center gap-2">

                    {/* <SideMenuToggle /> */}

                    {pathname !== '/test-code' && <Tooltip>
                        <TooltipTrigger asChild>
                            <Button
                                disabled={loading}
                                variant="outline"
                                className="px-2 md:h-fit ml-auto md:ml-0"
                                onClick={clickHandler}
                                data-testid="new-chat-button"
                            >
                                {loading ? (
                                    <div className="flex items-center gap-2">
                                        Generating...
                                    </div>
                                ) : (
                                    'Generate Server Code'
                                )}
                            </Button>
                        </TooltipTrigger>
                        <TooltipContent>Generate Server Code After Spec Has Been Saved</TooltipContent>
                    </Tooltip>
                    }

                    <Tooltip>
                        <TooltipTrigger asChild>
                            <Button
                                disabled={loading}
                                variant="outline"
                                className="px-2 md:h-fit ml-auto md:ml-0"
                                onClick={resetHandler}
                                data-testid="reset-button"
                            >
                               Reset Chat
                            </Button>
                        </TooltipTrigger>
                        <TooltipContent>Reset the chat and start a new conversation</TooltipContent>
                    </Tooltip>
                    {/* <ModeSelector className="w-full md:w-auto" chatVisibility={visibility!}/> */}
                </div>

                <ThemeSelector className="hidden md:flex" />

            </div>
        </div>
    );
}