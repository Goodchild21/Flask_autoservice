from enum import unique

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
# from dash_application import create_dash_application
# from sqlalchemy import create_engine


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)


# create_dash_application(app)

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


class FeedBackOffice(db.Model):
    __tablename__ = 'client_office'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('sing_client.id'))
    phone = db.Column(db.String(13), unique=True)
    brand = db.Column(db.Text)
    model = db.Column(db.Text)
    # service = db.Column(db.String(30))


# db.create_all()


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
            message=f'Шалом, {user}!' #Выдаст first_name, т.к. в repr'е только имя
            login_user(user)
            return render_template('sing_up_done.html', message=message)

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')



# ================================OFFICE================================
@app.route('/office', methods=['POST', 'GET'])
@login_required
def office():
    user = db.session.query(User).filter_by(log_in = current_user.log_in).one()
    first_name = user.first_name
    middle_name = user.middle_name
    last_name = user.last_name
    email = user.email


    if request.method == 'POST':
        feedback_office = FeedBackOffice(
            user_id=user.id,
            phone=request.form.get('phone'),
            brand=request.form.get('brand'),
            model=request.form.get('model')
            # service=request.form.get('service')
            )
        db.session.add(feedback_office)
        db.session.commit()

        return render_template('office.html',
                               first_name=first_name,
                               middle_name=middle_name,
                               last_name=last_name,
                               email=email,

                               phone=feedback_office.phone,
                               brand=feedback_office.brand,
                               model=feedback_office.model)


# ??????? проблема при поиске в таблице и проблема при создании нового узера(ошибка)
    if db.session.query(FeedBackOffice).filter_by(user_id = current_user.id):
        feedback = db.session.query(FeedBackOffice).filter_by(user_id = current_user.id).one()
        phone = feedback.phone,
        brand = feedback.brand,
        model = feedback.model

        return render_template('office.html',
                                    first_name=first_name,
                                    middle_name=middle_name,
                                    last_name=last_name,
                                    email=email,
                                    phone=phone,
                                    brand=brand,
                                    model=model)

    return render_template('office.html',
                           first_name=first_name,
                           middle_name=middle_name,
                           last_name=last_name,
                           email=email)


    # @login_required
# @app.route('/super_secret')
# def profile():
#     return f"User {current_user.username}"


if __name__ == '__main__':
    app.run(debug=True)
