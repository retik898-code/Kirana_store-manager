# 🏪 Kirana Store Smart Inventory & Reorder System

An automated, data-driven inventory management and automated supply chain optimization platform designed for hyper-local retail operations (Kirana stores). This platform replaces traditional manual bookkeeping processes with a modern, decoupled client-server architecture featuring real-time checkout transaction billing, automated rule-based low-stock anomaly tracking, and automated predictive restock generation using generative AI models.

---

## 📌 Problem Statement & Real-World Impact

Traditional local Mom-and-Pop (Kirana) stores operate with dense product listings, tight margins, and high turnover. Due to a reliance on paper ledgers or memory, shopkeepers frequently fall victim to:
1. **Stockouts**: Running completely out of daily kitchen essentials, resulting in immediate revenue loss and customer friction.
2. **Dead Stock Over-purchasing**: Unwittingly tying up limited working capital in slow-moving categories due to a lack of data-driven analytics.

**Real-World Impact**: This platform bridges the software accessibility gap. By introducing automated transaction workflows, shop owners minimize operational overhead, protect working capital from stagnation, and instantly generate crisp, ready-to-send B2B supplier purchase request templates directly from low-stock alerts with a single click.

---

## 🛠️ System Architecture & Workflow Pipeline

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        frontend client (streamlit)                     │
│  - Analytics Dashboard Panel   - Terminal Billing   - AI Supply Panel  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                        Asynchronous HTTP (JSON)
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                        backend server (fastapi)                        │
│  - Operational Route Controllers             - Request Payloads        │
└─────────────────┬────────────────────────────────────┬─────────────────┘
                  │                                    │
                  ▼                                    ▼
┌───────────────────────────────────┐    ┌───────────────────────────────┐
│          database engine          │    │         genai service         │
│  - SQLite Local Instance          │    │  - Google Gemini Pro Model   │
│  - Products, Sales, & Suppliers   │    │  - Velocity Insight Synthesis │
└───────────────────────────────────┘    └───────────────────────────────┘