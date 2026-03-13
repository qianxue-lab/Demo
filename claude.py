import streamlit as st
import anthropic
import json

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MSME CreditAI",
    page_icon="💼",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

.main { background-color: #0d0f14; }

/* Header */
.hero {
    background: linear-gradient(135deg, #1a1f2e 0%, #0d1117 100%);
    border: 1px solid #2a3142;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
}
.hero h1 {
    font-size: 2.2rem;
    font-weight: 700;
    color: #e8eaf0;
    margin: 0 0 0.4rem 0;
}
.hero h1 span { color: #4ade80; }
.hero p {
    color: #7a8499;
    font-size: 0.95rem;
    margin: 0;
}

/* Section labels */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    color: #4ade80;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* Score card */
.score-card {
    border-radius: 14px;
    padding: 1.8rem 2rem;
    margin: 1.5rem 0;
    border: 1px solid;
    text-align: center;
}
.score-high {
    background: linear-gradient(135deg, #052e16 0%, #0d1f0d 100%);
    border-color: #4ade80;
}
.score-medium {
    background: linear-gradient(135deg, #1c1a05 0%, #1a1505 100%);
    border-color: #facc15;
}
.score-low {
    background: linear-gradient(135deg, #1f0d0d 0%, #200808 100%);
    border-color: #f87171;
}
.score-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.score-value {
    font-size: 3rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.score-tier {
    font-size: 1rem;
    font-weight: 600;
    opacity: 0.85;
}

/* Info box */
.info-box {
    background: #131720;
    border: 1px solid #2a3142;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
    font-size: 0.9rem;
    color: #c8ccd8;
    line-height: 1.7;
}

/* Tips */
.tip-item {
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
    padding: 0.7rem 0;
    border-bottom: 1px solid #1e2330;
    color: #c8ccd8;
    font-size: 0.88rem;
    line-height: 1.6;
}
.tip-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    background: #1e2d1e;
    color: #4ade80;
    padding: 2px 7px;
    border-radius: 4px;
    flex-shrink: 0;
    margin-top: 2px;
}

/* Divider */
hr { border-color: #1e2330; }

/* Streamlit overrides */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] select {
    background-color: #131720 !important;
    color: #e8eaf0 !important;
    border: 1px solid #2a3142 !important;
    border-radius: 8px !important;
}
div[data-testid="stSlider"] { accent-color: #4ade80; }
.stButton > button {
    background: linear-gradient(135deg, #16a34a, #15803d) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>MSME <span>CreditAI</span></h1>
    <p>Alternative Credit Scoring for ASEAN Small Businesses · Powered by AI</p>
</div>
""", unsafe_allow_html=True)

# ── Form ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">📋 Business Profile</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    business_name = st.text_input("Business Name", placeholder="e.g. Kedai Runcit Ali")
    industry = st.selectbox("Industry", [
        "Retail / Grocery", "Food & Beverage", "Agriculture",
        "Manufacturing", "Services", "E-commerce", "Handicraft / Artisan", "Other"
    ])
    years_operating = st.number_input("Years in Operation", min_value=0, max_value=50, value=2)
    num_employees = st.number_input("Number of Employees", min_value=1, max_value=200, value=5)

with col2:
    monthly_revenue = st.number_input("Avg Monthly Revenue (RM)", min_value=0, value=8000, step=500)
    monthly_expenses = st.number_input("Avg Monthly Expenses (RM)", min_value=0, value=5500, step=500)
    has_bank_account = st.selectbox("Has Business Bank Account?", ["Yes", "No"])
    loan_amount_requested = st.number_input("Loan Amount Requested (RM)", min_value=0, value=20000, step=1000)

st.markdown('<div class="section-label" style="margin-top:1rem">📊 Additional Signals</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    has_digital_presence = st.selectbox("Online/Digital Presence?", ["Yes — active social media/e-commerce", "Partial — basic online presence", "No"])
    payment_method = st.selectbox("Accepts Digital Payments?", ["Yes — multiple platforms", "Yes — one platform", "Cash only"])

with col4:
    supplier_relationships = st.selectbox("Supplier Relationships", ["Long-term (3+ years)", "Medium (1–3 years)", "Short-term / New"])
    customer_retention = st.selectbox("Customer Base", ["Mostly repeat customers", "Mixed", "Mostly new customers"])

additional_notes = st.text_area("Any additional context (optional)", placeholder="e.g. Recently expanded to online sales, seasonal business, etc.", height=80)

st.markdown("<br>", unsafe_allow_html=True)
submit = st.button("🔍 Analyse Creditworthiness")

# ── AI Analysis ───────────────────────────────────────────────────────────────
if submit:
    if monthly_revenue == 0:
        st.warning("Please enter a monthly revenue figure.")
    else:
        with st.spinner("AI is analysing your business profile..."):

            business_data = {
                "business_name": business_name or "Unnamed Business",
                "industry": industry,
                "years_operating": years_operating,
                "num_employees": num_employees,
                "monthly_revenue_RM": monthly_revenue,
                "monthly_expenses_RM": monthly_expenses,
                "monthly_net_profit_RM": monthly_revenue - monthly_expenses,
                "profit_margin_pct": round((monthly_revenue - monthly_expenses) / monthly_revenue * 100, 1) if monthly_revenue else 0,
                "has_bank_account": has_bank_account,
                "loan_amount_requested_RM": loan_amount_requested,
                "loan_to_monthly_revenue_ratio": round(loan_amount_requested / monthly_revenue, 1) if monthly_revenue else 0,
                "digital_presence": has_digital_presence,
                "digital_payments": payment_method,
                "supplier_relationships": supplier_relationships,
                "customer_base": customer_retention,
                "additional_notes": additional_notes or "None"
            }

            prompt = f"""
You are an inclusive MSME credit analyst for ASEAN markets. Assess this small business's creditworthiness using ALTERNATIVE data signals (not just bank history), because many MSMEs are unbanked or informal.

Business Data:
{json.dumps(business_data, indent=2)}

Respond ONLY with a valid JSON object in this exact format (no markdown, no extra text):
{{
  "credit_score": <integer 300-850>,
  "tier": "<one of: High / Medium / Low>",
  "summary": "<2-3 sentence plain-language summary of their creditworthiness>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "risks": ["<risk 1>", "<risk 2>"],
  "improvement_tips": ["<tip 1>", "<tip 2>", "<tip 3>"],
  "recommended_loan_range_RM": "<e.g. RM 10,000 – RM 25,000>"
}}

Be fair, practical, and encouraging. Consider that informal businesses in ASEAN often lack credit history but are viable. Weight digital presence, profit margins, years operating, and supplier relationships heavily.
"""

            try:
                client = anthropic.Anthropic()
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )

                raw = response.content[0].text.strip()
                if raw.startswith("```"):
                    raw = raw.split("```")[1]
                    if raw.startswith("json"):
                        raw = raw[4:]
                result = json.loads(raw.strip())

                score = result["credit_score"]
                tier = result["tier"]

                # Score card styling
                if tier == "High":
                    card_class = "score-high"
                    score_color = "#4ade80"
                elif tier == "Medium":
                    card_class = "score-medium"
                    score_color = "#facc15"
                else:
                    card_class = "score-low"
                    score_color = "#f87171"

                st.markdown(f"""
<div class="score-card {card_class}">
    <div class="score-label" style="color:{score_color}">Credit Score</div>
    <div class="score-value" style="color:{score_color}">{score}</div>
    <div class="score-tier" style="color:{score_color}">{tier} Creditworthiness</div>
</div>
""", unsafe_allow_html=True)

                # Summary
                st.markdown('<div class="section-label">📝 AI Summary</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="info-box">{result["summary"]}</div>', unsafe_allow_html=True)

                # Recommended loan
                st.markdown(f'<div class="info-box">💰 <strong>Recommended Loan Range:</strong> {result["recommended_loan_range_RM"]}</div>', unsafe_allow_html=True)

                # Strengths & Risks
                col5, col6 = st.columns(2)
                with col5:
                    st.markdown('<div class="section-label">✅ Strengths</div>', unsafe_allow_html=True)
                    strengths_html = "".join([f'<div class="tip-item"><span class="tip-num">+</span>{s}</div>' for s in result["strengths"]])
                    st.markdown(f'<div class="info-box" style="padding:0.8rem 1rem">{strengths_html}</div>', unsafe_allow_html=True)

                with col6:
                    st.markdown('<div class="section-label">⚠️ Risk Factors</div>', unsafe_allow_html=True)
                    risks_html = "".join([f'<div class="tip-item"><span class="tip-num" style="background:#2d1515;color:#f87171">!</span>{r}</div>' for r in result["risks"]])
                    st.markdown(f'<div class="info-box" style="padding:0.8rem 1rem">{risks_html}</div>', unsafe_allow_html=True)

                # Improvement tips
                st.markdown('<div class="section-label">🚀 How to Improve Your Score</div>', unsafe_allow_html=True)
                tips_html = "".join([
                    f'<div class="tip-item"><span class="tip-num">0{i+1}</span>{tip}</div>'
                    for i, tip in enumerate(result["improvement_tips"])
                ])
                st.markdown(f'<div class="info-box" style="padding:0.8rem 1rem">{tips_html}</div>', unsafe_allow_html=True)

            except json.JSONDecodeError:
                st.error("Could not parse AI response. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")