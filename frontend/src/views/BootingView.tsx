import { useEffect } from 'react';
import { ShieldCheck } from 'lucide-react';

export default function BootingView({ onComplete }: { onComplete: () => void }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onComplete();
    }, 2500);
    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <div className="w-full h-full bg-blue-700 flex flex-col items-center justify-center p-8 text-white font-mono">
      <div className="flex flex-col items-center animate-pulse">
        <ShieldCheck size={80} className="mb-6 drop-shadow-lg" />
        <h1 className="text-3xl font-bold tracking-widest text-center mb-2">网络开拓者协会</h1>
        <h2 className="text-xl tracking-widest text-center opacity-90">NPA BIOS POST...</h2>
        <p className="mt-8 opacity-75 text-sm">System Check OK.</p>
        <p className="mt-2 opacity-75 text-sm">Loading Kernel Modules...</p>
      </div>
    </div>
  );
}
