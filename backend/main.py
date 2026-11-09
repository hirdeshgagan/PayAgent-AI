import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from requests.auth import HTTPBasicAuth

app = FastAPI(title="PayAgent AI Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Aapke PayPal Developer Dashboard ke Sandbox Credentials
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "AVXA7PxB-gv6kcTJtnqlCThUH8DtyB-VmwKVmNJfFUw93MwWheRB_R9P71DfXiYNVg0piJul8AkRZask")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET", "EC6_7n19T6wP2llW4djZQFBXBhYL3zOraE8n4JOtyCqEEy9A7qZgI-poXM0nphQSxhB1ZPLBOQjoqmGp")
PAYPAL_BASE_URL = "https://api-m.sandbox.paypal.com"

def get_paypal_access_token():
    auth = HTTPBasicAuth(PAYPAL_CLIENT_ID, PAYPAL_SECRET)
    headers = {"Accept": "application/json", "Accept-Language": "en_US"}
    data = {"grant_type": "client_credentials"}
    response = requests.post(f"{PAYPAL_BASE_URL}/v1/oauth2/token", auth=auth, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    raise HTTPException(status_code=500, detail="Failed to authenticate with PayPal Sandbox")

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
def ai_agent_brain(req: ChatRequest):
    user_msg = req.message.lower()
    
    # Amazon / Flipkart Style Smart E-Commerce Intent Matching
    if any(keyword in user_msg for keyword in ["headphone", "audio", "earbuds", "music", "boat", "sony"]):
        product = {
            "id": "prod_01",
            "name": "boAt Airdopes 141 True Wireless Earbuds",
            "price": "39.99",
            "currency": "USD",
            "platform": "Amazon Choice",
            "category": "Electronics",
            "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&auto=format&fit=crop&q=60",
            "description": "42H Playtime, Beast Mode for Low Latency Gaming, ENx Tech, ASAP Charge."
        }
        reply = f"Amazon catalog se aapke liye top-rated **{product['name']}** ($39.99) fetch kiya hai. Yeh **Amazon Choice** product hai. Kya main iska secure PayPal checkout initiate karun?"
    
    elif any(keyword in user_msg for keyword in ["keyboard", "gaming", "mechanical", "mouse", "flipkart"]):
        product = {
            "id": "prod_02",
            "name": "Cosmic Byte CB-GK-16 Firefly Mechanical Keyboard",
            "price": "64.99",
            "currency": "USD",
            "platform": "Flipkart Assured",
            "category": "Gaming Peripherals",
            "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&auto=format&fit=crop&q=60",
            "description": "Outemu Blue Switches, Rainbow LED Backlit, Anti-Ghosting Keys for Pro Gamers."
        }
        reply = f"Flipkart Assured store se **{product['name']}** ($64.99) select kiya gaya hai. Bataiye, kya direct order place karein?"
    
    elif any(keyword in user_msg for keyword in ["phone", "mobile", "smartphone", "iphone", "samsung"]):
        product = {
            "id": "prod_03",
            "name": "OnePlus Nord CE 5G Smartphone",
            "price": "299.99",
            "currency": "USD",
            "platform": "Amazon Mega Store",
            "category": "Smartphones",
            "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500&auto=format&fit=crop&q=60",
            "description": "90Hz Fluid AMOLED display, 5G enabled, triple camera setup with fast charging."
        }
        reply = f"Aapki requirement ke mutabiq Amazon store se **{product['name']}** ($299.99) mil gaya hai. Secure checkout ke liye button par click karein."
    
    else:
        product = {
            "id": "prod_04",
            "name": "Smart AI Productivity Hub Gadget",
            "price": "24.99",
            "currency": "USD",
            "platform": "Amazon Prime",
            "category": "Gadgets",
            "image": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=500&auto=format&fit=crop&q=60",
            "description": "Compact hardware companion for quick AI queries and daily workflow automation."
        }
        reply = f"Amazon/Flipkart network se match karta hua **{product['name']}** ($24.99) analyze kiya hai. Kya iska payment process karein?"

    return {
        "reply": reply,
        "product": product
    }

@app.post("/api/create-paypal-order")
def create_paypal_order(product_price: str, product_name: str):
    token = get_paypal_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": product_price
            },
            "description": product_name
        }],
        "application_context": {
            "return_url": "https://developer.paypal.com",
            "cancel_url": "https://developer.paypal.com"
        }
    }
    response = requests.post(f"{PAYPAL_BASE_URL}/v2/checkout/orders", headers=headers, json=payload)
    if response.status_code == 201:
        order_data = response.json()
        approval_url = next((link["href"] for link in order_data["links"] if link["rel"] == "approve"), None)
        return {
            "status": "success",
            "order_id": order_data["id"],
            "approval_url": approval_url
        }
    
    raise HTTPException(status_code=500, detail="Failed to create PayPal Order")