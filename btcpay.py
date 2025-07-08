from btcpay import BTCPayClient
import config

client = BTCPayClient(host=config.BTCPAY_HOST, api_key=config.BTCPAY_API_KEY)

def create_invoice(price, order_id):
    invoice = client.create_invoice(
        store_id=config.BTCPAY_STORE_ID,
        price=price,
        currency="EUR",
        metadata={"orderId": order_id}
    )
    return invoice["checkoutLink"]