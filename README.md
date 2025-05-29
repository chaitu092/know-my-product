# know-my-product

# 🛍️ ItemInsight – AI-Powered Product Info & Price Estimator

**ItemInsight** is a lightweight AI-powered application that delivers concise product summaries and real-time estimated prices in Indian Rupees (INR). Powered by cutting-edge Large Language Models (LLMs) like **GPT-4.1**, **Qwen**, and **LLaMA 3**, it’s perfect for quick product research, comparison, and market value estimation.

Built with **LangChain**, **Streamlit**, and integrations with **OpenAI** and **Groq**, ItemInsight offers a seamless experience with clean UI and structured output.

---

## 📌 Features

- ✅ Accepts free-text product name input
- 🧠 Utilizes top-tier LLMs (GPT-4.1, Qwen QWQ, LLaMA 3.3)
- ⚙️ Clean Streamlit UI for interactive exploration
- 📦 Returns structured JSON response with:
  - **Product Name**
  - **Short Description** (≤150 words)
  - **Estimated Price** in:
    - USD ($)
    - EUR (€)
    - INR (₹)
- 🔄 Multi-LLM toggle: switch easily between models
- 🔐 Secure API key usage via `.env` file
- 🌐 Ready for LLM observability via LangChain Tracing

---

## 🖼️ Sample Output

```json
{
  "product_name": "MacBook Air M2 (2023)",
  "product_details": "A lightweight, high-performance laptop powered by Apple’s M2 chip. Offers long battery life, a Retina display, and smooth macOS experience. Suitable for students, creators, and professionals.",
  "product_price_usd": 1200,
  "product_price_eur": 1100,
  "product_price_inr": 115000
}
