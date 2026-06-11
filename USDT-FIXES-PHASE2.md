# USDT/TRON Integration Fixes - Phase 1

## Completed (v2)

### 1. formatUSDT Function Added
**File:** `src/lib/mock-data.ts`
- Added `formatUSDT(amount)` function that returns USDT amounts
- Format: `<amount>.00 USDT` (2 decimal places for USDT, unlike XMR's 6)

### 2. InvoicePage.tsx - Full Chain Support
**File:** `src/pages/InvoicePage.tsx`

**What was fixed:**
- ✅ Detected TRX/USDT invoices via `invoice.chainType === 'trx'`
- ✅ Shows proper USDT amounts using `formatUSDT()` instead of `formatXMR()`
- ✅ Displays TRON address (`invoice.trxAddress`) instead of XMR subaddress
- ✅ Chain-aware QR code:
  - XMR: `monero:<address>?tx_amount=...`
  - USDT: TRONScan link with USDT token id
- ✅ Chain-specific color themes:
  - XMR: Purple (`text-primary`)
  - USDT: Orange (`text-orange-500`)
  - Applies TRON theme class (`theme-tron`) to entire page
  - Restores previous theme on unmount
- ✅ Chain-specific confirmations:
  - XMR: 10 confirmations
  - USDT: 19 confirmations (TRON network standard)
- ✅ Chain-specific explorer links:
  - XMR: xmrchain.net
  - USDT: tronscan.org
- ✅ Removed XMR-specific elements from USDT invoices (MoneroFeeInfo)
- ✅ Chain-specific copy address messages

**Visual improvements:**
- Background gradient matches chain color (orange for USDT, purple for XMR)
- Amount displays in chain-specific colors
- QR code QR schemes are chain-appropriate

---

## Remaining Issues to Fix

### 3. SendXmrDialog - Rename to Support Both Chains
**File:** `src/components/SendXmrDialog.tsx`

**Current issues:**
- Title says "Send XMR" - should be dynamic ("Send XMR" vs "Send USDT")
- Hardcoded to XMR addresses (95 or 106 chars)
- Displays XMR balance only
- No way to select USDT sending
- XMR fee tiers only

**Cake Wallet approach:**
- Chain selector at top of dialog
- Balance shows current chain
- Address validation matches selected chain
- Fee calculator adapts to chain

### 4. POS Page - USDT Mode Persistence Testing
**File:** `src/pages/dashboard/PosPage.tsx`

**What exists:**
- `selectedChain` state (localStorage: `pos-chain`)
- `xmrMode` state (localStorage: `pos-usdt-mode`)
- Theme switching on chain change

**Need to verify:**
- Does USDT currency toggle persist on page reload?
- Does the display show "USDT" not "A$" when USDT mode active?
- Does the title update correctly ("Tap to toggle between fiat and USDT input")?
- Theme switches to orange when TRX selected?

### 5. Overview Page - Dual Chain Stats
**File:** `src/pages/dashboard/OverviewPage.tsx`

**Current issues:**
- Only shows XMR stats
- `formatXMR()` called globally
- No chain selector or multi-chain balance display

**Cake Wallet approach:**
- Asset list with each chain's balance
- Toggle between total fiat value and individual chain breakdown
- Net worth calculation across all chains

### 6. PayPage.tsx - Verify Chain Detection
**File:** `src/pages/PayPage.tsx`

**Current state:** Already supports both chains via URL parameter `?chain=trx`
- Needs verification that USDT formatting is consistent
- Ensure mobile experience matches desktop

### 7. Send Button Text (Dashboard)
**Location:** Likely in `OverviewPage.tsx` or `SettingsPage.tsx`

**Current issue:** "SEND XMR" button should become "SEND" or chain-specific

---

## Architecture Pattern (Cake Wallet Inspired)

### State Management
```
Chain Selection (Global/POS/Invoice)
  ├─ Chain type: 'xmr' | 'trx'
  ├─ Theme: 'dark' | 'theme-tron'
  ├─ Currency formatter: formatXMR | formatUSDT
  ├─ Address validation: XMR (95/106) | TRX (34 chars)
  └─ Fee calculator: XMR tiers | TRX base fee

Per-Chain State
  ├─ Balance
  ├─ Pending transactions
  └─ History
```

### Component Hierarchy
```
App
 ├─ ChainProvider (new: context for chain state)
 │   ├─ ChainSelector (dropdown/tabs)
 │   └─ Theme application
 ├─ Dashboard
 │   ├─ Overview (multi-chain stats)
 │   ├─ SendDialog (chain-aware)
 │   └─ POS (chain toggle exists, needs testing)
 └─ InvoicePage (chain-aware - FIXED)
```

---

## Next Steps Priority

**P1 (Critical for merchant UX):**
1. Test POS page USDT persistence
2. Fix SendDialog to support both chains

**P2 (Important but less urgent):**
3. Overview page multi-chain display
4. Send button consistency

**P3 (Polish):**
5. Chain context provider for cleaner state management
6. Chain-specific fee calculators
7. Mobile wallet test

---

## Build & Deploy

Current build successful:
```
✓ built in 12.57s
dist/index.html                              1.09 kB
dist/assets/index-BSTO2ebq.css             84.23 kB
dist/assets/index-Cy3jioUJ.js           2,151.46 kB
dist/assets/index-D6NnSL8f.js           2,981.56 kB
```

Deployed to: `http://192.168.60.123:8090`

**Backup:** `backups/usdt-tron-complete-fix-20260420-234100.tar.gz`

---

## Testing Checklist

### Invoice Display (from POS or PayPage)
- [ ] XMR invoice shows purple theme, XMR amounts, XMR QR code
- [ ] USDT invoice shows orange theme, USDT amounts, TRON QR code
- [ ] Currency displays correctly: not "A$" for USDT invoices
- [ ] Explorer links work for both chains
- [ ] Theme switches when navigating between XMR and USDT invoices

### POS Interface
- [ ] USDT mode persists on page refresh
- [ ] Toggle shows correct amount (fiat vs USDT)
- [ ] TRX chain selection shows orange theme
- [ ] Create invoice uses correct chain

### Send Dialog (not implemented yet for USDT)
- [ ] Can select XMR or USDT chain
- [ ] Shows appropriate balance
- [ ] Validates address format for selected chain
- [ ] Calculates correct fees

---

## Code Patterns Established

**Chain Detection:**
```typescript
const isTrxInvoice = invoice?.chainType === 'trx' && invoice?.trxAddress;
```

**Chain Formatting:**
```typescript
const cryptoDisplay = isTrxInvoice 
  ? formatUSDT(cryptoAmount) 
  : formatXMR(cryptoAmount);
```

**Chain Theming:**
```typescript
useEffect(() => {
  const root = document.documentElement;
  if (isTrxInvoice) {
    const prev = root.classList.contains('dark') ? 'dark' : 
      Array.from(root.classList).find(c => c.startsWith('theme-')) || 'dark';
    localStorage.setItem('mf-previous-theme', prev);
    root.classList.add('theme-tron');
  } else {
    const prev = localStorage.getItem('mf-previous-theme') || 'dark';
    root.classList.remove('theme-tron');
    root.classList.add(prev.startsWith('theme-') ? prev : 'dark');
  }
}, [isTrxInvoice]);
```
