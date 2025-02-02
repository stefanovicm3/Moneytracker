from flask import Flask, request, jsonify, make_response,url_for
from functools import wraps
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash
import random
import string
import os
from flask_mail import Message, Mail
import jwt
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True, allow_headers=["Content-Type", "Authorization"])

# Tajni ključ za JWT
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback_key_ako_nema_varijable')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'proba@proba.com'  
app.config['MAIL_PASSWORD'] = 'proba-sifra123'  
mail = Mail(app)

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",       
        user="root",            
        password="",            
        database="personal_finance"  
    )
    return connection

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401  
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['id']
        except Exception as e:
            return jsonify({'error': 'Token is invalid'}), 401  
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated_function


def admin_required(f):
    @wraps(f)
    @token_required
    def decorated_function(current_user_id, *args, **kwargs):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT role FROM users WHERE id = %s", (current_user_id,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and user['role'] == 'admin':  
            return f(*args, **kwargs)
        else:
            return jsonify({'error': 'Access forbidden'}), 403  
    
    return decorated_function

##############################################-- Login -- ##################################################################
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'error': 'Neispravan Content-Type, očekuje se JSON'}), 400

    data = request.get_json()
    print("Prijavljeni podaci:", data)  

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Nedostaju email ili lozinka'}), 400

    email = data['email']
    lozinka = data['password']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    korisnik = cursor.fetchone()
    print("Korisnik pronađen:", korisnik)  

    cursor.close()
    connection.close()

    if korisnik and check_password_hash(korisnik['lozinka'], lozinka):
        token = jwt.encode({
            'id': korisnik['id'],
            'email': korisnik['email'],
            'role': korisnik['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'message': 'Login successful', 'token': token,'user_id': korisnik['id']}), 200

    return jsonify({'error': 'Invalid email or password'}), 400

@app.route('/logout', methods=["POST"])
@token_required
def logout(current_user_id):
    
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/register', methods=["POST"])
def register():
    data = request.get_json()

    if not data or 'email' not in data or 'lozinka' not in data:
        return jsonify({'error': 'Nedostaju email ili lozinka'}), 400

    email = data['email']
    lozinka = data['lozinka']

    if not email or not lozinka:
        return jsonify({'error': 'Email i lozinka ne mogu biti prazni'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    # Proveri da li email već postoji
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        connection.close()
        return jsonify({'error': 'Email je već registrovan'}), 400

    hashed_password = generate_password_hash(lozinka)

    try:
        cursor.execute(
            "INSERT INTO users (email, lozinka, role) VALUES (%s, %s, %s)",
            (email, hashed_password, 'user')  
        )
        connection.commit()

        payload = {
            'email': email,
            'role': 'user',  
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'message': 'Registration successful', 'token': token}), 201  
    except mysql.connector.Error as err:
        print(f"Greška u bazi podataka: {err}")  
        return jsonify({'error': 'Greška pri registraciji, pokušajte ponovo'}), 500  
    finally:
        cursor.close()
        connection.close()

@app.route('/forgot-password', methods=["POST"])
def forgot_password():
    email = request.json.get('email')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    korisnik = cursor.fetchone()

    if korisnik:
        # Generišemo jedinstveni token za reset lozinke
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
        
        # Spremimo token u bazu
        cursor.execute("UPDATE users SET reset_token = %s WHERE email = %s", (token, email))
        connection.commit()

        # Kreirajte URL za resetovanje lozinke
        reset_url = url_for('reset_password', token=token, _external=True)

        # Pošaljite email sa linkom za reset lozinke
        msg = Message("Password Reset Request", recipients=[email])
        msg.body = f"To reset your password, click the following link: {reset_url}"
        mail.send(msg)
        
        return jsonify({'message': 'Check your email for a password reset link.'}), 200

    return jsonify({'error': 'Email not found in our system.'}), 404

@app.route('/reset-password/<token>', methods=["POST"])
def reset_password(token):
    new_password = request.json.get('new_password')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Proverite da li je token validan
    cursor.execute("SELECT * FROM users WHERE reset_token = %s", (token,))
    korisnik = cursor.fetchone()

    if not korisnik:
        return jsonify({'error': 'Invalid or expired token.'}), 400  # Bad request

    hashed_password = generate_password_hash(new_password)
    
    # Ažuriranje lozinke i brisanje tokena iz baze
    cursor.execute("UPDATE users SET lozinka = %s, reset_token = NULL WHERE reset_token = %s", 
                   (hashed_password, token))
    connection.commit()
    
    return jsonify({'message': 'Your password has been reset successfully. You can now log in.'}), 200

##############################################-- Korisnici (main page) -- ##################################################################
@app.route('/korisnici', methods=['GET'])
@token_required
def render_korisnici(current_user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    
    cursor.execute("SELECT SUM(iznos) AS ukupno_prihodi FROM korisnici WHERE type = 'prihod' AND user_id = %s", (current_user_id,))
    prihod = cursor.fetchone()['ukupno_prihodi'] or 0

    
    cursor.execute("SELECT SUM(iznos) AS ukupno_rashodi FROM korisnici WHERE type = 'rashod' AND user_id = %s", (current_user_id,))
    rashod = cursor.fetchone()['ukupno_rashodi'] or 0

    
    trenutno_stanje = prihod - rashod  

    
    cursor.execute("SELECT * FROM korisnici WHERE user_id = %s", (current_user_id,))
    korisnici = cursor.fetchall()

    cursor.close()
    connection.close()

    
    prihod = "{:,.0f}".format(prihod).replace(",", ".")
    rashod = "{:,.0f}".format(rashod).replace(",", ".")
    trenutno_stanje = "{:,.0f}".format(trenutno_stanje).replace(",", ".")

    
    for korisnik in korisnici:
        korisnik['iznos'] = "{:,.0f}".format(korisnik['iznos']).replace(",", ".")

    return jsonify({
        'prihod': prihod,
        'rashod': rashod,
        'trenutno_stanje': trenutno_stanje,
        'korisnici': korisnici
    }), 200

@app.route('/dodaj-novi', methods=["POST"])
@token_required
def dodaj_novi(current_user_id):
    forma = request.json
    naziv = forma['naziv']
    iznos = float(forma['iznos'])
    tip = forma['tip']

    if tip == 'rashod':
        iznos = iznos

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO korisnici (naziv, iznos, type, user_id) VALUES (%s, %s, %s, %s)",
            (naziv, iznos, tip, current_user_id)  
        )
        connection.commit()
        return jsonify({'message': 'Successfully added new record'}), 201  

    except mysql.connector.Error as err:
        return jsonify({'error': f"Database error: {err}"}), 500  

    finally:
        cursor.close()
        connection.close()

@app.route('/korisnik_pregled/<int:id>', methods=['GET'])
@token_required
def korisnik_pregled(current_user_id, id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM korisnici WHERE id = %s AND user_id = %s", (id, current_user_id))
        korisnik = cursor.fetchone()

        cursor.close()
        connection.close()

        if not korisnik:
            return jsonify({'error': 'Korisnik nije pronađen ili nemate pristup'}), 404  

        return jsonify(korisnik), 200  

    except Exception as e:
        return jsonify({'error': f"Error fetching korisnik data: {e}"}), 500  

@app.route('/korisnik_brisanje/<int:id>', methods=["DELETE"])
@token_required
def korisnik_brisanje(current_user_id, id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "DELETE FROM korisnici WHERE id = %s AND user_id = %s"  
        cursor.execute(query, (id, current_user_id))
        connection.commit()

        return jsonify({'message': 'Successfully deleted record'}), 200  
    except mysql.connector.Error as err:
        return jsonify({'error': f"Error during deletion: {str(err)}"}), 500  
    finally:
        cursor.close()
        connection.close()

@app.route('/korisnik_izmena/<int:id>/izmeni', methods=["POST"])
@token_required
def korisnik_izmena_post(current_user_id, id):
    forma = request.json
    naziv = forma['naziv']
    iznos = float(forma['iznos'])
    tip = forma['type']

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "UPDATE korisnici SET naziv = %s, iznos = %s, type = %s WHERE id = %s AND user_id = %s"
        cursor.execute(query, (naziv, iznos, tip, id, current_user_id))  
        connection.commit()

        return jsonify({'message': 'Successfully updated record'}), 200  
    except mysql.connector.Error as err:
        return jsonify({'error': f"Error during update: {str(err)}"}), 500  
    finally:
        cursor.close()
        connection.close()

@app.route('/korisnik_izmena/<int:id>/preuzmi', methods=["GET"])
@token_required
def korisnik_izmena_get(current_user_id, id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = "SELECT * FROM korisnici WHERE id = %s AND user_id = %s"
        cursor.execute(query, (id, current_user_id))  
        korisnik = cursor.fetchone()

        if not korisnik:
            return jsonify({'error': 'Transakcija nije pronađena'}), 404

        return jsonify(korisnik), 200  
    except mysql.connector.Error as err:
        return jsonify({'error': f"Greška prilikom preuzimanja podataka: {str(err)}"}), 500
    finally:
        cursor.close()
        connection.close()


##############################################-- USERS ALL -- ##################################################################


@app.route('/users', methods=['GET'])
@token_required
@admin_required
def render_users(current_user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        
        cursor.execute("SELECT id, email, role FROM users")
        users = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(users), 200  

    except Exception as e:
        print(f"Greška pri dohvatanju korisnika: {e}")
        return jsonify({'error': f"Error: {e}"}), 500  

@app.route('/users/<int:id>', methods=['GET'])
@token_required
@admin_required
def get_user(current_user_id, id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT id, email, role FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            return jsonify(user), 200  
        else:
            return jsonify({'error': 'User not found'}), 404  

    except Exception as e:
        return jsonify({'error': f"Error: {e}"}), 500  
    
@app.route('/edit_user/<int:id>', methods=['POST'])
@token_required
@admin_required
def edit_user(current_user_id, id):
    data = request.json

    email = data['email']
    password = data['password']
    role = data['role']

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE users SET email = %s, lozinka = %s, role = %s WHERE id = %s
        """, (email, password, role, id))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'User updated successfully'}), 200  

    except Exception as e:
        return jsonify({'error': f"Error while updating user: {e}"}), 500  

@app.route('/add_user', methods=['POST'])
@token_required
@admin_required
def add_user(current_user_id):
    data = request.json

    email = data['email']
    lozinka = data['password']
    role = data['role']

    try:
        
        hashed_password = generate_password_hash(lozinka, method='pbkdf2:sha256')

        connection = get_db_connection()
        cursor = connection.cursor()

        
        cursor.execute("INSERT INTO users (email, lozinka, role) VALUES (%s, %s, %s)",
                       (email, hashed_password, role))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'User added successfully'}), 201  

    except Exception as e:
        return jsonify({'error': f"Error while adding user: {e}"}), 500  



@app.route('/delete_user/<int:id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(current_user_id, id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

       
        delete_query = "DELETE FROM users WHERE id = %s"
        print(f"Executing query: {delete_query} with id={id}")
        cursor.execute(delete_query, (id,))
        connection.commit()

        
        select_query = "SELECT * FROM korisnici WHERE user_id = %s"
        print(f"Executing query: {select_query} with user_id={id}")
        cursor.execute(select_query, (id,))
        result = cursor.fetchall()

        
        if result:
            print(f"Povezani podaci nisu obrisani: {result}")
            return jsonify({'error': 'Povezani podaci nisu obrisani, proverite stranacni ključ.'}), 500

        cursor.close()
        connection.close()

        return jsonify({'message': 'User deleted successfully'}), 200  

    except Exception as e:
        
        print(f"Greška prilikom brisanja korisnika: {e}")
        return jsonify({'error': f"Greška prilikom brisanja korisnika: {e}"}), 500  




##############################################-- Budzet i potrosnja -- ##################################################################

@app.route('/budzet', methods=['GET'])
@token_required
def render_budzet(current_user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        
        cursor.execute("SELECT SUM(iznos) AS ukupni_budzet FROM budzeti WHERE korisnik_id = %s", (current_user_id,))
        ukupni_budzet = cursor.fetchone()['ukupni_budzet'] or 0
        ukupni_budzet = int(ukupni_budzet)

        
        cursor.execute("""SELECT SUM(iznos) AS ukupna_potrosnja FROM potrosnja WHERE korisnik_id = %s""", (current_user_id,))
        ukupna_potrosnja = cursor.fetchone()['ukupna_potrosnja'] or 0
        ukupna_potrosnja = int(ukupna_potrosnja)

        
        cursor.execute("SELECT * FROM budzeti WHERE korisnik_id = %s", (current_user_id,))
        budzeti = cursor.fetchall()

        cursor.execute("""SELECT * FROM potrosnja WHERE korisnik_id = %s ORDER BY id DESC LIMIT 5""", (current_user_id,))
        potrosnje = cursor.fetchall()

        cursor.close()
        connection.close()

        
        return jsonify({
    'ukupni_budzet': format(ukupni_budzet, ',.0f').replace(',', '.'), 
    'ukupna_potrosnja': format(ukupna_potrosnja, ',.0f').replace(',', '.'), 
    'budzeti': [
        {'id': budzet['id'], 
         'kategorija': budzet['kategorija'], 
         'iznos': format(budzet['iznos'], ',.0f').replace(',', '.'), 
         'mesec': budzet['mesec'],  
         'godina': budzet['godina']}  
        for budzet in budzeti
    ],
    'potrosnje': [
        {'id': potrosnja['id'], 
         'kategorija': potrosnja['kategorija'], 
         'iznos': format(potrosnja['iznos'], ',.0f').replace(',', '.')} 
        for potrosnja in potrosnje
    ]
}), 200  

    except Exception as e:
        print(f"Greška pri dohvatanju budžeta: {e}")
        return jsonify({'error': f"Error: {e}"}), 500  

@app.route('/budzet/<int:id>', methods=['GET'])
@token_required
def get_budzet(current_user_id, id):  
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        
        cursor.execute("SELECT * FROM budzeti WHERE id = %s AND korisnik_id = %s", (id, current_user_id))
        budzet = cursor.fetchone()

        if not budzet:
            return jsonify({"error": "Budžet nije pronađen"}), 404

        cursor.close()
        connection.close()

        
        return jsonify({
            'id': budzet['id'],
            'kategorija': budzet['kategorija'],
            'iznos': format(budzet['iznos'], ',.0f').replace(',', '.'),  
            'mesec': budzet['mesec'],
            'godina': budzet['godina']
        }), 200  

    except Exception as e:
        print(f"Greška pri dohvatanju budžeta: {e}")
        return jsonify({'error': f"Error: {e}"}), 500  


@app.route('/budzet/dodaj', methods=['POST'])
@token_required
def dodaj_budzet(current_user_id):
    data = request.json

    
    if not all(key in data for key in ['kategorija', 'iznos', 'mesec', 'godina']):
        return jsonify({'error': 'Nedostaju obavezni podaci'}), 400  

    kategorija = data['kategorija']
    iznos = data['iznos']
    mesec = data['mesec']
    godina = data['godina']

    
    try:
        iznos = int(iznos)
        godina = int(godina)
    except ValueError:
        return jsonify({'error': 'Iznos i godina moraju biti brojevi'}), 400  

    
    if kategorija == 'nova_kategorija':
        if 'nova_kategorija' not in data or not data['nova_kategorija']:
            return jsonify({'error': 'Niste uneli novu kategoriju'}), 400  
        nova_kategorija = data['nova_kategorija']
        kategorija = nova_kategorija

        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT 1 FROM budzeti WHERE kategorija = %s AND korisnik_id = %s", (nova_kategorija, current_user_id))
            if cursor.fetchone():
                return jsonify({'error': 'Ova kategorija već postoji.'}), 400  

            
            cursor.close()
            connection.close()
        except Exception as e:
            return jsonify({'error': f"Greška pri proveri kategorije: {e}"}), 500  

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO budzeti (korisnik_id, kategorija, iznos, mesec, godina) VALUES (%s, %s, %s, %s, %s)",
            (current_user_id, kategorija, iznos, mesec, godina)
        )
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Budžet uspešno dodat'}), 201  

    except Exception as e:
        return jsonify({'error': f"Greška pri dodavanju budžeta: {e}"}), 500  



@app.route('/budzet/mesec/<string:mesec>/<int:godina>', methods=['GET'])
@token_required
def get_budzet_po_mesecu(current_user_id, mesec, godina):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        
        cursor.execute(
            "SELECT * FROM budzeti WHERE korisnik_id = %s AND mesec = %s AND godina = %s",
            (current_user_id, mesec, godina)
        )
        budzeti = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(budzeti), 200  

    except Exception as e:
        return jsonify({'error': f"Greška pri dohvatanju budžeta: {e}"}), 500  

@app.route('/budzet/izmeni/<int:id>', methods=['POST'])
@token_required
def izmeni_budzet(current_user_id, id):
    data = request.json

    kategorija = data['kategorija']
    iznos = int(data['iznos'])
    mesec = data['mesec']
    godina = int(data['godina'])

    
    if kategorija == 'nova_kategorija':
        nova_kategorija = data['nova_kategorija']
        kategorija = nova_kategorija

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE budzeti SET kategorija = %s, iznos = %s, mesec = %s, godina = %s WHERE id = %s",
            (kategorija, iznos, mesec, godina, id)
        )
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Budžet successfully updated'}), 200  

    except Exception as e:
        return jsonify({'error': f"Error updating budžet: {e}"}), 500  

@app.route('/kategorije', methods=['GET'])
@token_required
def get_kategorije(current_user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        
        cursor.execute("SELECT DISTINCT kategorija FROM budzeti WHERE korisnik_id = %s", (current_user_id,))
        kategorije = cursor.fetchall()

        cursor.close()
        connection.close()

        
        return jsonify([k['kategorija'] for k in kategorije]), 200  

    except Exception as e:
        print(f"Greška pri dohvatanju kategorija: {e}")
        return jsonify({'error': f"Error: {e}"}), 500  

@app.route('/sve-kategorije', methods=['GET'])
@token_required
def get_all_kategorije(current_user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        
        cursor.execute("SELECT DISTINCT kategorija FROM budzeti")
        kategorije = cursor.fetchall()

        cursor.close()
        connection.close()

        
        return jsonify([k['kategorija'] for k in kategorije]), 200  

    except Exception as e:
        print(f"Greška pri dohvatanju svih kategorija: {e}")
        return jsonify({'error': f"Error: {e}"}), 500  


@app.route('/budzet/obrisi/<int:id>', methods=['DELETE'])
@token_required
def obrisi_budzet(current_user_id, id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        
        cursor.execute("DELETE FROM potrosnja WHERE budzet_id = %s", (id,))

        cursor.execute("DELETE FROM budzeti WHERE id = %s", (id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Budžet successfully deleted'}), 200  

    except Exception as e:
        return jsonify({'error': f"Error deleting budžet: {e}"}), 500  

@app.route('/budzet/grafikon', methods=['GET'])
@token_required
def grafikon(current_user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        
        cursor.execute(""" 
            SELECT kategorija, 
                   SUM(CASE WHEN tip = 'budzet' THEN iznos ELSE 0 END) AS ukupni_budzet, 
                   SUM(CASE WHEN tip = 'potrosnja' THEN iznos ELSE 0 END) AS ukupna_potrosnja
            FROM (SELECT kategorija, iznos, 'budzet' AS tip FROM budzeti WHERE korisnik_id = %s
                  UNION ALL
                  SELECT kategorija, iznos, 'potrosnja' AS tip FROM potrosnja WHERE korisnik_id = %s) AS combined
            GROUP BY kategorija
        """, (current_user_id, current_user_id))

        budzeti = cursor.fetchall()

        kategorije = [budzet['kategorija'] for budzet in budzeti]
        budzet = [budzet['ukupni_budzet'] for budzet in budzeti]
        potrosnja = [budzet['ukupna_potrosnja'] for budzet in budzeti]

        cursor.close()
        connection.close()

        
        return jsonify({
            "kategorije": kategorije,
            "budzet": budzet,
            "potrosnja": potrosnja
        }), 200  

    except Exception as e:
        return jsonify({'error': f"Error fetching data for chart: {e}"}), 500  

@app.route('/budzet/potrosnja/<int:id>', methods=['POST'])
@token_required
def unesi_potrosnju(current_user_id, id):
    data = request.json

    
    if not current_user_id:
        return jsonify({'error': 'Korisnik nije prijavljen ili token nije validan.'}), 400  

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM users WHERE id = %s", (current_user_id,))
    user_exists = cursor.fetchone()[0]

    if not user_exists:
        return jsonify({'error': 'Korisnik sa tim ID-jem ne postoji u bazi.'}), 400  

    iznos_potrosnje = int(data['potroseno'])
    mesec = data['mesec']
    godina = int(data['godina'])
    kategorija = data['kategorija']

    try:
        cursor.execute(""" 
            INSERT INTO potrosnja (budzet_id, iznos, korisnik_id, mesec, godina, kategorija)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id, iznos_potrosnje, current_user_id, mesec, godina, kategorija))

        cursor.execute(""" 
            UPDATE users
            SET ukupna_potrosnja = ukupna_potrosnja + %s
            WHERE id = %s
        """, (iznos_potrosnje, current_user_id))

        cursor.execute(""" 
            UPDATE budzeti
            SET ukupna_potrosnja = ukupna_potrosnja + %s
            WHERE id = %s
        """, (iznos_potrosnje, id))

        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Potrošnja successfully added'}), 200  
    

    except Exception as e:
        return jsonify({'error': f"Error adding potrošnja: {e}"}), 500  


@app.route('/potrosnja/izmeni/<int:id>', methods=['PUT'])
@token_required
def izmeni_potrosnju(current_user_id, id):
    data = request.json

    
    if not current_user_id:
        return jsonify({'error': 'Korisnik nije prijavljen ili token nije validan.'}), 400  

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM potrosnja WHERE id = %s AND korisnik_id = %s", (id, current_user_id))
    potrosnja = cursor.fetchone()

    if not potrosnja:
        return jsonify({'error': 'Potrošnja nije pronađena'}), 404  

    iznos = int(data['iznos'])
    mesec = data['mesec']
    godina = int(data['godina'])
    kategorija = data['kategorija']

    try:
        cursor.execute(""" 
            UPDATE potrosnja
            SET iznos = %s, mesec = %s, godina = %s, kategorija = %s
            WHERE id = %s
        """, (iznos, mesec, godina, kategorija, id))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Potrošnja successfully updated'}), 200  

    except Exception as e:
        return jsonify({'error': f"Error updating potrošnja: {e}"}), 500  

@app.route('/api/budzet/<int:id>/potrosnje', methods=['GET'])
@token_required
def get_potrosnje(current_user_id, id):   
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM potrosnja WHERE budzet_id = %s AND korisnik_id = %s", (id, current_user_id))
    potrosnje = cursor.fetchall()

    if not potrosnje:
        return jsonify({'error': 'Nema potrošnje za ovaj budžet.'}), 404

    return jsonify({'potrosnje': potrosnje}), 200

@app.route('/potrosnja/obrisi/<int:id>', methods=['POST'])
@token_required
def obrisi_potrosnju(current_user_id, id):
    
    if not current_user_id:
        return jsonify({'error': 'Korisnik nije prijavljen ili token nije validan.'}), 400  

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        
        cursor.execute("DELETE FROM potrosnja WHERE id = %s AND korisnik_id = %s", (id, current_user_id))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Potrošnja successfully deleted'}), 200  

    except Exception as e:
        return jsonify({'error': f"Error deleting potrošnja: {e}"}), 500  

if __name__ == '__main__':
    app.run(debug=True)