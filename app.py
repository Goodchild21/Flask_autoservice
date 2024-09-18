from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)
login_manager = LoginManager(app)



class User(db.Model, UserMixin):
    __tablename__ = 'sing_client'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    middle_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(30))
    log_in = db.Column(db.String(30), unique=True, nullable=False)
    psw = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f"{self.first_name}"


@login_manager.user_loader
def load_user(log_in):
    # return  User.query.get(id)
    return db.session.get(User, log_in)



# *********************************PAGES********************************
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

@app.route('/sing_up_done')
def sing_up_done():
    return render_template('sing_up_done.html')



# ******************************REGISTRATION*****************************
@app.route('/sing_up', methods=['POST','GET'])
def sing_up():
    if request.method == "POST":
        # first_name = request.form['first_name']
        # middle_name = request.form['middle_name']
        # last_name = request.form['last_name']
        # email = request.form['email']
        # log_in = request.form['log_in']
        # psw = generate_password_hash(request.form.get('psw'))
        #
        # sing_client = Client(first_name=first_name, middle_name=middle_name, last_name=last_name, email=email,
        #                 log_in=log_in, psw=psw)

        user = User(
            first_name = request.form.get('first_name'),
            middle_name = request.form.get('middle_name'),
            last_name = request.form.get('last_name'),
            email = request.form.get('email'),
            log_in = request.form.get('log_in'),
            psw = generate_password_hash(request.form.get('psw'))
        )

        try:
            db.session.add(user)
            db.session.commit()
            # login_user(user)
            message='Вы зарегистрированы'
            return render_template('sing_up_done.html', message=message)
        except:
            message ='Произошла ошибка!!!'
            return render_template('sing_up_done.html', message=message)
    else:
        return render_template('sing_up.html')



# ***************************LOGIN****************************
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = db.session.query(User).filter_by(log_in=request.form.get('log_in')).first()

        if user is None:
            message = 'Ты тут чужой!!!'
            return render_template('sing_up_done.html', message=message)
        elif not check_password_hash(user.psw, request.form.get('psw')):
            message = 'Не праведный пароль!!!'
            return render_template('sing_up_done.html', message=message)
        elif check_password_hash(user.psw, request.form.get('psw')):
            message=f'Шалом, {user}!'
            login_user(user)
            return render_template('sing_up_done.html', message=message)

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')



# ================================OFFICE================================
class FeedBackOffice(db.Model):
    __tablename__ = 'client_office'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String, db.ForeignKey('sing_client.id'))
    brand = db.Column(db.String)
    model = db.Column(db.String)
    service = db.Column(db.String)



@app.route('/office', methods=['POST', 'GET'])
@login_required
def office():
    if request.method == 'POST':
        feedback_office = FeedBackOffice(
            phone=request.form.get('phone'),
            brand=request.form.get('brand'),
            model=request.form.get('model'),
            service=request.form.get('service'),
        )
        #
        name = db.session.query(User).filter_by('log_in').first()


        try:
            db.session.add(feedback_office)
            db.session.commit()
            message = 'OFFICE UPDATE'
            return render_template('office_up_done.html', message=message)
        except:
            message = 'Произошла ошибка!!!'
            return render_template('office_up_done.html', message=message)
    else:
        #
        return render_template('office.html', first_name=name)




# @login_required
# @app.route('/super_secret')
# def profile():
#     return f"User {current_user.username}"


if __name__ == '__main__':
    app.run(debug=True)
