"use client";
import { useState } from "react";

export default function PayAgentApp() {
  const [messages, setMessages] = useState([
    { 
      sender: "ai", 
      text: "👋 Hello Hirdesh! Main aapka **PayAgent AI** autonomous commerce assistant hoon. Aaj aap kya khareedna chahte hain ya kis service ka payment automate karna hai? (Jaise: *wireless headphones*, *gaming keyboard*, ya *cloud optimizer*)" 
    }
  ]);
  const [input, setInput] = useState("");
  const [activeProduct, setActiveProduct] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = input;
    setMessages((prev) => [...prev, { sender: "user", text: userMsg }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { sender: "ai", text: data.reply }]);
      setActiveProduct(data.product);
    } catch (err) {
      setMessages((prev) => [...prev, { sender: "ai", text: "⚠️ Error connecting to AI backend server. Make sure FastAPI is running!" }]);
    }
    setLoading(false);
  };

  const handlePayPalCheckout = async () => {
    if (!activeProduct) return;
    try {
      setLoading(true);
      const res = await fetch(`http://localhost:8000/api/create-paypal-order?product_price=${activeProduct.price}&product_name=${encodeURIComponent(activeProduct.name)}`, {
        method: "POST"
      });
      const data = await res.json();
      if (data.approval_url) {
        window.location.href = data.approval_url; // Redirects to PayPal Sandbox Secure Checkout
      }
    } catch (err) {
      alert("PayPal Checkout Failed!");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center p-4 md:p-8">
      {/* Header */}
      <header className="w-full max-w-4xl flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
        <div>
          <h1 className="text-2xl font-black bg-gradient-to-r from-emerald-400 to-blue-500 bg-clip-text text-transparent">
            PayAgent AI 🚀
          </h1>
          <p className="text-xs text-slate-400">Autonomous Agentic Commerce powered by PayPal & AI</p>
        </div>
        <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 text-xs font-semibold rounded-full border border-emerald-500/20">
          PayPal Hackathon Ready
        </span>
      </header>

      {/* Main Workspace Container */}
      <main className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-3 gap-6 flex-1">
        
        {/* Left / Center: Chat Interface */}
        <section className="md:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col h-[70vh] shadow-2xl">
          <div className="flex-1 overflow-y-auto space-y-4 pr-2">
            {messages.map((msg, idx) => (
              <div 
                key={idx} 
                className={`p-3.5 rounded-xl max-w-[85%] text-sm leading-relaxed ${
                  msg.sender === "user" 
                    ? "bg-emerald-600 text-white ml-auto rounded-br-none shadow-md" 
                    : "bg-slate-800 text-slate-200 mr-auto rounded-bl-none border border-slate-700/50"
                }`}
              >
                <div dangerouslySetInnerHTML={{ __html: msg.text }}></div>
              </div>
            ))}
            {loading && (
              <div className="text-slate-400 text-xs animate-pulse flex items-center gap-2 p-2">
                <span className="w-2 h-2 bg-emerald-400 rounded-full animate-ping"></span>
                AI Agent is analyzing catalog & generating secure PayPal order...
              </div>
            )}
          </div>

          {/* Input Form */}
          <form onSubmit={sendMessage} className="mt-4 flex gap-2 pt-2 border-t border-slate-800">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask AI agent to find a product or service..."
              className="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-emerald-500 transition"
            />
            <button 
              type="submit" 
              className="bg-emerald-500 hover:bg-emerald-600 px-6 py-3 rounded-xl font-bold text-sm text-slate-950 transition shadow-lg shadow-emerald-500/20"
            >
              Send
            </button>
          </form>
        </section>

        {/* Right Sidebar: Active AI Decision / Cart & Checkout Card */}
        <aside className="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between shadow-2xl h-[70vh]">
          <div>
            <h2 className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-4 border-b border-slate-800 pb-2">
              🤖 Active AI Decision
            </h2>

            {activeProduct ? (
              <div className="bg-slate-950 border border-emerald-500/30 rounded-xl p-4 space-y-3 shadow-inner">
                <span className="text-[10px] uppercase font-bold px-2 py-0.5 bg-blue-500/10 text-blue-400 rounded">
                  {activeProduct.category}
                </span>
                <h3 className="font-bold text-base text-white">{activeProduct.name}</h3>
                <p className="text-xs text-slate-300 leading-relaxed">{activeProduct.description}</p>
                <div className="text-xl font-black text-emerald-400 pt-2">
                  ${activeProduct.price} <span className="text-xs font-normal text-slate-400">{activeProduct.currency}</span>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-slate-500 text-sm">
                No product selected yet. Chat with the AI agent to generate an autonomous order.
              </div>
            )}
          </div>

          {/* PayPal Checkout Button Action */}
          {activeProduct && (
            <div className="pt-4 border-t border-slate-800 space-y-3">
              <button
                onClick={handlePayPalCheckout}
                className="w-full bg-[#0070BA] hover:bg-[#005ea6] text-white font-bold py-3 px-4 rounded-xl text-sm flex items-center justify-center gap-2 transition shadow-lg shadow-blue-500/20"
              >
                <span>Pay securely with</span>
                <span className="italic font-black tracking-tight text-amber-300">PayPal</span>
              </button>
              <p className="text-[10px] text-center text-slate-500">
                Sandbox Environment Active • Instant API Capture
              </p>
            </div>
          )}
        </aside>

      </main>
    </div>
  );
}