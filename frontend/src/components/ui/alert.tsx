import { ReactNode } from 'react';
import { cn } from '../../lib/utils';
import { AlertTriangle, CheckCircle, XCircle, Info } from 'lucide-react';

interface AlertProps {
  children: ReactNode;
  variant?: 'default' | 'destructive' | 'success' | 'warning';
  className?: string;
}

const icons = {
  default: Info,
  destructive: XCircle,
  success: CheckCircle,
  warning: AlertTriangle,
};

export const Alert = ({ 
  children, 
  variant = 'default', 
  className 
}: AlertProps) => {
  const Icon = icons[variant];

  return (
    <div
      className={cn(
        "relative rounded-lg border p-4 flex items-start gap-3",
        {
          'default': 'bg-blue-50 border-blue-200 text-blue-800',
          'destructive': 'bg-red-50 border-red-200 text-red-800',
          'success': 'bg-green-50 border-green-200 text-green-800',
          'warning': 'bg-yellow-50 border-yellow-200 text-yellow-800',
        }[variant],
        className
      )}
    >
      <Icon className="h-5 w-5 mt-0.5" />
      <div>{children}</div>
    </div>
  );
};