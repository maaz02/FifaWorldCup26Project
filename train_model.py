import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score, log_loss

def main():
    # ──────────────────────────────────────────────
    # Load data
    # ──────────────────────────────────────────────
    df = pd.read_csv("train.csv")

    # ──────────────────────────────────────────────
    # 1. Preprocessing
    # ──────────────────────────────────────────────

    # Impute missing squad_total_market_value_eur with
    # the median market value *within* each World Cup edition year,
    # so we don't mix different economic eras.
    median_by_version = df.groupby("version")["squad_total_market_value_eur"].transform("median")
    df["squad_total_market_value_eur"] = df["squad_total_market_value_eur"].fillna(median_by_version)

    # Define the 4 binary targets we want to predict independently
    targets = ["quarter_finalist", "semi_finalist", "finalist", "winner"]

    # Save the version column for GroupKFold groups before dropping it
    groups = df["version"].values

    # Drop non-numeric identifiers and targets from the feature set
    drop_cols = ["team", "continent"] + targets
    X = df.drop(columns=drop_cols)
    y = df[targets]

    feature_names = X.columns.tolist()

    # ──────────────────────────────────────────────
    # 2. GroupKFold Cross-Validation
    # ──────────────────────────────────────────────
    unique_versions = sorted(df["version"].unique())
    n_splits = len(unique_versions)  # leave-one-tournament-out
    gkf = GroupKFold(n_splits=n_splits)

    # Containers for out-of-fold probabilities
    oof_proba = {t: np.zeros(len(X)) for t in targets}
    # Store per-fold importances for 'winner' target
    winner_importances = np.zeros(len(feature_names))

    print("=" * 60)
    print("       MODEL TRAINING — GroupKFold Cross-Validation")
    print("=" * 60)
    print(f"\nTotal samples : {len(X)}")
    print(f"Features      : {len(feature_names)}")
    print(f"CV folds      : {n_splits}  (one per tournament edition)")
    print(f"Editions      : {unique_versions}")

    for fold_idx, (train_idx, val_idx) in enumerate(gkf.split(X, y, groups)):
        held_out_year = groups[val_idx[0]]
        print(f"\n  Fold {fold_idx + 1}/{n_splits} — held-out edition: {held_out_year}  "
              f"(train={len(train_idx)}, val={len(val_idx)})")

        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]

        for target in targets:
            y_train = y[target].iloc[train_idx]
            y_val   = y[target].iloc[val_idx]

            clf = RandomForestClassifier(
                n_estimators=300,
                max_depth=6,
                min_samples_leaf=4,
                class_weight="balanced",
                random_state=42,
                n_jobs=-1,
            )
            clf.fit(X_train, y_train)

            # Predicted probability for the positive class
            proba = clf.predict_proba(X_val)[:, 1]
            oof_proba[target][val_idx] = proba

            # Accumulate feature importances for 'winner'
            if target == "winner":
                winner_importances += clf.feature_importances_

    # Average the winner importances across folds
    winner_importances /= n_splits

    # ──────────────────────────────────────────────
    # 3. Evaluation — OOF ROC-AUC & Log-Loss
    # ──────────────────────────────────────────────
    print("\n")
    print("=" * 60)
    print("          OUT-OF-FOLD EVALUATION METRICS")
    print("=" * 60)
    print(f"\n{'Target':<20} {'ROC-AUC':>10} {'Log-Loss':>10}")
    print("-" * 42)

    for target in targets:
        y_true = y[target].values
        probas = oof_proba[target]

        auc  = roc_auc_score(y_true, probas)
        ll   = log_loss(y_true, probas)
        print(f"{target:<20} {auc:>10.4f} {ll:>10.4f}")

    # ──────────────────────────────────────────────
    # 4. Feature Importance — Top 5 for 'winner'
    # ──────────────────────────────────────────────
    print("\n")
    print("=" * 60)
    print("      TOP 5 FEATURES FOR PREDICTING 'winner'")
    print("=" * 60)

    importance_df = (
        pd.DataFrame({"feature": feature_names, "importance": winner_importances})
        .sort_values("importance", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )
    importance_df.index += 1  # 1-indexed ranking

    print(f"\n{'Rank':<6} {'Feature':<35} {'Importance':>10}")
    print("-" * 53)
    for rank, row in importance_df.iterrows():
        print(f"{rank:<6} {row['feature']:<35} {row['importance']:>10.4f}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
