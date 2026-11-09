# PayAgent AI 🚀
### Autonomous Agentic Commerce powered by PayPal & AI

**PayAgent AI** is an intelligent full-stack shopping and payment assistant built for the **PayPal AI Hackathon**. It bridges natural language conversational AI with real-world financial transactions using the **PayPal Sandbox REST API**.

---

## 🌟 Key Features
- **Conversational Product Discovery:** Chat naturally to find products from popular simulated marketplaces (*Amazon*, *Flipkart*, etc.).
- **Rich Visual Showcase:** High-resolution product cards displaying live images, categories, and descriptions.
- **Autonomous PayPal Checkout:** Seamless integration with the **PayPal Orders API (`/v2/checkout/orders`)** for secure sandbox payment redirection.

---

## 🛠️ Tech Stack
- **Frontend:** Next.js 14, React, Tailwind CSS
- **Backend:** Python, FastAPI, Pydantic, Requests
- **Payments:** PayPal Sandbox REST API (OAuth2 Client Credentials & Orders)

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
\`\`\`bash
git clone https://github.com/hirdeshgagan/PayAgent-AI.git
cd PayAgent-AI
\`\`\`

### 2. Run the Backend (FastAPI)
\`\`\`bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
\`\`\`

### 3. Run the Frontend (Next.js)
\`\`\`bash
cd frontend-new
npm install
npm run dev
\`\`\`
Open your browser and navigate to `http://localhost:3000`.
