from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # redirect here if login required

# Database model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# WTForm classes
class RegisterForm(FlaskForm):
    user_field = StringField(validators=[InputRequired(), Length(min=4, max=150)], render_kw={"placeholder": "Username"})
    pass_field = PasswordField(validators=[InputRequired(), Length(min=4, max=150)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_user_field(self, user_field):
        existing_user = User.query.filter_by(username=user_field.data).first()
        if existing_user:
            raise ValidationError("That username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    user_field = StringField(validators=[InputRequired(), Length(min=4, max=150)], render_kw={"placeholder": "Username"})
    pass_field = PasswordField(validators=[InputRequired(), Length(min=4, max=150)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.pass_field.data, method='pbkdf2:sha256')
        new_user = User(username=form.user_field.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.user_field.data).first()
        if user and check_password_hash(user.password, form.pass_field.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password", "danger")
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
