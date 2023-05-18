from flask import Flask, request, jsonify, make_response, redirect, url_for
import jwt
import datetime
from functools import wraps
from config import db
from models import User
from app import app


with app.app_context():
    db.create_all()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing'}), 403 
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view this'})

@app.route('/protected')
@token_required
def protected():

    token = request.args.get('token')

    if not token:
        return jsonify({'message': 'Token is missing'}), 403 
        
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token is invalid'}), 403
    return jsonify({'message': 'This is only available for people with a valid token'})

# @app.route('/login')
# def login():
#     auth = request.authorization

#     if auth and auth.password == 'secret':
#         token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, app.config['SECRET_KEY'], algorithm='HS256')
#         return jsonify({'token': token})
        
#     return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:
        return jsonify({'message': 'Invalid username or password'}), 401

    token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, app.config['SECRET_KEY'], algorithm='HS256')

    redirect_url = url_for('welcome', token=token)  # Ajoute le token à l'URL de redirection
    return redirect(redirect_url)
    # return jsonify({'token': token})
    # return redirect("/welcome")



@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})


@app.route('/welcome')
@token_required
def welcome():

    token = request.args.get('token')

    if not token:
        return jsonify({'message': 'Token is missing'}), 403 
        
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token is invalid'}), 403
   
    return jsonify({"message":"You are login"})


if __name__ == '__main__':
    app.run(debug=True)
