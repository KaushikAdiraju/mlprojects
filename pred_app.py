from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.prediction import CustomData, PredictPipeline

application = Flask(__name__)
app = application

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == "GET":
        print("GET request received.")
        return render_template('prediction.html', results=None)

    else:
        print("POST request received.")

        try:
            # Step 1: Capture Form Data
            print("Form data received:", request.form)

            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=float(request.form.get('reading_score')),
                writing_score=float(request.form.get('writing_score'))
            )

            # Step 2: Convert to DataFrame
            pred_df = data.convert_dataframe()
            print("Converted DataFrame:\n", pred_df)

            # Step 3: Load Model & Predict
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            print("Prediction Results:", results)

            # Step 4: Return Prediction in Template
            return render_template('prediction.html', results=results[0].round(2))

        except Exception as e:
            # Print the error in terminal and return plain text response
            print("Error occurred:", e)
            return f"An error occurred: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
    predict()
