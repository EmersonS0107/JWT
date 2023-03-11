from flask import Flask,request,jsonify,make_response,render_template,session
import jwt
from datetime import datetime,timedelta
from functools import wraps

app=Flask(__name__)
app.config['SECRET_KEY']='\x80o\x89\xb8);0b\xf5]\xa00'


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request/args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is mising!'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify ({'Alert!':'Invalid Token!'})
    return decorated


#home
@app.route('/')
def home():
    if not session.get('logged_in'):
       return render_template('login.html')
    else:
        return 'logged in currently!'

#public
@app.route('/public')
def public():
    return 'for public'

#Authenticated
@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your login page!'



#login
@app.route('/login',methods=['POST'])
def login():
    if request.form['username']and request.form['password']=='nosreme':
        session['logged_in']=True
        token = jwt.encode ({
            'user':request.form['username'],
            'expiration':str(datetime.utcnow() + timedelta(seconds=120))
        },
            app.config['SECRET_KEY'])
        return jsonify({'token':token.decode('utf-8')})
    else:
     return make_response('Unable to verify' , 403, {'WWW.Authenticate':'Basic realm:"Authentication failed!"'} )


if __name__ == "__main__":
    app.run(debug=True)