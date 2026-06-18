import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv

def main():
    # Load environment variables from .env
    load_dotenv()

    # ──────────────────────────────────────────────
    # 1. Data Merging
    # ──────────────────────────────────────────────
    preds_df = pd.read_csv("world_cup_2026_predictions.csv")
    test_df  = pd.read_csv("test.csv")

    merged_df = preds_df.merge(test_df, on="team", suffixes=("", "_test"))

    # ──────────────────────────────────────────────
    # 2. Filter Top 3 by prob_winner
    # ──────────────────────────────────────────────
    top3 = (
        merged_df
        .sort_values("prob_winner", ascending=False)
        .head(3)
        .reset_index(drop=True)
    )

    print("=" * 70)
    print("     2026 FIFA WORLD CUP — AI SCOUTING REPORTS (Top 3)")
    print("=" * 70)
    print(f"\n  Model : llama-3.1-8b-instant via Groq")
    print(f"  Teams : {', '.join(top3['team'].tolist())}")

    # ──────────────────────────────────────────────
    # 3. Groq API Setup
    # ──────────────────────────────────────────────
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    system_prompt = (
        "You are an elite football tactician and data analyst who has spent "
        "decades studying World Cup history, squad compositions, and "
        "tournament dynamics. You blend hard data with tactical insight to "
        "produce punchy, authoritative scouting narratives. "
        "Always output exactly one paragraph of 3-4 sentences. "
        "Focus on the blend of market value, recent form, and historical pedigree "
        "to explain why the data predicts this outcome for the team."
    )

    # ──────────────────────────────────────────────
    # 4 & 5. Loop through Top 3, build prompt, call API
    # ──────────────────────────────────────────────
    for idx, row in top3.iterrows():
        team_name    = row["team"]
        prob_qf      = row["prob_quarter_finalist"]
        prob_sf      = row["prob_semi_finalist"]
        prob_final   = row["prob_finalist"]
        prob_winner  = row["prob_winner"]
        market_value = row["squad_total_market_value_eur"]
        fifa_rank    = row["fifa_rank_pre_tournament"]
        wins         = row["wins_last_4y"]
        losses       = row["losses_last_4y"]
        draws        = row["draws_last_4y"]
        titles       = row["world_cup_titles_before"]

        user_prompt = (
            f"Generate a scouting report for {team_name} at the 2026 FIFA World Cup.\n\n"
            f"Data Profile:\n"
            f"- Predicted Probabilities: QF={prob_qf:.4f}, SF={prob_sf:.4f}, "
            f"Final={prob_final:.4f}, Winner={prob_winner:.4f}\n"
            f"- Squad Market Value: EUR {market_value:,.0f}\n"
            f"- FIFA Rank (pre-tournament): {int(fifa_rank)}\n"
            f"- Last 4 Years Form: {int(wins)}W / {int(draws)}D / {int(losses)}L\n"
            f"- Previous World Cup Titles: {int(titles)}\n\n"
            f"Explain in 3-4 sentences why the model rates {team_name} this way, "
            f"connecting the data points to real tactical and historical factors."
        )

        # Call Groq API
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

        # ──────────────────────────────────────────
        # 6. Print cleanly separated output
        # ──────────────────────────────────────────
        print(f"\n{'-' * 70}")
        print(f"  #{idx + 1}  {team_name.upper()}")
        print(f"      Prob Winner: {prob_winner:.4f}  |  FIFA Rank: {int(fifa_rank)}  |  "
              f"Value: EUR {market_value:,.0f}")
        print(f"{'-' * 70}")
        print(f"\n  {narrative}\n")

    print("=" * 70)
    print("  Scouting reports generated successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()
