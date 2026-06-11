# TRX/USDT Integration Plan (April 20, 2026)

## Status
- Building has errors due to SettingsPage.tsx syntax issues
- Need to restore working state before proceeding
- Current TRX backend is complete (TronClient, TronPaymentManager, store)

## Build Fix Status
✅ SettingsPage.tsx restored from backup
- WIP due to earlier Python script error
- Reverted to last known stable state

## TRX/USDT Integration Requirements

### Scope
- Use internal self-custody TRX wallet (TronAddress from merchant)
- Support TRC-20 USDT payments
- Avoid redesigning Monero flow - duplicate the pattern for TRX

### Key Components Needed

1. **POS Terminal Toggle (PosPage.tsx)**
   - Add XMR/TRX toggle switch in header (top-right)
   - Switch between XMR and TRX/USDT payment flows
   - Update UI based on selected chain

2. **Payment Link Creation (PaymentLinksPage.tsx)**
   - Already has chain selector ✅
   - Need to ensure TRX option generates TRX/USDT links
   - Separate QR codes for XMR vs TRX/USDT

3. **USD-to-USDT Conversion**
   - Add USDT price tracking (TRC-20)
   - USD → USDT conversion (1:1 usually, but track market rate)
   - Display USDT amount in checkout

4. **TRX/USDT Payment Flow (PayPage.tsx)**
   - Detect `?chain=trx` parameter
   - Display TRX TronQRCode component ✅
   - Show USDT amount (not TRX) for customer
   - Payment monitoring via TrxPaymentProgress ✅

5. **Data Model Updates**
   - Invoice records need chainType field ✅
   - Invoice amounts: fiat + usdtAmount field
   - Store USDT price at time of invoice

## Implementation Priority

### Phase 1: Build Fix (Immediate)
- Restore SettingsPage.tsx to working state
- Remove broken helper functions
- Test build succeeds
- Deploy to port 8090

### Phase 2: POS Terminal Toggle
- Add toggle component in PosPage.tsx
- State: `selectedChain: 'xmr' | 'trx'`
- Update payment flow based on selection

### Phase 3: USDT Conversion
- Add USDT price to currency-service.ts
- Add `usdToUsdt()` function
- Display USDT amounts in POS

### Phase 4: PayPage USDT Display
- Show "TRON (USDT)" branding
- Display USDT amount in checkout
- Use existing TrxPaymentProgress for monitoring

## Technical Notes

- TRC-20 USDT contract: TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t
- Internal wallet: merchant.tronAddress
- Confirmations: 19 for TRX
- 1 USDT = 1 USD (pegged), but track market price

## Files to Modify

1. `src/pages/dashboard/PosPage.tsx` - Add chain toggle
2. `src/lib/currency-service.ts` - Add USDT price
3. `src/pages/PayPage.tsx` - Show USDT branding/amount
4. `src/lib/store.ts` - Add invoice.price fields if needed

## Next Steps

Once build is fixed:
1. Create incremental backup
2. Implement POS toggle
3. Test XMR flow still works
4. Test TRX/USDT flow
5. Deploy

## Current Blocker

Build error on SettingsPage.tsx due to earlier script issues. Need to:
1. Restore SettingsPage.tsx to stable version
2. Remove broken `safeCopyToClipboard` code
3. Test build
4. Only then proceed with TRX integration
