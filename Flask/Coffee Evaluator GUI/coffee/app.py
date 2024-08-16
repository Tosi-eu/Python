from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import pandas as pd
import joblib

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

dv_dt_loaded = joblib.load('uploads/dv_dt.joblib')
model_dt_loaded = joblib.load('uploads/model_dt.joblib')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='Nenhum arquivo enviado')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', error='Nome de arquivo inválido')

        if file and file.filename.rsplit('.', 1)[1].lower() == 'json':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            df_test = pd.read_json(file_path)
            X_test = dv_dt_loaded.transform(df_test.to_dict(orient="records"))
            predictions = model_dt_loaded.predict(X_test)
            predicted_quality = ['Bom' if pred == 1 else 'Indesejado' for pred in predictions]

            return render_template('index.html', predicted_quality=predicted_quality)
        else:
            return render_template('index.html', error='Apenas arquivos JSON são permitidos')

    return render_template('index.html', predicted_quality=None, error=None)

if __name__ == '__main__':
    app.run(debug=True)
