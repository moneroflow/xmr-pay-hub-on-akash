import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { ShieldCheck, Loader2, AlertTriangle, CheckCircle2, Lock } from 'lucide-react';
import { toast } from 'sonner';
import { useStore } from '@/lib/store';
import { restoreWalletFromSeed } from '@/lib/wallet-generator';
import { REMOTE_NODES } from '@/lib/node-manager';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface Props {
  onComplete: () => void;
  onCancel: () => void;
}

export default function RestoreWalletFromSeed({ onComplete, onCancel }: Props) {
  const updateMerchant = useStore(s => s.updateMerchant);
  const loadSeed = useStore(s => s.loadSeed);
  const autoConnectNode = useStore(s => s.autoConnectNode);

  const [seedInput, setSeedInput] = useState('');
  const [passphrase, setPassphrase] = useState('');
  const [restoring, setRestoring] = useState(false);
  const [error, setError] = useState('');

  const wordCount = seedInput.trim().split(/\\s+/).filter(Boolean).length;
  const isValid = wordCount === 25;

  const handleRestore = async () => {
    if (!passphrase) {
      toast.error('Please enter your encryption passphrase');
      return;
    }

    setRestoring(true);
    setError('');
    try {
      // Verify the seed is actually decryptable and exists on native storage first
      // or if we are importing a fresh seed, we should essentially "save" it to a new slot.
      // Since this is 'Restore', we'll assume the user is providing a seed that needs to be stored securely.
      
      const wallet = restoreWalletFromSeed(seedInput);

      // Securely save the seed to native storage using the passphrase
      // We reuse the saveSeed logic to ensure the restored seed is also encrypted
      const saveSeedTauri = useStore.getState().saveSeed;
      await saveSeedTauri(wallet.seedPhrase, passphrase);

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
        privacyPassphrase: passphrase,
      });

      const status = await autoConnectNode();
      if (status?.connected) {
        toast.success('Wallet restored! Connected to ' + (status.label || 'remote node'));
      } else {
        toast.success('Wallet restored! Connecting to network...');
      }

      onComplete();
    } catch (e: any) {
      setError(e.message || 'Invalid seed phrase');
      toast.error(e.message || 'Could not restore wallet');
    }
    setRestoring(false);
  };

  return (
    <div className="space-y-5">
      <div className="p-4 rounded-xl bg-primary/5 border border-primary/20">
        <div className="flex items-start gap-3">
          <ShieldCheck className="w-5 h-5 text-primary mt-0.5 shrink-0" />
          <div className="flex-1">
            <p className="text-sm font-semibold text-foreground">Restore from Seed Phrase</p>
            <p className="text-xs text-muted-foreground mt-1">
              Enter your 25-word Monero seed phrase to restore your wallet. Your keys never leave your browser.
            </p>
          </div>
        </div>
      </div>

      <div className="space-y-2">
        <Label className="text-xs font-medium text-foreground">Seed Phrase (25 words)</Label>
        <Textarea
          value={seedInput}
          onChange={(e) => { setSeedInput(e.target.value); setError(''); }}
          className="bg-background border-border font-mono text-sm min-h-[120px] resize-none"
          placeholder="Enter your 25-word seed phrase, separated by spaces..."
        />
        <div className="flex items-center justify-between">
          <span className={`text-xs ${isValid ? 'text-success' : 'text-muted-foreground'}`}>
            {wordCount}/25 words
          </span>
          {isValid && (
            <Badge className="bg-success/10 text-success border-success/20 text-[10px]">
              <CheckCircle2 className="w-3 h-3 mr-1" /> Ready
            </Badge>
          )}
        </div>
      </div>

      {/* Passphrase Section */}
      <div className="p-4 rounded-xl bg-card border border-border space-y-3">
        <div className="flex items-center gap-2 mb-1">
          <Lock className="w-4 h-4 text-primary" />
          <span className="text-sm font-semibold text-foreground">Secure Restoration</span>
        </div>
        <p className="text-xs text-muted-foreground">
          Enter a passphrase to encrypt this restored wallet on your device.
        </p>
        <div className="space-y-2">
          <Label htmlFor="restore-passphrase" className="text-xs text-muted-foreground">Encryption Passphrase</Label>
          <Input 
            id="restore-passphrase"
            type="password" 
            value={passphrase} 
            onChange={(e) => setPassphrase(e.target.value)} 
            placeholder="Strong password..."
            className="bg-background border-border text-sm"
          />
        </div>
      </div>

      {error && (
        <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/30">
          <p className="text-xs text-destructive flex items-center gap-2">
            <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
            {error}
          </p>
        </div>
      )}

      <div className="flex justify-between pt-1">
        <Button variant="ghost" onClick={onCancel} className="text-muted-foreground text-sm">Cancel</Button>
        <Button onClick={handleRestore} disabled={!isValid || restoring} className="bg-gradient-orange hover:opacity-90">
          {restoring ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <ShieldCheck className="w-4 h-4 mr-2" />}
          {restoring ? 'Restoring...' : 'Restore Wallet'}
        </Button>
      </div>
    </div>
  );
}
