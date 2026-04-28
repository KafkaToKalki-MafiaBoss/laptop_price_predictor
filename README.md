# Laptop Price Predictor
NOTE: This is 1st draft of the project

An end-to-end machine learning web app that predicts laptop prices based on hardware specifications.
NOTE: This Model was built with data from 2017-2020 BUT this is first draft of the model. In further updates, this issue will be resolved.

## Features
- Predicts laptop prices using trained ML model
- Interactive web interface
- Deployed on Streamlit Cloud

## Tech Stack
- Python
- Pandas
- Scikit-learn
- Streamlit

## ML Workflow
1. Data preprocessing
2. Feature engineering
3. Model training
4. Prediction pipeline
5. Deployment

## Files
- app.py -> Streamlit application
- pipe.pkl -> Trained prediction pipeline
- df.pkl -> Processed data used in app
- Laptop_price_predictor.ipynb -> Model development notebook

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Live Demo
https://laptoppricepredictor-6gs7zd83stqbmvazm6lnqf.streamlit.app/

## Sample Inputs
Example:
- Company: Dell
- RAM: 16GB
- SSD: 512GB

Predicted Price:
₹XX,XXX

## Future Improvements
- Improved Dataset
- Better feature engineering
- More models comparison
- Improved UI/UX
- API deployment using Flask/FastAPI
