'use client';

import { PlusIcon } from "lucide-react";
import { Button } from "../ui/button";
import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarHeader
} from "../ui/sidebar";
import {
    Tooltip,
    TooltipTrigger,
    TooltipContent
} from "../ui/tooltip";
import { useContext } from "react";
import { ChatStateContext } from "@/context/chat-state";
import { useRouter } from "next/navigation";

export default function SideMenu() {
    const router = useRouter();
    const {chats, loading} = useContext(ChatStateContext); // Assuming ChatStateContext is defined and provides chats and loading state

    console.log("Rendering SideMenu with chats:", chats);

    return (
        <Sidebar>
            <SidebarHeader className="mb-4">
                <div className="flex flex-row items-center justify-between">
                    <h1 className="text-lg font-semibold">Chat History</h1>
                    <Tooltip>
                        <TooltipTrigger asChild>
                            <Button variant="outline" className="px-2 md:h-fit ml-auto md:ml-0" onClick={() => router.push('/')}>
                                <PlusIcon />
                            </Button>
                        </TooltipTrigger>
                        <TooltipContent>New Chat</TooltipContent>
                    </Tooltip>
                </div>
            </SidebarHeader>
            <SidebarContent>
                <SidebarGroup className="px-4 overflow-hidden">
                    {loading ? (
                        <div className="animate-pulse space-y-2">
                            <div className="h-4 bg-gray-300 rounded w-3/4" />
                            <div className="h-4 bg-gray-300 rounded w-2/3" />
                        </div>
                    ) : (
                        chats.map((chat) => (
                            <Button
                                key={chat.chat_id}
                                variant="ghost"
                                className="w-full justify-start capitalize"
                                onClick={() => router.push(`/${chat.chat_id}`)}
                            >
                                {`${chat.info.name}`}
                            </Button>
                        ))
                    )}
                </SidebarGroup>
            </SidebarContent>
            <SidebarFooter />
        </Sidebar>
    );
}
