from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    direction = db.Column(db.String(25), nullable=False)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/prices')
def prices():
    return render_template('prices.html')

@app.route('/news')
def news():
    return render_template('news.html')


if __name__ == '__main__':
    app.run()
