
import React, { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from './ui/tooltip';

type NodeStatus = 'Offline' | 'Starting' | 'Online' | 'Error';

export const NetworkHealthOrb = () => {
  const [status, setStatus] = useState<NodeStatus>('Offline');
  const [route, setRoute] = useState('nym');

  const updateStatus = async () => {
    try {
      const result: NodeStatus = await invoke('get_node_status');
      setStatus(result);
    } catch (e) {
      setStatus('Error');
    }
  };

  useEffect(() => {
    updateStatus();
    const interval = setInterval(updateStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleStart = async () => {
    try {
      await invoke('start_sovereign_node', { route });
    } catch (e) {
      console.error("Failed to start node", e);
    }
  };

  const handleStop = async () => {
    try {
      await invoke('stop_sovereign_node');
    } catch (e) {
      console.error("Failed to stop node", e);
    }
  };

  const getOrbColor = () => {
    switch (status) {
      case 'Online': return 'bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.8)]';
      case 'Starting': return 'bg-yellow-400 animate-pulse shadow-[0_0_10px_rgba(250,204,21,0.8)]';
      case 'Error': return 'bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.8)]';
      default: return 'bg-gray-500';
    }
  };

  return (
    <TooltipProvider>
      <div className="flex items-center gap-3 px-3 py-2 rounded-full bg-slate-900/50 border border-slate-700 backdrop-blur-sm">
        <Tooltip>
          <TooltipTrigger asChild>
            <div className={`w-3 h-3 rounded-full cursor-help transition-all duration-500 ${getOrbColor()}`} />
          </TooltipTrigger>
          <TooltipContent>
            <p>Network Status: {status}</p>
          </TooltipContent>
        </Tooltip>
        
        <div className="flex items-center gap-2 border-l border-slate-700 pl-3">
          <select 
            value={route} 
            onChange={(e) => setRoute(e.target.value)}
            className="bg-transparent text-xs text-slate-400 outline-none cursor-pointer hover:text-white transition-colors"
          >
            <option value="nym" className="bg-slate-800">Nym</option>
            <option value="tor" className="bg-slate-800">Tor</option>
            <option value="i2p" className="bg-slate-800">I2p</option>
          </select>
          
          <button 
            onClick={status === 'Offline' ? handleStart : handleStop}
            className="text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded bg-slate-800 text-slate-300 hover:bg-slate-700 transition-colors"
          >
            {status === 'Offline' ? 'Start' : 'Stop'}
          </button>
        </div>
      </div>
    </TooltipProvider>
  );
};
