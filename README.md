<<<<<<< HEAD
# Fake News & Scam Detector

A production-ready Streamlit web application that detects fake news and scam-like content from raw text or a live URL using a hybrid NLP approach:

- Transformers-based text classification when a Hugging Face model is available
- Rule-based scam phrase detection for explainability and resilience
- URL scraping with BeautifulSoup
- WhatsApp-style chat UI with confidence scores, highlighted indicators, and human-readable explanations

## Features

- Text detection: classify pasted content as `Fake`, `Real`, or `Scam`
- URL detection: scrape article text from a web page and analyze it
- Suspicious phrase highlighting:
  - Red = high-risk terms
  - Yellow = moderate-risk terms
- Explainability:
  - trigger phrases
  - reason summary
  - confidence score
- Modern mobile-friendly Streamlit interface
- Loading states and error handling

## Project Structure

```text
.
|-- app.py
|-- requirements.txt
|-- README.md
`-- src
    |-- __init__.py
    |-- config.py
    |-- explain.py
    |-- highlighting.py
    |-- modeling.py
    |-- scraper.py
    `-- ui.py
```

## Setup

1. Create a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
streamlit run app.py
```

## Model Notes

The app defaults to the Hugging Face model in `src/config.py`:

```python
DEFAULT_MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
```

You can swap this for a custom fake-news or scam classifier with:

```powershell
$env:DETECTOR_MODEL_NAME="your-huggingface-model"
streamlit run app.py
```

For best production results, point this to a model you have specifically fine-tuned for:

- fake news detection
- misinformation detection
- scam / phishing / spam classification

## Production Recommendations

- Replace the default model with a domain-tuned classifier
- Add request caching or a job queue for high traffic
- Add observability and structured logging
- Add a moderation layer for hostile or oversized inputs
- Add unit tests for trigger extraction and scoring

## Example Inputs

- Scam-like:
  - `Urgent! Your account will be closed today. Verify your account now to claim your bonus.`
- Fake-news-like:
  - `Shocking secret report proves everything you know is false.`
- Safer:
  - `The city council approved the budget after a public vote on Tuesday evening.`
=======
# fake-news-detector
>>>>>>> 00a4e489e07ce42b791c4e4dc3ef439b06611ee4
