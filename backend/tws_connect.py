from ib_async import *

def get_order_details(order_id):
    """
    Retrieve and display details of an order using its ID.
 
    Args:
        order_id: The ID of the order to look up
    """
    # Get all open orders with their trade objects
    trades = ib.trades()
    print(f"Total trades: {len(trades)}")
    print(trades)
 
    # Search for the specific order
    for trade in trades:
        if trade.order.orderId == order_id:
            order = trade.order
            order_status = trade.orderStatus
 
            print("\nOrder Details:")
            print("-------------")
            print(f"Order ID: {order.orderId}")
            print(f"Status: {order_status.status}")
            print(f"Action: {order.action}")
            print(f"Quantity: {order.totalQuantity}")
            print(f"Order Type: {order.orderType}")
 
            if hasattr(order, 'lmtPrice') and order.lmtPrice:
                print(f"Limit Price: {order.lmtPrice}")
            if hasattr(order, 'auxPrice') and order.auxPrice:
                print(f"Stop Price: {order.auxPrice}")
 
            print(f"Time in Force: {order.tif}")
            print(f"Account: {order.account}")
            print(f"Filled: {order_status.filled}")
            print(f"Remaining: {order_status.remaining}")
            return trade
 
    print(f"No order found with ID: {order_id}")
    return None

def check_order_status(trade, contract, max_attempts=10, delay=1):
    """
    Check the status of an order and print detailed information.
    
    Args:
        trade: The trade object returned by placeOrder
        contract: The contract object
        max_attempts: Maximum number of times to check the status
        delay: Delay between checks in seconds
    """
    # Get current market data
    ticker = ib.reqMktData(contract)
    ib.sleep(1)  # Wait for market data
    
    for attempt in range(max_attempts):
        status = trade.orderStatus.status
        filled = trade.orderStatus.filled
        remaining = trade.orderStatus.remaining
        avg_fill_price = trade.orderStatus.avgFillPrice
        limit_price = trade.order.lmtPrice
 
        print(f"\nOrder Status Check {attempt + 1}/{max_attempts}:")
        print(f"Status: {status}")
        print(f"Limit Price: {limit_price}")
        print(f"Current Market Price: {ticker.marketPrice()}")
        print(f"Filled: {filled}")
        print(f"Remaining: {remaining}")
        print(f"Average Fill Price: {avg_fill_price}")
 
        if status in ['Filled', 'Cancelled', 'Inactive']:
            print("\nOrder processing complete!")
            return
 
        ib.sleep(delay)
 
    print("\nMaximum status checks reached. Order may still be processing.")

# Connect to TWS
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=121)

# Optional: request delayed/free market data
ib.reqMarketDataType(4)

# ✅ Correct stock contract (not Forex)
contract = Stock('AAPL', 'SMART', 'USD')

# ✅ Create a limit order (LMT), price = 180.00
order = LimitOrder('BUY', 200, 280.00)

# Place the order
# trade = ib.placeOrder(contract, order)

# Print initial order status
# print(f"🛒 Limit Order placed: {trade}")

# Print order status
# print(f"⌛ Order status: {trade.orderStatus.status}")
# print(f"✅ Filled: {trade.orderStatus.filled}")
# print(f"Order ID: {trade.order.orderId}")
get_order_details(36)

# check_order_status(trade, contract)



