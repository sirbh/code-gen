import { ArrowUp } from "lucide-react";
import { Button } from "../ui/button";
import { Card, CardContent } from "../ui/card";
import { Textarea } from "../ui/textarea";

export default function ChatInput({
  input,
  setInput,
  handleSend,
  showDefaultOptions,
  loading,
  messageLoading
}: {
  input: string;
  setInput: (value: string) => void;
  handleSend: () => void;
  showDefaultOptions: boolean;
  loading: boolean;
  messageLoading: boolean;
}) {
  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const suggestions = [
    {
      prompt: "Summarize this conversation",
      description: "Get a concise summary of the chat so far.",
    },
    {
      prompt: "What are the next steps?",
      description: "Ask the assistant to provide action items.",
    },
    {
      prompt: "Explain this more simply",
      description: "Ask for a beginner-friendly explanation.",
    },
    {
      prompt: "List pros and cons",
      description: "Get a balanced comparison of any topic discussed.",
    },
  ];

  return (
    <div className="w-full max-w-2xl mx-auto px-4 py-6 sticky bottom-0 bg-muted space-y-4">
      {/* Suggested Messages */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {loading && suggestions.map((s, idx) => (
          <Card
            key={idx}
            className="transition p-4 flex animate-pulse space-x-4"
          >
            <CardContent className="">
              <div className="flex-1 space-y-6 py-1">
                <div className="h-2 rounded bg-gray-200"></div>
                <div className="space-y-3">
                  <div className="grid grid-cols-3 gap-4">
                    <div className="col-span-2 h-2 rounded bg-gray-200"></div>
                    <div className="col-span-1 h-2 rounded bg-gray-200"></div>
                  </div>
                  <div className="h-2 rounded bg-gray-200"></div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Chat Input */}
      <div className="flex items-end gap-2 relative">
        <Textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Send a message..."
          rows={1}
          className="min-h-[100px] max-h-[200px] resize-none text-base p-3 flex-1 pb-12"
          disabled={loading||messageLoading}
        />
        <Button className="absolute" variant="ghost" onClick={handleSend} disabled={loading||messageLoading}>
          <ArrowUp size={16} className="right-0" />
        </Button>
      </div>
    </div>
  );
}
