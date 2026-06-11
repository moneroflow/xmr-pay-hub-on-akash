import { useStore } from '@/lib/store';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Badge } from '@/components/ui/badge';
import { Slider } from '@/components/ui/slider';
import { FadeIn } from '@/components/FadeIn';
import { Copy, Check, Eye, EyeOff, Zap, Shield, ShieldCheck, Lock, Upload, Download, Server, Wifi, WifiOff, HelpCircle, Loader2, Cloud, Globe, Monitor, ChevronDown, Info, Smartphone, RefreshCw, Radio, Settings2, KeyRound, Beaker, Cpu } from 'lucide-react';
import { useState, useRef } from 'react';
import { toast } from 'sonner';
import { exportEncryptedBackup, importEncryptedBackup } from '@/lib/crypto-store';
import { testConnection, piconeroToXmr } from '@/lib/monero-rpc';
import { formatXMR } from '@/lib/mock-data';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import BrowserWalletSetup from '@/components/BrowserWalletSetup';
import RestoreWalletFromSeed from '@/components/RestoreWalletFromSeed';
import { REMOTE_NODES, findFastestNode } from '@/lib/node-manager';
import { isMerchantPro } from '@/lib/subscription';
import AdvancedWalletSetup from '@/components/AdvancedWalletSetup';
import { hashPassword } from '@/lib/hash-password';
import { zkBridge } from '@/lib/zk-bridge';

export default function SettingsPage() {
  const merchant = useStore(s => s.merchant);
  const updateMerchant = useStore(s => s.updateMerchant);
  const restoreFromBackup = useStore(s => s.restoreFromBackup);
  const deleteAccount = useStore(s => s.deleteAccount);
  const setZkStatus = useStore(s => s.setZkStatus);
  const zkStatus = useStore(s => s.zkStatus);
  const [showKey, setShowKey] = useState(false);
  const [copied, setCopied] = useState(false);
  const [restoring, setRestoring] = useState(false);
  const [testing, setTesting] = useState(false);
  const [showRpcHelp, setShowRpcHelp] = useState(false);
  const [autoSelecting, setAutoSelecting] = useState(false);
  const [showBrowserWalletSetup, setShowBrowserWalletSetup] = useState(false);
  const [showRestoreFromSeed, setShowRestoreFromSeed] = useState(false);
  const [showWalletChoice, setShowWalletChoice] = useState(false);
  const [dangerSeed, setDangerSeed] = useState('');
  const [showDangerConfirm, setShowDangerConfirm] = useState(false);
  const [showAdvancedSetup, setShowAdvancedSetup] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  // Admin password gate state
  const [adminUnlocked, setAdminUnlocked] = useState(false);
  const [showSetAdmin, setShowSetAdmin] = useState(false);
  const [showUnlockAdmin, setShowUnlockAdmin] = useState(false);
  const [adminPass, setAdminPass] = useState('');
  const [adminPassConfirm, setAdminPassConfirm] = useState('');
  const [unlockPass, setUnlockPass] = useState('');
  const [showAdminPass, setShowAdminPass] = useState(false);
  const [pendingAction, setPendingAction] = useState<(() => void) | null>(null);

  const requireAdmin = (action: () => void) => {
    if (adminUnlocked) { action(); return; }
    setPendingAction(() => action);
    if (!merchant.adminPasswordHash) {
      setShowSetAdmin(true);
    } else {
      setShowUnlockAdmin(true);
    }
  };

  const handleSetAdminAndProceed = () => {
    if (adminPass.length < 6) { toast.error('Password must be at least 6 characters'); return; }
    if (adminPass !== adminPassConfirm) { toast.error('Passwords do not match'); return; }
    updateMerchant({ adminPasswordHash: hashPassword(adminPass) });
    setShowSetAdmin(false);
    setAdminPass('');
    setAdminPassConfirm('');
    setAdminUnlocked(true);
    toast.success('Admin password set! 🔒');
    if (pendingAction) { pendingAction(); setPendingAction(null); }
  };

  const handleUnlockAndProceed = () => {
    if (hashPassword(unlockPass) === merchant.adminPasswordHash) {
      setAdminUnlocked(true);
      setShowUnlockAdmin(false);
      setUnlockPass('');
      toast.success('Admin unlocked');
      if (pendingAction) { pendingAction(); setPendingAction(null); }
    } else {
      toast.error('Wrong admin password');
    }
  };

  const copyKey = () => {
    navigator.clipboard.writeText(merchant.apiKey);
    setCopied(true);
    toast.success('API key copied!');
    setTimeout(() => setCopied(false), 2000);
  };

  const handleExportBackup = async () => {
    if (!merchant.privacyPassphrase) { toast.error('Set a passphrase first'); return; }
    try {
      const state = useStore.getState();
      const data = JSON.stringify({
        merchant: state.merchant,
        invoices: state.invoices,
        subscriptions: state.subscriptions,
        paymentLinks: state.paymentLinks,
        referrals: state.referrals,
        referralPayouts: state.referralPayouts,
        isAuthenticated: state.isAuthenticated,
        timestamp: new Date().toISOString(),
        version: '2.0',
      });
      const blob = await exportEncryptedBackup(data, merchant.privacyPassphrase);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = `moneroflow-backup-${Date.now()}.json.aes`; a.click();
      URL.revokeObjectURL(url);
      toast.success('Encrypted backup downloaded!');
    } catch { toast.error('Backup export failed'); }
  };

  const handleRestoreBackup = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !merchant.privacyPassphrase) { toast.error('Select a file and ensure passphrase is set'); return; }
    setRestoring(true);
    try {
      const json = await importEncryptedBackup(file, merchant.privacyPassphrase);
      const parsed = JSON.parse(json);
      restoreFromBackup(parsed);
      toast.success(`Backup restored successfully! ${parsed.invoices?.length || 0} invoices recovered.`);
    } catch { toast.error('Restore failed — wrong passphrase or corrupted file'); }
    setRestoring(false);
  };

  const handleTestConnection = async () => {
    setTesting(true);
    try {
      const endpoint = merchant.walletMode === 'remote'
        ? `http://${merchant.remoteNodeUrl}`
        : merchant.rpcEndpoint;
      const result = await testConnection({
        endpoint,
        username: merchant.rpcUsername,
        password: merchant.rpcPassword,
        walletFilename: merchant.rpcWalletFilename,
      });
      if (result.success && result.balance) {
        updateMerchant({ rpcConnected: true });
        toast.success(`Connected! Balance: ${formatXMR(piconeroToXmr(result.balance.unlockedBalance))}`);
      } else {
        updateMerchant({ rpcConnected: false });
        toast.error(result.error || 'Connection failed');
      }
    } catch {
      updateMerchant({ rpcConnected: false });
      toast.error('RPC connection failed — check your wallet is running');
    }
    setTesting(false);
  };

  const handleAutoSelectNode = async () => {
    setAutoSelecting(true);
    try {
      const result = await findFastestNode();
      if (result) {
        updateMerchant({ remoteNodeUrl: result.node.url, remoteNodeSsl: result.node.ssl });
        toast.success(`Selected fastest node: ${result.status.label} (${result.status.latencyMs}ms)`);
      } else {
        toast.error('Could not connect to any remote node');
      }
    } catch {
      toast.error('Node test failed');
    }
    setAutoSelecting(false);
  };

  const handleZkTest = async () => {
    setZkStatus('generating');
    try {
      const response = await zkBridge.generateProof({
        proof_type: 'proof_of_balance',
        params: { threshold: '100XMR' },
      });
      
      // Simulate the network delay of verification
      await new Promise(resolve => setTimeout(resolve, 1200));
      
      const isVerified = await zkBridge.verifyProof(response.proof, response.public_inputs);
      if (isVerified) {
        setZkStatus('verified');
        toast.success('ZK-Proof Verified! Trustless balance proven.');
      } else {
        setZkStatus('error');
        toast.error('ZK-Proof verification failed');
      }
    } catch (e) {
      setZkStatus('error');
      toast.error('ZK-Engine error: ' + (e instanceof Error ? e.message : 'Unknown error'));
    }
  };

  const walletMode = merchant.walletMode || 'viewonly';
  const isPro = isMerchantPro(merchant);

  const setWalletMode = (mode: 'selfcustody' | 'viewonly') => {
    if (mode === 'viewonly') {
      if (!merchant.viewOnlySetupComplete) {
        setShowWalletChoice(true);
        return;
      }
      updateMerchant({
        walletMode: mode,
        nativeRpcEnabled: false,
        rpcConnected: true,
      });
      return;
    }
    updateMerchant({
      walletMode: mode,
      nativeRpcEnabled: true,
      rpcConnected: merchant.rpcConnected,
    });
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <FadeIn>
        <h1 className="text-2xl font-bold text-foreground">Settings</h1>
        <p className="text-muted-foreground text-sm">Configure your merchant account</p>
      </FadeIn>

      {/* Wallet Mode Selection */}
      <FadeIn delay={0.02}>
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Server className="w-5 h-5 text-primary" />
            <h2 className="text-lg font-semibold text-foreground">Wallet & Node</h2>
            <Dialog open={showRpcHelp} onOpenChange={setShowRpcHelp}>
              <DialogTrigger asChild>
                <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-primary h-8 px-2">
                  <HelpCircle className="w-4 h-4" />
                </Button>
              </DialogTrigger>
              <DialogContent className="bg-card border-border max-w-lg max-h-[90vh] overflow-y-auto">
                <DialogHeader><DialogTitle className="text-foreground">How to run monero-wallet-rpc</DialogTitle></DialogHeader>
                <div className="space-y-3 text-sm text-muted-foreground">
                  <p>Run the following command to start your own wallet RPC server:</p>
                  <pre className="bg-background border border-border rounded-lg p-3 text-xs font-mono text-foreground overflow-x-auto whitespace-pre-wrap">
{`monero-wallet-rpc \\\\
  --rpc-bind-port 18082 \\\\
  --rpc-login monero:yourpassword \\\\
  --wallet-dir /path/to/wallets \\\\
  --daemon-address node.moneroworld.com:18089 \\\\
  --disable-rpc-ban`}
                  </pre>
                  <div className="space-y-2 pt-2">
                    <p className="text-foreground font-medium">Required flags:</p>
                    <ul className="list-disc list-inside space-y-1 text-xs">
                      <li><code className="text-primary">--rpc-bind-port</code> — Port for RPC (default: 18082)</li>
                      <li><code className="text-primary">--rpc-login</code> — Username:password for auth</li>
                      <li><code className="text-primary">--wallet-dir</code> — Directory containing wallet files</li>
                      <li><code className="text-primary">--daemon-address</code> — Monero node to connect to</li>
                    </ul>
                  </div>
                  <div className="pt-2 border-t border-border">
                    <p className="text-xs">⚠️ CORS: If testing locally, add <code className="text-primary">--rpc-access-control-origins=*</code></p>
                    <p className="text-xs mt-1">In production, RPC calls go through server-side API routes — never expose credentials to the browser.</p>
                  </div>
                </div>
              </DialogContent>
            </Dialog>
          </div>
          <p className="text-xs text-muted-foreground">Choose how XMRPay connects to the Monero network.</p>

          <div className="grid gap-3">
            <button
              onClick={() => setWalletMode('viewonly')}
              className={`w-full text-left p-5 rounded-xl border-2 transition-all ${
                walletMode === 'viewonly'
                  ? 'border-primary bg-primary/5'
                  : 'border-border bg-card hover:border-muted-foreground/30'
              }`}
            >
              <div className="flex items-start gap-4">
                <div className={`mt-0.5 p-2.5 rounded-lg ${walletMode === 'viewonly' ? 'bg-primary/10' : 'bg-muted'}`}>
                  <Smartphone className={`w-5 h-5 ${walletMode === 'viewonly' ? 'text-primary' : 'text-muted-foreground'}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-semibold text-foreground">In-Browser Wallet</span>
                    <Badge className="bg-primary/10 text-primary border-primary/20 text-[10px]">Recommended</Badge>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">Instant setup — wallet is created automatically in your browser. Self-custody with zero downloads. Works on any device.</p>
                  <Badge variant="outline" className="mt-2 text-[10px] text-muted-foreground border-border">🔐 Lightweight • Self-Custody • Max Privacy</Badge>
                </div>
                <div className={`mt-1 w-5 h-5 rounded-full border-2 flex items-center justify-center shrink-0 ${
                  walletMode === 'viewonly' ? 'border-primary' : 'border-muted-foreground/30'
                }`}>
                  {walletMode === 'viewonly' && <div className="w-2.5 h-2.5 rounded-full bg-primary" />}
                </div>
              </div>
            </button>

            <button
              onClick={() => setWalletMode('selfcustody')}
              className={`w-full text-left p-5 rounded-xl border-2 transition-all ${
                walletMode === 'selfcustody'
                  ? 'border-primary bg-primary/5'
                  : 'border-border bg-card hover:border-muted-foreground/30'
              }`}
            >
              <div className="flex items-start gap-4">
                <div className={`mt-0.5 p-2.5 rounded-lg ${walletMode === 'selfcustody' ? 'bg-primary/10' : 'bg-muted'}`}>
                  <Monitor className={`w-5 h-5 ${walletMode === 'selfcustody' ? 'text-primary' : 'text-muted-foreground'}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-semibold text-foreground">Full Self-Custody</span>
                    <Badge variant="outline" className="text-[10px] text-muted-foreground border-border">Advanced</Badge>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">Run your own monero-wallet-rpc. Full sovereignty — your node, your keys, your rules.</p>
                  <Badge variant="outline" className="mt-2 text-[10px] text-muted-foreground border-border">🔐 Advanced – Self-Custody</Badge>
                </div>
                <div className={`mt-1 w-5 h-5 rounded-full border-2 flex items-center justify-center shrink-0 ${
                  walletMode === 'selfcustody' ? 'border-primary' : 'border-muted-foreground/30'
                }`}>
                  {walletMode === 'selfcustody' && <div className="w-2.5 h-2.5 rounded-full bg-primary" />}
                </div>
              </div>
            </button>
          </div>

          <Dialog open={showBrowserWalletSetup} onOpenChange={setShowBrowserWalletSetup}>
            <DialogContent className="bg-card border-border max-w-lg max-h-[90vh] overflow-y-auto">
              <DialogHeader><DialogTitle className="text-foreground">Create Your Browser Wallet</DialogTitle></DialogHeader>
              <BrowserWalletSetup
                onComplete={() => setShowBrowserWalletSetup(false)}
                onCancel={() => setShowBrowserWalletSetup(false)}
              />
            </DialogContent>
          </Dialog>

          <Dialog open={showRestoreFromSeed} onOpenChange={setShowRestoreFromSeed}>
            <DialogContent className="bg-card border-border max-w-lg max-h-[90vh] overflow-y-auto">
              <DialogHeader><DialogTitle className="text-foreground">Restore Wallet from Seed</DialogTitle></DialogHeader>
              <RestoreWalletFromSeed
                onComplete={() => setShowRestoreFromSeed(false)}
                onCancel={() => setShowRestoreFromSeed(false)}
              />
            </DialogContent>
          </Dialog>

          <Dialog open={showWalletChoice} onOpenChange={setShowWalletChoice}>
            <DialogContent className="bg-card border-border max-w-md">
              <DialogHeader><DialogTitle className="text-foreground">Set Up Browser Wallet</DialogTitle></DialogHeader>
              <p className="text-sm text-muted-foreground">Choose how to get started:</p>
              <div className="grid gap-3 pt-2">
                <button
                  onClick={() => { setShowWalletChoice(false); setShowBrowserWalletSetup(true); }}
                  className="w-full text-left p-4 rounded-xl border-2 border-border bg-card hover:border-primary/50 transition-all"
                >
                  <div className="flex items-start gap-3">
                    <div className="p-2 rounded-lg bg-primary/10">
                      <Shield className="w-5 h-5 text-primary" />
                    </div>
                    <div className="flex-1">
                      <span className="font-semibold text-foreground text-sm">Create New Wallet</span>
                      <p className="text-xs text-muted-foreground mt-1">Generate a fresh wallet with a new seed phrase. You'll back it up once during setup.</p>
                    </div>
                  </div>
                </button>
                <button
                  onClick={() => { setShowWalletChoice(false); setShowRestoreFromSeed(true); }}
                  className="w-full text-left p-4 rounded-xl border-2 border-border bg-card hover:border-primary/50 transition-all"
                >
                  <div className="flex items-start gap-3">
                    <div className="p-2 rounded-lg bg-muted">
                      <Download className="w-5 h-5 text-muted-foreground" />
                    </div>
                    <div className="flex-1">
                      <span className="font-semibold text-foreground text-sm">Restore from Seed Phrase</span>
                      <p className="text-xs text-muted-foreground mt-1">Already have a 25-word seed? Enter it to restore your existing wallet.</p>
                    </div>
                  </div>
                </button>
              </div>
            </DialogContent>
          </Dialog>

          {walletMode === 'viewonly' && merchant.viewOnlySetupComplete && (
            <div className="p-5 rounded-xl bg-card border border-border space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-foreground">Browser Wallet</h3>
                <Badge className="bg-success/10 text-success border-success/20 text-xs">
                  <Eye className="w-3 h-3 mr-1" /> Active
                </Badge>
              </div>

              <div className="space-y-1.5">
                <label className="text-[11px] font-medium text-muted-foreground uppercase tracking-wider">Primary Address</label>
                <div className="flex items-center gap-2">
                  <p className="font-mono text-[11px] text-foreground bg-background border border-border rounded-lg p-3 flex-1 break-all leading-relaxed">{merchant.viewOnlyAddress}</p>
                  <Button variant="outline" size="icon" className="shrink-0 border-border hover:border-primary/50 h-8 w-8" onClick={() => { navigator.clipboard.writeText(merchant.viewOnlyAddress); toast.success('Address copied'); }}>
                    <Copy className="w-3.5 h-3.5" />
                  </Button>
                </div>
              </div>

              {!merchant.viewOnlySeedBackedUp && merchant.viewOnlySeedPhrase ? (
                <div className="p-4 rounded-lg bg-destructive/10 border border-destructive/30 space-y-3">
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-destructive" />
                    <p className="text-sm font-semibold text-destructive">⚠️ Back up your seed phrase NOW</p>
                  </div>
                  <p className="text-[11px] text-muted-foreground leading-relaxed">
                    Write down these 25 words in order and store them somewhere safe offline. This is the <strong className="underline">only way</strong> to recover your wallet. Once you confirm, this phrase will be hidden permanently.
                  </p>
                  {showKey ? (
                    <>
                      <div className="bg-background border border-border rounded-lg p-3">
                        <p className="font-mono text-xs text-foreground leading-relaxed break-all select-all">{merchant.viewOnlySeedPhrase}</p>
                      </div>
                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          className="border-border text-xs"
                          onClick={() => {
                            navigator.clipboard.writeText(merchant.viewOnlySeedPhrase || '');
                            toast.success('Seed phrase copied — store it safely!');
                          }}
                        >
                          <Copy className="w-3 h-3 mr-1.5" /> Copy
                        </Button>
                        <Button
                          size="sm"
                          className="bg-gradient-orange text-xs"
                          onClick={() => {
                            updateMerchant({ viewOnlySeedBackedUp: true });
                          }}
                        >
                          <ShieldCheck className="w-3 h-3 mr-1.5" /> Confirm Backed Up
                        </Button>
                      </div>
                    </>
                  ) : null}
                </div>
              ) : null}
            </div>
          )}
            </div>
          </FadeIn>

      {/* Privacy Labs - ZK Hybrid Framework Section */}
      <FadeIn delay={0.04}>
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Beaker className="w-5 h-5 text-primary" />
            <h2 className="text-lg font-semibold text-foreground">Privacy Labs <Badge variant="outline" className="ml-2 text-[10px]">BETA</Badge></h2>
          </div>
          <p className="text-xs text-muted-foreground">Experimental Zero-Knowledge (ZK) tools for trustless privacy.</p>

          <div className="grid gap-3">
            <div className="p-5 rounded-xl border-2 border-border bg-card space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Cpu className="w-5 h-5 text-primary" />
                  <div>
                    <span className="font-semibold text-foreground text-sm">ZK-Proof Engine</span>
                    <p className="text-[11px] text-muted-foreground">Generate trustless proofs of balance without revealing address.</p>
                  </div>
                </div>
                <Switch 
                  checked={true} 
                  onCheckedChange={() => {}} 
                  className="data-[state=checked]:bg-primary" 
                />
              </div>

              <div className="pt-2">
                <Button 
                  onClick={handleZkTest}
                  disabled={zkStatus === 'generating'}
                  className="w-full bg-primary hover:bg-primary/90 text-white text-xs h-9"
                >
                  {zkStatus === 'generating' ? (
                    <><Loader2 className="w-3 h-3 mr-2 animate-spin" /> Generating Proof...</>
                  ) : (
                    <>Generate Proof of Balance (&gt;100 XMR)</>
                  )}
                </Button>

                {zkStatus === 'verified' && (
                  <div className="mt-3 p-3 rounded-lg bg-success/10 border border-success/20 flex items-center gap-3">
                    <ShieldCheck className="w-4 h-4 text-success" />
                    <p className="text-xs text-success font-medium">ZK-Proof Verified: Balance requirement met trustlessly.</p>
                  </div>
                )}

                {zkStatus === 'error' && (
                  <div className="mt-3 p-3 rounded-lg bg-destructive/10 border border-destructive/20 flex items-center gap-3">
                    <ShieldAlert className="w-4 h-4 text-destructive" />
                    <p className="text-xs text-destructive font-medium">ZK-Proof failed verification.</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </FadeIn>

      {/* Other Settings (API, Backups, etc) */}
      <FadeIn delay={0.06}>
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Settings2 className="w-5 h-5 text-primary" />
            <h2 className="text-lg font-semibold text-foreground">Account & Security</h2>
          </div>

          <div className="grid gap-4">
            <div className="p-4 rounded-xl bg-card border border-border space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <KeyRound className="w-4 h-4 text-muted-foreground" />
                  <span className="text-sm font-medium text-foreground">API Access Key</span>
                </div>
                <Button variant="outline" size="sm" className="h-7 text-xs border-border" onClick={copyKey}>
                  {copied ? <Check className="w-3 h-3 mr-1" /> : <Copy className="w-3 h-3 mr-1" />}
                  {copied ? 'Copied' : 'Copy'}
                </Button>
              </div>
              <div className="flex items-center gap-2">
                <p className="font-mono text-xs text-muted-foreground bg-background border border-border rounded-lg p-2 flex-1 break-all">{merchant.apiKey}</p>
              </div>
            </div>
          </div>
        </div>
      </FadeIn>
    </div>
  );
}
