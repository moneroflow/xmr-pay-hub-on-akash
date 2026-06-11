# 🌌 XMR Pay Hub

## The Sovereign Payment Gateway
XMR Pay Hub is a high-performance, privacy-centric payment orchestration layer designed for those who refuse to compromise on financial autonomy. Built for the modern era of decentralized finance, it bridges the gap between absolute privacy (Monero) and global liquidity (USDT/TRON), providing a seamless, professional-grade checkout experience for merchants and users alike.

### 🛡️ The Ethos
In a world of increasing financial surveillance, XMR Pay Hub stands as a bastion of **financial sovereignty**. Our core philosophy is simple: **Your money is your data, and your data is your business.** 

We believe that privacy is not about having something to hide, but about having something to protect. By combining the anonymity of Monero with the versatility of TRC-20 USDT, we empower merchants to accept payments without exposing their entire financial history to the world.

---

## 🚀 Power & Capabilities

XMR Pay Hub isn't just a payment processor; it's a comprehensive financial toolkit:

- **Dual-Chain Agility:** Switch instantly between Monero (XMR) for maximum privacy and TRON (USDT) for rapid liquidity.
- **Professional POS Interface:** A dedicated Point-of-Sale terminal with dynamic currency conversion and precise decimal control for real-world retail environments.
- **Sovereign Wallet Management:** Full control over your seeds and keys. No custodial middlemen. No "frozen" accounts.
- **Advanced Analytics:** Deep insights into your payment flows, referral networks, and revenue streams without sacrificing user privacy.
- **Automated Infrastructure:** Optimized for deployment on Akash Network, ensuring your gateway is hosted on a decentralized cloud, immune to single-point-of-failure shutdowns.

---

## 🛠️ Installation & Local Setup

Get your own sovereign gateway running in minutes.

### Prerequisites
- **Docker** (installed and running)
- **Git**
- A `.env` file configured with your RPC endpoints and API keys (optional — used only to increase rate limits for high-volume Tron/USDT transactions via TronGrid).

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/moneroflow/xmr-pay-hub-on-akash.git
   cd xmr-pay-hub-on-akash
   ```

2. **(Optional) High-Performance API Configuration**
   The hub works out-of-the-box using public blockchain nodes. However, if you are running a high-volume merchant store and experience rate-limiting, you can optionally add a TronGrid API key to increase stability:
   ```bash
   cp .env.example .env
   nano .env # Add your VITE_TRONGRID_API_KEY here
   ```
   *Note: This is entirely optional. Most users will not need to perform this step.*

3. **Build and Run with Docker**
   ```bash
   # Build the production image
   docker build -t xmr-pay-hub .

   # Run the container
   docker run -d -p 8090:80 --name xmr-pay-hub --env-file .env xmr-pay-hub
   ```

4. **Access the Hub**
   Open your browser and navigate to: `http://localhost:8090`

---

## 🌐 Deployment on Akash
For those seeking true decentralization, XMR Pay Hub is optimized for the **Akash Network**. By deploying via the provided `deploy.yaml`, you ensure your payment infrastructure is distributed across a peer-to-peer cloud, further enhancing the resilience and anonymity of your operation.

**Privacy is a right, not a privilege. Welcome to the future of payments.**
