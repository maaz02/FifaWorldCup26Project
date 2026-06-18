import pandas as pd
import os

def main():
    train_path = 'train.csv'
    test_path = 'test.csv'

    print("==================================================")
    print("           DATASET EXPLORATION SUMMARY            ")
    print("==================================================")

    # Load datasets safely
    train_df = None
    if not os.path.exists(train_path):
        print(f"Warning: '{train_path}' not found in the current directory.")
    else:
        train_df = pd.read_csv(train_path)
    
    test_df = None
    if not os.path.exists(test_path):
        print(f"Warning: '{test_path}' not found in the current directory.")
    else:
        test_df = pd.read_csv(test_path)

    # 1. Exact shape of both DataFrames
    print("\n--- 1. Data Shapes ---")
    if train_df is not None:
        print(f"Train Dataset: {train_df.shape[0]} rows, {train_df.shape[1]} columns")
    if test_df is not None:
        print(f"Test Dataset:  {test_df.shape[0]} rows, {test_df.shape[1]} columns")

    # 2. Data types of all columns
    print("\n--- 2. Data Types ---")
    if train_df is not None:
        print("\n[ Train Dataset ]")
        print(train_df.dtypes.to_string())
    if test_df is not None:
        print("\n[ Test Dataset ]")
        print(test_df.dtypes.to_string())

    # 3. Summary of missing (null) values
    print("\n--- 3. Missing Values Summary ---")
    if train_df is not None:
        print("\n[ Train Dataset - Missing Values ]")
        train_missing = train_df.isnull().sum()
        train_missing = train_missing[train_missing > 0]
        if train_missing.empty:
            print("No missing values found.")
        else:
            print(train_missing.to_string())
            
    if test_df is not None:
        print("\n[ Test Dataset - Missing Values ]")
        test_missing = test_df.isnull().sum()
        test_missing = test_missing[test_missing > 0]
        if test_missing.empty:
            print("No missing values found.")
        else:
            print(test_missing.to_string())

    # 4. First 3 rows of the test dataset
    print("\n--- 4. First 3 Rows of Test Dataset ---")
    if test_df is not None:
        print(test_df.head(3).to_string())

    print("\n==================================================")

if __name__ == "__main__":
    main()
