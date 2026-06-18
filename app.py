import streamlit as st
import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="FIFA World Cup 2026 Predictions",
    page_icon="⚽",
    layout="wide",
)

# ──────────────────────────────────────────────────────
# Custom CSS for premium look
# ──────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main header */
    .team-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .team-subtitle {
        font-size: 1.1rem;
        color: #888;
        margin-bottom: 1.5rem;
    }

    /* Probability cards */
    .prob-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .prob-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
    }
    .prob-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #a0a0b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    .prob-value {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Stats section */
    .stat-row {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.06);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .stat-label {
        font-size: 0.95rem;
        color: #a0a0b8;
        font-weight: 500;
    }
    .stat-value {
        font-size: 1.05rem;
        color: #e0e0f0;
        font-weight: 700;
    }

    /* Scouting report box */
    .report-box {
        background: linear-gradient(135deg, #1a1a2e, #0f3460);
        border-radius: 16px;
        padding: 1.8rem;
        border: 1px solid rgba(102, 126, 234, 0.25);
        line-height: 1.7;
        color: #d0d0e8;
        font-size: 1rem;
    }

    /* Leaderboard table tweaks */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29, #302b63, #24243e);
    }

    /* Divider */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102,126,234,0.4), transparent);
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────
# Data Loading (cached)
# ──────────────────────────────────────────────────────
@st.cache_data
def load_data():
    preds = pd.read_csv("world_cup_2026_predictions.csv")
    test  = pd.read_csv("test.csv")
    merged = preds.merge(test, on="team", suffixes=("", "_test"))
    # Clean up duplicate continent column if present
    if "continent_test" in merged.columns:
        merged.drop(columns=["continent_test"], inplace=True)
    return merged


data = load_data()

# ──────────────────────────────────────────────────────
# Sidebar — Team Selector
# ──────────────────────────────────────────────────────
st.sidebar.markdown("## 🏆 World Cup 2026")
st.sidebar.markdown("##### Prediction Dashboard")
st.sidebar.markdown("---")

sorted_teams = data.sort_values("prob_winner", ascending=False)["team"].tolist()
selected_team = st.sidebar.selectbox(
    "Select a Team",
    sorted_teams,
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.caption("Model: Random Forest (GroupKFold CV)")
st.sidebar.caption("LLM: Llama 3.1 8B via Groq")
st.sidebar.caption("Data: FIFA 2002-2022 historical")

# ──────────────────────────────────────────────────────
# Get selected team data
# ──────────────────────────────────────────────────────
team_row = data[data["team"] == selected_team].iloc[0]

# ──────────────────────────────────────────────────────
# Tabs
# ──────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📊 Team Analysis", "🌍 Global Leaderboard"])

# ══════════════════════════════════════════════════════
# TAB 1: Team Analysis
# ══════════════════════════════════════════════════════
with tab1:
    # Header
    st.markdown(f'<div class="team-header">{selected_team}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="team-subtitle">{team_row["continent"]}  ·  '
        f'FIFA Rank #{int(team_row["fifa_rank_pre_tournament"])}  ·  '
        f'2026 FIFA World Cup</div>',
        unsafe_allow_html=True,
    )

    # ── Stage Probabilities ──────────────────────────
    st.markdown("### Stage Probabilities")

    prob_cols = st.columns(4)
    prob_data = [
        ("Quarter-Final", team_row["prob_quarter_finalist"]),
        ("Semi-Final",     team_row["prob_semi_finalist"]),
        ("Final",          team_row["prob_finalist"]),
        ("Winner",         team_row["prob_winner"]),
    ]

    for col, (label, value) in zip(prob_cols, prob_data):
        with col:
            st.markdown(
                f"""
                <div class="prob-card">
                    <div class="prob-label">{label}</div>
                    <div class="prob-value">{value * 100:.1f}%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── Raw Stats ────────────────────────────────────
    st.markdown("### Team Profile")

    market_value = team_row["squad_total_market_value_eur"]
    fifa_rank    = int(team_row["fifa_rank_pre_tournament"])
    wins         = int(team_row["wins_last_4y"])
    draws        = int(team_row["draws_last_4y"])
    losses       = int(team_row["losses_last_4y"])
    titles       = int(team_row["world_cup_titles_before"])
    avg_age      = team_row["squad_avg_age"]

    stats = [
        ("Squad Market Value",    f"\u20ac{market_value:,.0f}"),
        ("FIFA Rank",             f"#{fifa_rank}"),
        ("Last 4 Years Form",     f"{wins}W / {draws}D / {losses}L"),
        ("World Cup Titles",      str(titles)),
        ("Squad Average Age",     f"{avg_age:.1f} years"),
        ("FIFA Points",           f"{team_row['fifa_points_pre_tournament']:,.2f}"),
    ]

    left_col, right_col = st.columns(2)
    for i, (label, value) in enumerate(stats):
        target_col = left_col if i % 2 == 0 else right_col
        with target_col:
            st.markdown(
                f"""
                <div class="stat-row">
                    <span class="stat-label">{label}</span>
                    <span class="stat-value">{value}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── AI Scouting Report ───────────────────────────
    st.markdown("### AI Scouting Report")

    if st.button("Generate AI Scouting Report", type="primary", use_container_width=True):
        with st.spinner(f"Generating scouting report for {selected_team}..."):
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

            system_prompt = (
                "You are a data-driven tactician. You must strictly use the "
                "provided data. Do not hallucinate historical facts. "
                "Note: Argentina is the defending 2022 champion. "
                "Output exactly one paragraph of 3-4 punchy sentences blending "
                "market value, recent form, and historical pedigree to explain "
                "why the model rates this team the way it does."
            )

            user_prompt = (
                f"Generate a scouting report for {selected_team} at the 2026 FIFA World Cup.\n\n"
                f"Data Profile:\n"
                f"- Predicted Probabilities: QF={team_row['prob_quarter_finalist']:.4f}, "
                f"SF={team_row['prob_semi_finalist']:.4f}, "
                f"Final={team_row['prob_finalist']:.4f}, "
                f"Winner={team_row['prob_winner']:.4f}\n"
                f"- Squad Market Value: EUR {market_value:,.0f}\n"
                f"- FIFA Rank (pre-tournament): {fifa_rank}\n"
                f"- Last 4 Years Form: {wins}W / {draws}D / {losses}L\n"
                f"- Previous World Cup Titles: {titles}\n"
                f"- Squad Average Age: {avg_age:.1f}\n\n"
                f"Explain in 3-4 sentences why the model rates {selected_team} this way."
            )

            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt},
                ],
                model="llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=300,
            )

            narrative = chat_completion.choices[0].message.content.strip()

        st.markdown(
            f'<div class="report-box">{narrative}</div>',
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════
# TAB 2: Global Leaderboard
# ══════════════════════════════════════════════════════
with tab2:
    st.markdown(
        '<div class="team-header">Global Leaderboard</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="team-subtitle">All 48 teams ranked by predicted Winner probability</div>',
        unsafe_allow_html=True,
    )

    leaderboard_cols = [
        "team", "continent",
        "prob_quarter_finalist", "prob_semi_finalist",
        "prob_finalist", "prob_winner",
        "fifa_rank_pre_tournament", "squad_total_market_value_eur",
        "wins_last_4y", "draws_last_4y", "losses_last_4y",
    ]

    leaderboard = (
        data[leaderboard_cols]
        .sort_values("prob_winner", ascending=False)
        .reset_index(drop=True)
    )
    leaderboard.index += 1
    leaderboard.index.name = "Rank"

    # Rename for display
    display_df = leaderboard.rename(columns={
        "team":                         "Team",
        "continent":                    "Continent",
        "prob_quarter_finalist":        "P(QF)",
        "prob_semi_finalist":           "P(SF)",
        "prob_finalist":                "P(Final)",
        "prob_winner":                  "P(Winner)",
        "fifa_rank_pre_tournament":     "FIFA Rank",
        "squad_total_market_value_eur": "Market Value (EUR)",
        "wins_last_4y":                 "W",
        "draws_last_4y":               "D",
        "losses_last_4y":              "L",
    })

    # Format probability columns as percentages
    for pcol in ["P(QF)", "P(SF)", "P(Final)", "P(Winner)"]:
        display_df[pcol] = display_df[pcol].apply(lambda x: f"{x * 100:.1f}%")

    display_df["Market Value (EUR)"] = display_df["Market Value (EUR)"].apply(
        lambda x: f"\u20ac{x:,.0f}"
    )
    display_df["FIFA Rank"] = display_df["FIFA Rank"].astype(int)

    st.dataframe(
        display_df,
        use_container_width=True,
        height=700,
    )
