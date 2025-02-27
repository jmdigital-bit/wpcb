from flask import Flask, request
import pandas as pd
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Load warehouse data
df = pd.read_csv("warehouse.csv")

def find_item_location(item_name):
    """Search warehouse CSV for item location."""
    item = df[df['Item'].str.lower() == item_name.lower()]
    if not item.empty:
        location = item.iloc[0]['Location']
        quantity = item.iloc[0]['Quantity']
        return f"📍 {item_name} is at {location}. Stock: {quantity} left."
    return f"❌ Sorry, {item_name} is not found in the warehouse."

@app.route("/webhook", methods=["POST"])
def whatsapp_bot():
    """Handle incoming WhatsApp messages."""
    incoming_msg = request.form.get("Body").strip()
    response = MessagingResponse()
    
    if incoming_msg.lower() == "hi":
        response.message("Hello! Ask me where an item is located.")
    else:
        reply = find_item_location(incoming_msg)
        response.message(reply)

    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
