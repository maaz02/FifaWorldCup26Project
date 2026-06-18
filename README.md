# FIFA 26 Prediction

An open-source AI Predictor for the 2026 FIFA World Cup. This project features a full end-to-end Machine Learning pipeline paired with Large Language Models (LLMs) to generate dynamic, tactical scouting reports.

## Features

- **Machine Learning Models**: Random Forest classifiers to predict tournament progression probabilities (Quarter-Final, Semi-Final, Final, Winner) based on historical World Cup data.
- **LLM Scouting Reports**: Integrates with Groq API and Llama 3.1 to generate automated, narrative-driven tactical scouting reports tailored for each team.
- **FastAPI Backend**: Serves predictions and LLM reports through a fast, modern API.
- **Interactive UI**: A fully integrated frontend (Vanilla JS/Tailwind) that provides team analysis and a global leaderboard.
- **Streamlit Dashboard (Optional)**: Includes an alternative `app.py` for a rapid Streamlit-based UI.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MaazShaikh/Fifa-26-Prediction.git
   cd Fifa-26-Prediction
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables:**
   Copy `.env.example` to `.env` and configure your API keys:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Running the Application

**Run the Full-Stack FastAPI App:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
Navigate to `http://localhost:8000` to view the frontend interface.

**(Alternative) Run the Streamlit Dashboard:**
```bash
streamlit run app.py
```

## Data Scripts

- `explore_data.py`: Lightweight data exploration to inspect the shapes and missing values of the CSV files.
- `train_model.py`: Training pipeline using GroupKFold cross-validation to evaluate OOF ROC-AUC and feature importance.
- `predict_2026.py`: Inference script to generate `world_cup_2026_predictions.csv` using the full historical training data.
- `generate_reports.py`: Command-line script to test the Groq LLM integration and generate reports for the top teams.

## License

This project is open-source and available under the MIT License.
