# Telegram Crypto Shop Bot

## Features
- Dynamic city → product → amount catalog
- Self-hosted crypto top-up using BTCPay Server
- Balance and purchase tracking

## Setup
1. Clone the repo
2. Edit a `.env` file with:
   ```
   API_TOKEN=your_telegram_token
   BTCPAY_HOST=https://your.btcpay.server
   BTCPAY_API_KEY=your_api_key
   BTCPAY_STORE_ID=store_id_here
   ```
3. Run the bot:
   ```bash
   python bot.py
   ```

## TODO
- Implement full catalog navigation
- Add crypto webhook handling
- Admin panel for adding/editing products