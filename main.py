"""
FastAPI Backend for 2026 FIFA World Cup AI Predictor
Serves prediction data and LLM-generated scouting reports.
"""

import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# ──────────────────────────────────────────────────────
# App Init
# ──────────────────────────────────────────────────────
app = FastAPI(
    title="World Cup 2026 AI Predictor API",
    version="1.0.0",
)

# CORS — allow frontend dev servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────────────
# Data Loading (on startup)
# ──────────────────────────────────────────────────────
preds_df = pd.read_csv("world_cup_2026_predictions.csv")
test_df = pd.read_csv("test.csv")

# Merge predictions with raw stats
merged_df = preds_df.merge(test_df, on="team", suffixes=("", "_test"))
if "continent_test" in merged_df.columns:
    merged_df.drop(columns=["continent_test"], inplace=True)

# Pre-sort by prob_winner descending
merged_df = merged_df.sort_values("prob_winner", ascending=False).reset_index(drop=True)


# ──────────────────────────────────────────────────────
# Request / Response Models
# ──────────────────────────────────────────────────────
class ReportRequest(BaseModel):
    team: str


class ReportResponse(BaseModel):
    team: str
    report: str


# ──────────────────────────────────────────────────────
# API Endpoints
# ──────────────────────────────────────────────────────

@app.get("/api/teams")
def get_teams():
    """Return a list of all 48 team names sorted by winner probability."""
    return {"teams": merged_df["team"].tolist()}


@app.get("/api/leaderboard")
def get_leaderboard():
    """Return the full merged dataset sorted by prob_winner descending."""
    # Select relevant columns for the leaderboard
    cols = [
        "team", "continent",
        "prob_quarter_finalist", "prob_semi_finalist",
        "prob_finalist", "prob_winner",
        "fifa_rank_pre_tournament", "squad_total_market_value_eur",
        "wins_last_4y", "draws_last_4y", "losses_last_4y",
        "world_cup_titles_before", "squad_avg_age",
        "fifa_points_pre_tournament",
    ]
    available_cols = [c for c in cols if c in merged_df.columns]
    records = merged_df[available_cols].to_dict(orient="records")
    return {"leaderboard": records}


@app.get("/api/team/{team_name}")
def get_team(team_name: str):
    """Return probabilities and raw stats for a specific team."""
    row = merged_df[merged_df["team"].str.lower() == team_name.lower()]
    if row.empty:
        raise HTTPException(status_code=404, detail=f"Team '{team_name}' not found.")

    team_data = row.iloc[0]

    return {
        "team": team_data["team"],
        "continent": team_data["continent"],
        "probabilities": {
            "quarter_finalist": round(float(team_data["prob_quarter_finalist"]), 4),
            "semi_finalist": round(float(team_data["prob_semi_finalist"]), 4),
            "finalist": round(float(team_data["prob_finalist"]), 4),
            "winner": round(float(team_data["prob_winner"]), 4),
        },
        "stats": {
            "squad_total_market_value_eur": int(team_data["squad_total_market_value_eur"]),
            "fifa_rank_pre_tournament": int(team_data["fifa_rank_pre_tournament"]),
            "fifa_points_pre_tournament": round(float(team_data["fifa_points_pre_tournament"]), 2),
            "wins_last_4y": int(team_data["wins_last_4y"]),
            "draws_last_4y": int(team_data["draws_last_4y"]),
            "losses_last_4y": int(team_data["losses_last_4y"]),
            "world_cup_titles_before": int(team_data["world_cup_titles_before"]),
            "squad_avg_age": round(float(team_data["squad_avg_age"]), 1),
        },
    }


@app.post("/api/generate_report", response_model=ReportResponse)
def generate_report(req: ReportRequest):
    """Generate an AI scouting report for the given team via Groq."""
    row = merged_df[merged_df["team"].str.lower() == req.team.lower()]
    if row.empty:
        raise HTTPException(status_code=404, detail=f"Team '{req.team}' not found.")

    team_data = row.iloc[0]
    team_name = team_data["team"]

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured.")

    client = Groq(api_key=api_key)

    system_prompt = (
        "You are a data-driven tactician. You must strictly use the "
        "provided data. Do not hallucinate historical facts. "
        "Note: Argentina is the defending 2022 champion. "
        "Output exactly one paragraph of 3-4 punchy sentences blending "
        "market value, recent form, and historical pedigree to explain "
        "why the model rates this team the way it does."
    )

    user_prompt = (
        f"Generate a scouting report for {team_name} at the 2026 FIFA World Cup.\n\n"
        f"Data Profile:\n"
        f"- Predicted Probabilities: "
        f"QF={team_data['prob_quarter_finalist']:.4f}, "
        f"SF={team_data['prob_semi_finalist']:.4f}, "
        f"Final={team_data['prob_finalist']:.4f}, "
        f"Winner={team_data['prob_winner']:.4f}\n"
        f"- Squad Market Value: EUR {team_data['squad_total_market_value_eur']:,.0f}\n"
        f"- FIFA Rank (pre-tournament): {int(team_data['fifa_rank_pre_tournament'])}\n"
        f"- Last 4 Years Form: "
        f"{int(team_data['wins_last_4y'])}W / "
        f"{int(team_data['draws_last_4y'])}D / "
        f"{int(team_data['losses_last_4y'])}L\n"
        f"- Previous World Cup Titles: {int(team_data['world_cup_titles_before'])}\n"
        f"- Squad Average Age: {team_data['squad_avg_age']:.1f}\n\n"
        f"Explain in 3-4 sentences why the model rates {team_name} this way."
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
    return ReportResponse(team=team_name, report=narrative)


# ──────────────────────────────────────────────────────
# Serve Frontend (static index.html)
# ──────────────────────────────────────────────────────
@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")
