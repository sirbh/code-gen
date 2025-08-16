'use client';

import { type ReactNode, useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { cn } from '@/lib/utils';
import { CheckCircleIcon, ChevronDownIcon, Computer, Moon, Sun } from 'lucide-react';
import { useTheme } from 'next-themes';



export type Theme = 'dark' | 'light' | 'system'    ;

const visibilities: Array<{
  id: Theme;
  label: string;
  description: string;
  icon: ReactNode;
}> = [
    {
      id: 'dark',
      label: 'Dark',
      description: 'Use dark mode for the interface',
      icon: <Moon />,
    },
    {
      id: 'light',
      label: 'Light',
      description: 'Use light mode for the interface',
      icon: <Sun />,
    },
    {
        id: 'system',
        label: 'System',
        description: 'Use system preference for the interface',
        icon: <Computer />,
    }
  ];

export function ThemeSelector({
  className,
}: {
  className?: string;
} & React.ComponentProps<typeof Button>) {
  const [open, setOpen] = useState(false);
  const {setTheme, theme} = useTheme();
  const [visibilityType, setVisibilityType] = useState<Theme>(theme as Theme || 'system');


  console.log('Current theme:', theme);

  const handleVisibilityChange = (type: Theme) => {
    setVisibilityType(type);
    setTheme(type);

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
            visibilityType === 'dark' ? (
              <Moon className="size-4" />
            ) : visibilityType === 'light' ? (
              <Sun className="size-4" />
            ) : (
              <Computer className="size-4" />
            )
           }
         
          <span className="text-sm font-medium">
            {visibilities.find((v) => v.id === visibilityType)?.label}
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
              setVisibilityType(visibility.id);
              setOpen(false);
              handleVisibilityChange(visibility.id);
            }}
            className="gap-4 group/item flex flex-row justify-between items-center"
            data-active={visibility.id === visibilityType}
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