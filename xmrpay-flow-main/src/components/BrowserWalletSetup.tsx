import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Badge } from '@/components/ui/badge';
import { Copy, Download, ShieldAlert, CheckCircle2, Loader2, Lock } from 'lucide-react';
import { toast } from 'sonner';
import { useStore } from '@/lib/store';
import { generateBrowserWallet, type GeneratedWallet } from '@/lib/wallet-generator';
import { REMOTE_NODES } from '@/lib/node-manager';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { hashPassword } from '@/lib/hash-password';

interface Props {
  onComplete: () => void;
  onCancel: () => void;
}

export default function BrowserWalletSetup({ onComplete, onCancel }: Props) {
  const updateMerchant = useStore(s => s.updateMerchant);
  const saveSeed = useStore(s => s.saveSeed);
  const autoConnectNode = useStore(s => s.autoConnectNode);
  const merchant = useStore(s => s.merchant);

  const [wallet, setWallet] = useState<GeneratedWallet | null>(null);
  const [confirmed, setConfirmed] = useState(false);
  const [saving, setSaving] = useState(false);
  const [copied, setCopied] = useState(false);
  const [adminPass, setAdminPass] = useState('');

  // Auto-generate on first render
  if (!wallet) {
    const w = generateBrowserWallet();
    setWallet(w);
  }

  if (!wallet) return null;

  const allKeys = `=== XMRPay Browser Wallet Backup ===
Date: ${new Date().toISOString()}

SEED PHRASE (25 words):
${wallet.seedPhrase}

PRIMARY ADDRESS:
${wallet.address}

PRIVATE VIEW KEY:
${wallet.viewKey}

⚠️ KEEP THIS FILE SECURE. Anyone with your seed phrase can access your funds.
`;

  const handleCopyAll = () => {
    navigator.clipboard.writeText(allKeys);
    setCopied(true);
    toast.success('All keys copied to clipboard');
    setTimeout(() => setCopied(false), 3000);
  };

  const handleDownload = () => {
    const blob = new Blob([allKeys], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `xmrpay-wallet-backup-${Date.now()}.txt`; a.click();
    URL.revokeObjectURL(url);
    toast.success('Backup file downloaded');
  };

  const handleConfirm = async () => {
    if (adminPass.length < 6) {
      toast.error('Admin password must be at least 6 characters for security');
      return;
    }

    setSaving(true);
    try {
      // 1. Encrypt the seed using the Admin Password as the Master Key
      await saveSeed(wallet.seedPhrase, adminPass);

      // 2. Set up the wallet and the admin security hash
      updateMerchant({
        walletMode: 'viewonly',
        viewOnlyAddress: wallet.address,
        viewOnlyViewKey: wallet.viewKey,
        viewOnlySpendKey: wallet.spendKey,
        viewOnlyPublicSpendKey: wallet.publicSpendKey,
        viewOnlyPublicViewKey: wallet.publicViewKey,
        viewOnlySeedPhrase: wallet.seedPhrase,
        viewOnlySeedBackedUp: true,
        viewOnlyRestoreHeight: 0,
        viewOnlyNodeUrl: REMOTE_NODES[0].url,
        viewOnlySetupComplete: true,
        viewOnlySubaddressIndex: 1,
        nodeStatus: 'connecting',
        privacyPassphrase: adminPass, // Used for backup/encryption logic
        adminPasswordHash: hashPassword(adminPass), // Used for UI admin gate
      });

      // Auto-connect to the fastest node
      const status = await autoConnectNode();
      if (status?.connected) {
        toast.success('Wallet ready! Connected to ' + (status.label || 'remote node'));
      } else {
        toast.success('Wallet created! Connecting to network...');
      }

      onComplete();
    } catch (e) {
      toast.error('Failed to secure wallet: ' + (e instanceof Error ? e.message : 'Unknown error'));
    }
    setSaving(false);
  };

  return (
    <div className="space-y-5">
      {/* Warning banner */}
      <div className="p-4 rounded-xl bg-destructive/10 border border-destructive/30">
        <div className="flex items-start gap-3">
          <ShieldAlert className="w-5 h-5 text-destructive mt-0.5 shrink-0" />
          <div className="flex-1">
            <p className="text-sm font-semibold text-destructive">Back Up Your Wallet Now</p>
            <p className="text-xs text-destructive/80 mt-1">
              This information is shown <strong className="underline">ONLY ONCE</strong>. Write it down or save it securely. If you lose it, you cannot recover this wallet.
            </p>
          </div>
        </div>
      </div>

      {/* Seed phrase */}
      <div className="space-y-2">
        <label className="text-xs font-medium text-foreground">Seed Phrase (25 words)</label>
        <div className="p-4 rounded-xl bg-background border border-border">
          <div className="grid grid-cols-3 sm:grid-cols-5 gap-2">
            {wallet.seedPhrase.split(' ').map((word, i) => (
              <div key={i} className="flex items-center gap-1.5 text-sm">
                <span className="text-muted-foreground text-[10px] w-4 text-right">{i + 1}.</span>
                <span className="font-mono font-medium text-foreground">{word}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Address */}
      <div className="space-y-1.5">
        <label className="text-xs font-medium text-foreground">Primary Address</label>
        <p className="font-mono text-[11px] text-muted-foreground bg-background border border-border rounded-lg p-3 break-all leading-relaxed">
          {wallet.address}
        </p>
      </div>

      {/* View Key */}
      <div className="space-y-1.5">
        <label className="text-xs font-medium text-foreground">Private View Key</label>
        <p className="font-mono text-[11px] text-muted-foreground bg-background border border-border rounded-lg p-3 break-all leading-relaxed">
          {wallet.viewKey}
        </p>
      </div>

      {/* Action buttons */}
      <div className="flex gap-2">
        <Button variant="outline" size="sm" onClick={handleCopyAll} className="flex-1 border-border hover:border-primary/50 text-xs">
          {copied ? <CheckCircle2 className="w-3.5 h-3.5 mr-1.5 text-primary" /> : <Copy className="w-3.5 h-3.5 mr-1.5" />}\n          {copied ? 'Copied!' : 'Copy All Keys'}
        </Button>
        <Button variant="outline" size="sm" onClick={handleDownload} className="flex-1 border-border hover:border-primary/50 text-xs">
          <Download className="w-3.5 h-3.5 mr-1.5" /> Download .txt
        </Button>
      </div>

      {/* Unified Security Password Section */}
      <div className="p-4 rounded-xl bg-card border border-border space-y-3">
        <div className="flex items-center gap-2 mb-1">
          <Lock className="w-4 h-4 text-primary" />
          <span className="text-sm font-semibold text-foreground">Admin & Security Password</span>
        </div>
        <p className="text-xs text-muted-foreground">
          This password serves two critical purposes:
          <ul className="list-disc list-inside mt-1 space-y-1">
            <li><strong className="text-foreground">Device Encryption:</strong> It encrypts your wallet seed on this machine's native storage.</li>
            <li><strong className="text-foreground">Admin Access:</strong> It is required to change API keys or manage account security.</li>
          </ul>
        </p>
        <div className="space-y-2">
          <Label htmlFor="adminPass" className="text-xs text-muted-foreground">Create Master Password</Label>
          <Input 
            id="adminPass"
            type="password" 
            value={adminPass} 
            onChange={(e) => setAdminPass(e.target.value)} 
            placeholder="Min 6 characters..."
            className="bg-background border-border text-sm"
          />
        </div>
      </div>

      {/* Confirmation checkbox */}
      <div className="flex items-start gap-3 p-4 rounded-xl bg-card border border-border">
        <Checkbox id="confirm-backup" checked={confirmed} onCheckedChange={(v) => setConfirmed(!!v)} className="mt-0.5" />
        <label htmlFor="confirm-backup" className="text-sm text-foreground cursor-pointer leading-relaxed">
          I have safely backed up my seed phrase, address, and view key. I understand this cannot be shown again.
        </label>
      </div>

      {/* Footer buttons */}
      <div className="flex justify-between pt-1">
        <Button variant="ghost" onClick={onCancel} className="text-muted-foreground text-sm">Cancel</Button>
        <Button onClick={handleConfirm} disabled={!confirmed || saving} className="bg-gradient-orange hover:opacity-90">
          {saving ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <CheckCircle2 className="w-4 h-4 mr-2" />}\n          {saving ? 'Securing...' : 'I Have Saved My Backup'}
        </Button>
      </div>
    </div>
  );
}
