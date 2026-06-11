
import React, { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { Loader2, FileCheck, ShieldAlert, Cpu } from 'lucide-react';
import { toast } from 'sonner';

export default function ZkPluginPage() {
  const [plugins, setPlugins] = useState<string[]>([]);
  const [darkfiEnabled, setDarkfiEnabled] = useState(false);
  const [loading, setLoading] = useState(false);
  const [selectedPlugin, setSelectedPlugin] = useState<any>(null);

  const fetchPlugins = async () => {
    try {
      const result: string[] = await invoke('list_zk_plugins');
      setPlugins(result);
    } catch (e) {
      toast.error("Failed to fetch ZK plugins");
    }
  };

  const handleToggleDarkfi = async (enabled: boolean) => {
    try {
      await invoke('toggle_darkfi', { enabled });
      setDarkfiEnabled(enabled);
      if (enabled) fetchPlugins();
    } catch (e) {
      toast.error("Failed to toggle DarkFi mode");
    }
  };

  const loadPlugin = async (id: string) => {
    setLoading(true);
    try {
      const circuit: any = await invoke('load_zk_plugin', { pluginId: id });
      setSelectedPlugin(circuit);
      toast.success(`Loaded circuit: ${id}`);
    } catch (e) {
      toast.error(`Error loading plugin: ${e}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (darkfiEnabled) {
      fetchPlugins();
    }
  }, [darkfiEnabled]);

  return (
    <div className="p-6 space-y-6 max-w-4xl mx-auto">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">ZK-Plugin Manager</h1>
          <p className="text-slate-400">Manage sovereign ZK-circuits and DarkFi integration</p>
        </div>
        
        <div className="flex items-center gap-3 p-4 rounded-xl bg-slate-900 border border-slate-800">
          <Label htmlFor="darkfi-toggle" className="text-slate-300 font-medium">Sovereign Mode</Label>
          <Switch 
            id="darkfi-toggle" 
            checked={darkfiEnabled} 
            onCheckedChange={handleToggleDarkfi} 
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="bg-slate-900 border-slate-800 text-white">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Cpu className="w-5 h-5 text-blue-400" />
              Available Circuits
            </CardTitle>
            <CardDescription className="text-slate-500">
              Detected .zk files in the sovereign plugins directory
            </CardDescription>
          </CardHeader>
          <CardContent>
            {!darkfiEnabled ? (
              <div className="text-center py-10 text-slate-500 italic">
                Enable Sovereign Mode to discover plugins
              </div>
            ) : plugins.length === 0 ? (
              <div className="text-center py-10 text-slate-500 italic">
                No circuits found in /plugins directory
              </div>
            ) : (
              <div className="space-y-3">
                {plugins.map(id => (
                  <div key={id} className="flex items-center justify-between p-3 rounded-lg bg-slate-800 border border-slate-700 hover:border-blue-500 transition-colors group">
                    <div className="flex items-center gap-3">
                      <FileCheck className="w-4 h-4 text-slate-400 group-hover:text-blue-400" />
                      <span className="font-mono text-sm">{id}</span>
                    </div>
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      onClick={() => loadPlugin(id)}
                      disabled={loading}
                    >
                      {loading ? <Loader2 className="w-3 h-3 animate-spin" /> : 'Load'}
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800 text-white">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ShieldAlert className="w-5 h-5 text-purple-400" />
              Circuit Inspector
            </CardTitle>
            <CardDescription className="text-slate-500">
              Technical metadata for the currently loaded ZK-circuit
            </CardDescription>
          </CardHeader>
          <CardContent>
            {!selectedPlugin ? (
              <div className="text-center py-10 text-slate-500 italic">
                Select a circuit to inspect its binary structure
              </div>
            ) : (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-3 rounded-lg bg-slate-800 border border-slate-700">
                    <div className="text-[10px] uppercase text-slate-500 font-bold">Circuit ID</div>
                    <div className="text-sm font-mono">{selectedPlugin.id}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-slate-800 border border-slate-700">
                    <div className="text-[10px] uppercase text-slate-500 font-bold">Version</div>
                    <div className="text-sm font-mono">{selectedPlugin.version}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-slate-800 border border-slate-700">
                    <div className="text-[10px] uppercase text-slate-500 font-bold">Public Inputs</div>
                    <div className="text-sm font-mono">{selectedPlugin.public_input_count}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-slate-800 border border-slate-700">
                    <div className="text-[10px] uppercase text-slate-500 font-bold">Witnesses</div>
                    <div className="text-sm font-mono">{selectedPlugin.witness_count}</div>
                  </div>
                </div>
                <div className="p-3 rounded-lg bg-slate-800 border border-slate-700">
                  <div className="text-[10px] uppercase text-slate-500 font-bold mb-2">Bytecode (SAMPLED)</div>
                  <div className="text-xs font-mono text-blue-300 break-all line-clamp-3">
                    {Array.from(selectedPlugin.bytecode).map((b: any) => b.toString(16).padStart(2, '0')).join(' ')}
                  </div>
                </div>
                <div className="flex justify-end">
                  <Badge variant="outline" className="text-blue-400 border-blue-400/30">
                    Bincode Verified
                  </Badge>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
