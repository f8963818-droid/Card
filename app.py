from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os, urllib.parse, re

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-secret-before-deploying')
DB = os.path.join(os.path.dirname(__file__), 'cardvault.db')
WHATSAPP_NUMBER = '918115195515'  # India country code + number, digits only

CARDS = [
    {'id': 1, 'name': 'Obsidian Elite', 'kind': 'Membership', 'price': 499, 'tone': 'obsidian', 'desc': 'Minimal black finish with a premium metallic accent.'},
    {'id': 2, 'name': 'Aurora Gift', 'kind': 'Gift Card', 'price': 799, 'tone': 'aurora', 'desc': 'A colourful gift-card design for special occasions.'},
    {'id': 3, 'name': 'Royal Sapphire', 'kind': 'Membership', 'price': 999, 'tone': 'sapphire', 'desc': 'Deep sapphire styling with an elegant finish.'},
    {'id': 4, 'name': 'Rose Gold Club', 'kind': 'Membership', 'price': 699, 'tone': 'rose', 'desc': 'Warm rose-gold look for a distinctive membership.'},
]

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with db() as con:
        con.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL)')
        con.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, card_id INTEGER NOT NULL, utr TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'pending_review', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

@app.context_processor
def inject_user():
    return {'current_user': session.get('username')}

@app.route('/')
def home():
    return render_template('index.html', cards=CARDS)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if len(username) < 3 or len(password) < 8:
            flash('Username must be 3+ characters and password at least 8 characters.', 'error')
            return render_template('auth.html', mode='register')
        try:
            with db() as con:
                con.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, generate_password_hash(password)))
            flash('Account created. Please sign in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('That username is already taken.', 'error')
    return render_template('auth.html', mode='register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        with db() as con:
            user = con.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        flash('Incorrect username or password.', 'error')
    return render_template('auth.html', mode='login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/buy/<int:card_id>')
def buy(card_id):
    if 'user_id' not in session:
        flash('Please sign in before starting an order.', 'error')
        return redirect(url_for('login'))
    card = next((c for c in CARDS if c['id'] == card_id), None)
    if not card:
        return redirect(url_for('home'))
    return render_template('checkout.html', card=card)

@app.route('/payment/submit/<int:card_id>', methods=['POST'])
def submit_payment(card_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    card = next((c for c in CARDS if c['id'] == card_id), None)
    utr = request.form.get('utr', '').strip()
    if not card or not re.fullmatch(r'[A-Za-z0-9-]{8,30}', utr):
        flash('Enter a valid UTR/reference number (8–30 letters or numbers).', 'error')
        return redirect(url_for('buy', card_id=card_id))
    with db() as con:
        cur = con.execute('INSERT INTO orders (user_id, card_id, utr, status) VALUES (?, ?, ?, ?)',
                           (session['user_id'], card_id, utr, 'pending_review'))
        order_id = cur.lastrowid
    return render_template('order_pending.html', card=card, order_id=order_id, utr=utr)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
