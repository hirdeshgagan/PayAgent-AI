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

# PayPal Sandbox Credentials (Aap apne PayPal Developer Dashboard se Client ID aur Secret yahan daal sakte hain)
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
    
    # Advanced AI Agent Intent Matching & Product Recommendation with Image URLs
    if any(keyword in user_msg for keyword in ["headphone", "audio", "earbuds", "music"]):
        product = {
            "id": "prod_01",
            "name": "pTron Bassbuds Pro AI-ENC Wireless Earbuds",
            "price": "49.99",
            "currency": "USD",
            "category": "Electronics",
            "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&auto=format&fit=crop&q=60",
            "description": "High-fidelity sound, AI environmental noise cancellation, and ultra-low latency gaming mode."
        }
        reply = f"Maine aapke liye top-rated **{product['name']}** select kiya hai ($49.99). Iski image aur details aap side card mein dekh sakte hain. Kya main iska autonomous PayPal checkout initiate karun?"
    
    elif any(keyword in user_msg for keyword in ["keyboard", "gaming", "mechanical", "setup"]):
        product = {
            "id": "prod_02",
            "name": "RGB Mechanical Pro Gaming Keyboard",
            "price": "79.99",
            "currency": "USD",
            "category": "Peripherals",
            "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&auto=format&fit=crop&q=60",
            "description": "Hot-swappable switches, custom RGB profiles, and ergonomic wrist rest for pro gamers."
        }
        reply = f"Aapke gaming setup ke liye yeh **{product['name']}** ($79.99) sabse best rahega. Bataiye, kya direct order place karein?"
    
    elif any(keyword in user_msg for keyword in ["cloud", "optimizer", "dev", "server"]):
        product = {
            "id": "prod_03",
            "name": "Cloud FinOps AI Cost Optimizer License",
            "price": "129.99",
            "currency": "USD",
            "category": "Developer Tools",
            "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=500&auto=format&fit=crop&q=60",
            "description": "Automated AWS/Cloud cost tracking, anomaly detection, and instant savings recommendations."
        }
        reply = f"Cloud management ke liye hamara flagship tool **{product['name']}** ($129.99) available hai. Securely checkout karne ke liye button par click karein."
    
    else:
        product = {
            "id": "prod_04",
            "name": "Smart AI Productivity Hub Gadget",
            "price": "29.99",
            "currency": "USD",
            "category": "Gadgets",
            "image": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=500&auto=format&fit=crop&q=60",
            "description": "Compact hardware companion for quick AI queries and daily workflow automation."
        }
        reply = f"Aapki query ke mutabiq maine **{product['name']}** ($29.99) analyze kiya hai. Kya iska payment process karein?"

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