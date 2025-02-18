from flask import Flask, render_template
from routes.auth import auth
from routes.services import services

app = Flask(__name__)
app.secret_key = 'e0b7572c14324f5c6eb34e7edde62069'
app.register_blueprint(auth)
app.register_blueprint(services)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)