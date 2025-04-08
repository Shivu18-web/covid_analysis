from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import base64

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def analyze_covid_data(filepath):
    df = pd.read_csv(filepath)
    summary = df.describe().to_html(classes='table table-striped table-bordered')

    # Plotting the data
    plt.figure(figsize=(8, 6))
    df.plot(x='Date', y=['Confirmed', 'Recovered', 'Deaths'], marker='o')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('COVID-19 Data Analysis')
    plt.legend(loc='best')

    # Save plot to memory
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    return summary, plot_url


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            summary, plot_url = analyze_covid_data(filepath)
            return render_template('results.html', summary=summary, plot_url=plot_url)
    return render_template('upload.html')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/more')
def more():
    return render_template('more.html')


if __name__ == '__main__':
    app.run(debug=True)
