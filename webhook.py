from flask import Flask, request
import hmac, hashlib
import config
import sqlite3

app = Flask(__name__)

@app.route("/btcpay_webhook", methods=["POST"])
def webhook():
    raw = request.data
    sig = request.headers.get("BTCPay-Sig")
    expected = hmac.new(config.WEBHOOK_SECRET.encode(), raw, hashlib.sha256).hexdigest()
    if sig != expected:
        return "Invalid signature", 400
    data = request.json
    if data.get("type") == "InvoiceSettled":
        metadata = data["data"].get("metadata", {})
        order_id = metadata.get("orderId")
        conn = sqlite3.connect("shop.db")
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM orders WHERE id = ?", (order_id,))
        row = cur.fetchone()
        if row:
            user_id = row[0]
            cur.execute("UPDATE users SET balance = balance + (SELECT price FROM product_options WHERE id = (SELECT option_id FROM orders WHERE id = ?)) WHERE id = ?", (order_id, user_id))
            cur.execute("UPDATE orders SET status = 'paid' WHERE id = ?", (order_id,))
            conn.commit()
    return "OK", 200