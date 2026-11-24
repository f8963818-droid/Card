CARDVAULT — Flask + HTML + CSS + JavaScript

RUN IN TERMUX:
1. Install Termux from a trusted source.
2. Copy this folder into your phone's Download folder.
3. In Termux:
   pkg update -y && pkg upgrade -y
   pkg install python unzip -y
   termux-setup-storage
   cd ~/storage/downloads/cardvault
   pip install -r requirements.txt
   python app.py
4. Open Chrome: http://127.0.0.1:5000

EDIT PRODUCTS:
Open app.py and edit the CARDS list (name, kind, price, desc, tone).
WhatsApp contact is configured near the top of app.py as WHATSAPP_NUMBER.
Use country code + number, digits only. Current value: 918115195515.

SECURITY NOTES:
- Passwords are hashed and stored in SQLite.
- This starter app is for local testing and enquiry workflows, not production deployment.
- Before public hosting: set a strong random SECRET_KEY, enable HTTPS, add CSRF protection,
  rate limiting, secure cookie settings, backups, and proper production hosting.
- WhatsApp enquiry is not payment processing. Do not collect bank-card numbers, CVVs,
  OTPs, or banking passwords.
- Product designs are generic gift/membership concepts, not bank-issued payment cards.
