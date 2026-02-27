import streamlit as st
import matplotlib.pyplot as plt
from analyzer import *
from nudger import *

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Budget Nudge AI",
    page_icon="💸",
    layout="wide"
)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page):
    st.session_state.page = page


# ---------------- GLOBAL STYLES ----------------
st.markdown("""
<style>

/* App Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #eef2ff 0%, #f8fafc 100%);
}

/* Remove top padding */
.block-container {
    padding-top: 2rem;
}

/* Typography */
html, body {
    font-family: 'Inter', sans-serif;
}

/* Card System */
.card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(10px);
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.06);
    transition: 0.3s ease-in-out;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 15px 35px rgba(0,0,0,0.1);
}

/* Section Title */
.section-title {
    font-size: 26px;
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 20px;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    padding: 80px;
    border-radius: 25px;
    text-align: center;
    color: white;
    box-shadow: 0px 15px 40px rgba(79,70,229,0.4);
}

/* Success */
.success-text {
    color: #059669;
    font-weight: 600;
}

/* Alert */
.alert-text {
    color: #dc2626;
    font-weight: 600;
}

/* Insight Card */
.insight-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.05);
    border-left: 6px solid #6366f1;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# =======================
# -------- HOME ---------
# =======================
if st.session_state.page == "home":

    st.markdown("""
    <div class="hero">
        <h1>💸 Budget Nudge AI</h1>
        <p>Smart • Predictive • AI-Powered Financial Coaching</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Enter Dashboard", use_container_width=True):
            go_to("dashboard")


# =======================
# ----- DASHBOARD -------
# =======================
elif st.session_state.page == "dashboard":

    st.sidebar.title("⚙ Settings")
    st.sidebar.markdown("---")

    income = st.sidebar.number_input("Monthly Income (₹)", value=25000)
    threshold = st.sidebar.number_input("Food Budget Threshold (₹)", value=4000)
    personality = st.sidebar.selectbox(
        "AI Personality Mode",
        ["Savage", "Friendly", "Financial Guru", "Meme Mode"]
    )

    if st.sidebar.button("Logout"):
        go_to("home")

    st.markdown("<div class='section-title'>📊 Financial Dashboard</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Transaction CSV", type=["csv"])

    if uploaded_file is None:
        st.info("Upload transaction file to begin analysis.")
    else:
        df = load_data(uploaded_file)
        df = categorize_spending(df)

        total_spend, food_spend = calculate_totals(df)
        projection = projected_spend(df)
        category_sum = df.groupby("category")["amount"].sum()

        # -------- CARD GRID (3 COLUMN SYSTEM) --------
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.metric("💰 Total Spend", f"₹{total_spend}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.metric("🍔 Food Spend", f"₹{food_spend}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.metric("📈 Projected Spend", f"₹{projection}")
            st.markdown("</div>", unsafe_allow_html=True)

        # -------- SPENDING RATIO CARD --------
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        food_ratio = (food_spend / total_spend) * 100 if total_spend != 0 else 0
        st.subheader("Spending Ratio")
        st.progress(min(int(food_ratio), 100))

        if food_ratio > 30:
            st.markdown(f"<div class='alert-text'>Food spending is {food_ratio:.2f}% of total expenses.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='success-text'>Food spending is {food_ratio:.2f}% of total expenses.</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # -------- ANALYTICS CARD --------
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Spending Analytics")

        fig, ax = plt.subplots()
        bars = ax.bar(category_sum.index, category_sum.values, color="#4f46e5")
        ax.spines[['top', 'right']].set_visible(False)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2,
                    height,
                    f"₹{int(height)}",
                    ha='center',
                    va='bottom')

        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

        # -------- AI INSIGHT CARD --------
        st.markdown("<br>", unsafe_allow_html=True)

        if check_overspend(food_spend, threshold, income):

            severity = ((food_spend - threshold) / threshold) * 100

            st.markdown(f"""
            <div class='insight-card'>
                <div class='alert-text'>⚠ Overspending Detected</div>
                <p>You exceeded your food budget by <b>{severity:.2f}%</b>.</p>
            </div>
            """, unsafe_allow_html=True)

            with st.spinner("Generating AI Insight..."):
                nudge = generate_nudge(food_spend, threshold, personality, projection)

            st.markdown(f"""
            <div class='insight-card'>
                <div style='font-weight:600;color:#1e3a8a;'>💡 AI Suggestion</div>
                <p>{nudge}</p>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class='insight-card'>
                <div class='success-text'>🎉 You are within budget. Keep it up!</div>
            </div>
            """, unsafe_allow_html=True)