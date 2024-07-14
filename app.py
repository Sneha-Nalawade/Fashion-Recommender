# import sys
# sys.path.append('D:/Fashion-Recommender/recommender_system')

# from flask import Flask, jsonify, render_template
# # import recommender_system
from recommender_system.recommender import predict_ratings  # Assuming predict_ratings function is defined in recommender.py

# app = Flask(__name__, template_folder='public')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/predict/<string:user_id>', methods=['GET'])
# def predict(user_id):
#     predicted_ratings = predict_ratings(user_id)
#     return jsonify(predicted_ratings.to_dict())

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__, template_folder='public')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
# db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict/<string:user_id>', methods=['GET'])
@login_required
def predict(user_id):
    predicted_ratings = predict_ratings(user_id)
    return jsonify(predicted_ratings.to_dict())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
