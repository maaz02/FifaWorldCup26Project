import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def main():
    # ──────────────────────────────────────────────
    # Load datasets
    # ──────────────────────────────────────────────
    train_df = pd.read_csv("train.csv")
    test_df  = pd.read_csv("test.csv")

    targets = ["quarter_finalist", "semi_finalist", "finalist", "winner"]

    # ──────────────────────────────────────────────
    # 1. Preprocessing — Train
    # ──────────────────────────────────────────────
    # Impute missing squad_total_market_value_eur by version median
    median_by_version = train_df.groupby("version")["squad_total_market_value_eur"].transform("median")
    train_df["squad_total_market_value_eur"] = train_df["squad_total_market_value_eur"].fillna(median_by_version)

    # Separate features and targets
    drop_cols = ["team", "continent"] + targets
    X_train = train_df.drop(columns=drop_cols)
    y_train = train_df[targets]

    feature_names = X_train.columns.tolist()

    # ──────────────────────────────────────────────
    # 2. Preprocessing — Test
    # ──────────────────────────────────────────────
    # Save identifiers for the output file
    test_teams      = test_df["team"].values
    test_continents = test_df["continent"].values

    # Drop identifiers and target columns (which are NaN in test)
    test_drop_cols = ["team", "continent"] + [t for t in targets if t in test_df.columns]
    X_test = test_df.drop(columns=test_drop_cols)

    # Impute any remaining missing numeric values in test using
    # the median from the 2026 subset of training data
    train_2026_mask = train_df["version"] == 2026
    if train_2026_mask.any():
        fill_values = train_df.loc[train_2026_mask, feature_names].median()
    else:
        # Fallback: use global training medians
        fill_values = X_train.median()

    X_test = X_test[feature_names]  # ensure column alignment
    X_test = X_test.fillna(fill_values)

    print("=" * 70)
    print("        2026 FIFA WORLD CUP — PREDICTION PIPELINE")
    print("=" * 70)
    print(f"\n  Training samples  : {len(X_train)}")
    print(f"  Test samples      : {len(X_test)}  (48 qualified teams)")
    print(f"  Features          : {len(feature_names)}")
    print(f"  Targets           : {targets}")

    # ──────────────────────────────────────────────
    # 3. Train final models on FULL training data
    # ──────────────────────────────────────────────
    print("\n  Training 4 Random Forest models on full historical data ...")

    predictions = {}
    for target in targets:
        clf = RandomForestClassifier(
            n_estimators=300,
            max_depth=6,
            min_samples_leaf=4,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        )
        clf.fit(X_train, y_train[target])
        proba = clf.predict_proba(X_test)[:, 1]
        predictions[f"prob_{target}"] = proba
        print(f"    [OK] {target}")

    # ──────────────────────────────────────────────
    # 4. Build and save output CSV
    # ──────────────────────────────────────────────
    output_df = pd.DataFrame({
        "team":                 test_teams,
        "continent":            test_continents,
        "prob_quarter_finalist": predictions["prob_quarter_finalist"],
        "prob_semi_finalist":    predictions["prob_semi_finalist"],
        "prob_finalist":         predictions["prob_finalist"],
        "prob_winner":           predictions["prob_winner"],
    })

    output_path = "world_cup_2026_predictions.csv"
    output_df.to_csv(output_path, index=False)
    print(f"\n  Saved predictions -> {output_path}")

    # ──────────────────────────────────────────────
    # 5. Print Top 10 leaderboard by prob_winner
    # ──────────────────────────────────────────────
    top10 = (
        output_df
        .sort_values("prob_winner", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )
    top10.index += 1  # 1-indexed rank

    print("\n")
    print("=" * 70)
    print("           TOP 10 TEAMS — 2026 WORLD CUP PREDICTIONS")
    print("=" * 70)
    print()
    print(f"| {'Rank':>4} | {'Team':<15} | {'Continent':<15} | {'QF':>8} | {'SF':>8} | {'Final':>8} | {'Winner':>8} |")
    print(f"|{'-'*6}|{'-'*17}|{'-'*17}|{'-'*10}|{'-'*10}|{'-'*10}|{'-'*10}|")

    for rank, row in top10.iterrows():
        print(
            f"| {rank:>4} "
            f"| {row['team']:<15} "
            f"| {row['continent']:<15} "
            f"| {row['prob_quarter_finalist']:>8.4f} "
            f"| {row['prob_semi_finalist']:>8.4f} "
            f"| {row['prob_finalist']:>8.4f} "
            f"| {row['prob_winner']:>8.4f} |"
        )

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
