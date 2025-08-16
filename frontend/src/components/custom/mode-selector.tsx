'use client';

import { type ReactNode, startTransition, useEffect, useOptimistic, useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { cn } from '@/lib/utils';
import { CheckCircleIcon, ChevronDownIcon, GlobeIcon, LockIcon } from 'lucide-react';
import axios from 'axios';
import { useParams } from 'next/navigation';



export type VisibilityType = 'private' | 'public';


const visibilities: Array<{
  id: VisibilityType;
  label: string;
  description: string;
  icon: ReactNode;
}> = [
    {
      id: 'private',
      label: 'Private',
      description: 'Only you can access this chat',
      icon: <LockIcon />,
    },
    {
      id: 'public',
      label: 'Public',
      description: 'Anyone with the link can access this chat',
      icon: <GlobeIcon />,
    },
  ];

export function ModeSelector({
  className,
  chatVisibility,
}: {
  className?: string;
  chatVisibility: VisibilityType;
} & React.ComponentProps<typeof Button>) {
  const [open, setOpen] = useState(false);
  const [visibility, setVisibility] = useState<VisibilityType>(chatVisibility);
  const params = useParams<{ chat: string }>();
  const [optimisticVisibility, addOptimisticVisibility] = useOptimistic<VisibilityType>(visibility);
  
  useEffect(() => {
  setVisibility(chatVisibility);
}, [chatVisibility]);
  
  console.log('ModeSelector visibility:', chatVisibility);
  const handleVisibilityChange = (newVisibility: 'private' | 'public') => {
    const isPublic = newVisibility === 'public';

    axios.patch(`/api/chat/${params.chat}/visibility`, {
      is_public: isPublic, // match FastAPI's expected body
    }, {
      withCredentials: true,
    })
      .then(() => {
        return "update successfull"
      })
      .catch((error) => {
        console.error('Error updating chat visibility:', error);
      });
  };



  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger
        asChild
        className={cn(
          'w-fit data-[state=open]:bg-accent data-[state=open]:text-accent-foreground',
          className,
        )}
      >
        <Button
          data-testid="visibility-selector"
          variant="outline"
          className="hidden md:flex md:px-2 md:h-[34px]"
        >

          {
            optimisticVisibility === 'private' ? (
              <LockIcon className="mr-2 h-4 w-4" />
            ) : (
              <GlobeIcon className="mr-2 h-4 w-4" />
            )
          }
          <span className="text-sm font-medium">
            {visibilities.find((v) => v.id === optimisticVisibility)?.label}
          </span>
          <ChevronDownIcon />
        </Button>
      </DropdownMenuTrigger>

      <DropdownMenuContent align="start" className="min-w-[300px]">
        {visibilities.map((visibility) => (
          <DropdownMenuItem
            data-testid={`visibility-selector-item-${visibility.id}`}
            key={visibility.id}
            onSelect={() => {
              startTransition(async () => {
                addOptimisticVisibility(visibility.id);
                console.log('Selected visibility:', visibility.id);
                try {
                  await handleVisibilityChange(visibility.id);
                  setVisibility(visibility.id)
                } catch (error) {
                  console.error('Error updating visibility:', error);
                }

              });
            }}
            className="gap-4 group/item flex flex-row justify-between items-center"
            data-active={visibility.id === optimisticVisibility}
          >
            <div className="flex flex-col gap-1 items-start">
              {visibility.label}
              {visibility.description && (
                <div className="text-xs text-muted-foreground">
                  {visibility.description}
                </div>
              )}
            </div>
            <div className="text-foreground dark:text-foreground opacity-0 group-data-[active=true]/item:opacity-100">
              <CheckCircleIcon />
            </div>
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}