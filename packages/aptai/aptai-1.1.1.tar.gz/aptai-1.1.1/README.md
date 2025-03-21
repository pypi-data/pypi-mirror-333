
# AptAI: AI-Powered DeFi & NFT Toolkit for Aptos

AptAI is a powerful Python library that merges AI capabilities with Aptos blockchain functionality, delivering seamless DeFi operations, NFT management, and real-time price tracking—all in one package. Built by Teck, AptAI simplifies complex blockchain interactions while leveraging AI for enhanced analytics and automation.

## ✨ Key Features

### 🔹 Real-Time Price Tracking
- Fetch live token prices from DexScreener
- Monitor Liquidswap pools for accurate token pricing
- Historical price data analysis
- Gas price predictions
- Market volatility tracking

### 🔹 NFT Management Made Simple
- Multi-marketplace support: Topaz, Souffl3, Bluemove
- Track NFT floor prices and volumes
- Monitor ownership & transfers across wallets
- Real-time collection analytics

### 🔹 Seamless DeFi Operations
- DEX pair analytics and tracking
- Track liquidity pools and volumes
- Monitor wallet risk levels
- Token distribution analysis
- Smart contract security audits

### 🔹 AI-Powered Features
- Built-in Groq LLM integration for smart analysis
- AI chatbot for blockchain queries
- Market trend predictions
- Contract analysis and risk assessment
- Customizable AI parameters

### 🔹 Telegram Bot Integration
- Real-time price alerts
- NFT tracking commands
- AI chat functionality
- Market analysis on demand
- Security monitoring

## 🚀 Installation

```bash
pip install aptai
```

## 💡 Quick Start Guide

```python
from aptai import AptAi

# Initialize AptAi
apt_ai = AptAi()

# Get token price
price = apt_ai.get_price("aptos")

# Chat with AI
response = apt_ai.chat("Explain APT tokenomics")

# Analyze contract
analysis = apt_ai.analyze_contract("contract_address")

# Check security
security = apt_ai.get_contract_security("contract_address")

# Get DEX pairs
pairs = apt_ai.get_dex_pairs("token_address")

# Predict gas
gas = apt_ai.predict_gas_price()

# Get historical data
history = apt_ai.get_historical_prices("aptos")
```

## 📌 API Reference

### 💰 Price & Market Data
- `get_price(token)`: Fetch real-time token price
- `get_historical_prices(token)`: Get price history
- `predict_gas_price()`: Estimate gas costs
- `get_dex_pairs(token)`: List DEX trading pairs

### 🎨 NFT Operations
- `get_nft_data(address)`: Get collection stats
- `track_nft_transfers(address)`: Monitor transfers
- `get_nft_floor_price(collection)`: Track floor prices

### 🔒 Security & Analysis
- `analyze_contract(address)`: Smart contract analysis
- `get_contract_security(address)`: Security audit
- `analyze_wallet_risk(address)`: Risk assessment
- `get_token_distribution(token)`: Holder analysis

### 🧠 AI Features
- `chat(message)`: Chat with AI assistant
- `ai_analysis(query)`: Get market insights
- `analyze_market_conditions()`: Market analysis

## 👤 Author
Developed by Teck  
📧 teckdegen@gmail.com
