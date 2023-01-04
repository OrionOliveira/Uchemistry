# https://github.com/thisbejim/Pyrebase
import pyrebase as pb
import requests
import json
from Firebase import error_handling as err_hd

# Configurações do Banco de Dados
config = {
  "apiKey": "AIzaSyAA33tB4kOF8aDkFjjo_T_F-e8BsVnxbgA",
  "authDomain": "uchemistry-edd97.firebaseapp.com",
  "databaseURL": "https://uchemistry-edd97-default-rtdb.firebaseio.com",
  "projectId": "uchemistry-edd97",
  "storageBucket": "uchemistry-edd97.appspot.com",
  "messagingSenderId": "267090985449",
  "appId": "1:267090985449:web:31c9bfc35336912b6d8b78",
  "measurementId": "G-XQDEN833J9"
  }

firebase = pb.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# Function to Sign in
def sign_in_db(name, email, password, rpt_pssw):

  # Verifica se há erros com as informações que o usuário passou
  error = err_hd.signin_errors(name, email, password, rpt_pssw)
  
  # Se não houver erros, tenta criar o usuário e retorna o UID (Id do usuário)
  if error[0] == False:
      try:
        auth_token = auth.create_user_with_email_and_password(email, password)
        token_id = auth_token['idToken']

        UserID = auth.get_account_info(token_id)['users'][0]['localId']
        
        data = {
          'email': email,
          'name': name
        }

        a = db.child(f'Users/UIDs/{UserID}/Info').set(data, token_id)
        return UserID

      # Se não conseguir criar o usuário retorna o erro:
      except requests.HTTPError as e:
          error_json = e.args[1]
          error = json.loads(error_json)['error']['message']
          print(f'database.py[sign_in_db]: {error}')
          if error == 'INVALID_EMAIL':
            return 'inv_email'
          elif error == 'EMAIL_EXISTS':
            return 'email_exst'
          elif error == 'WEAK_PASSWORD':
            return 'wk_pssw'
  # Se houver erros de informações, a função retorna o erro para ser mostrado no front-end
  else:
    return error[1]

# Function to Login
def login_db(email, senha):
  if email == '':
    return 'email_emp'
  else:
    try:
      auth_token = auth.sign_in_with_email_and_password(email, senha)
      token_id = auth_token['idToken']
      # Return User ID
      UserID = auth.get_account_info(token_id)['users'][0]['localId']

      # Return User name
      users = db.child(f'Users/UIDs/{UserID}/Info').get()
      converted_to_dict = dict(users.val())
      user_name = converted_to_dict['name']
      token_id = auth.refresh(auth_token['refreshToken'])
      return user_name, UserID
      
    # Tratamento de erros
    except requests.HTTPError as e:
      error_json = e.args[1]
      error = json.loads(error_json)['error']['message']
      if error == 'EMAIL_NOT_FOUND':
        return 'email_nf'
      elif error == 'INVALID_EMAIL':
        return 'inv_email'
      elif error == 'MISSING_PASSWORD':
        return 'mss_pssw'
      elif error == 'INVALID_PASSWORD':
        return 'inv_pssw'
      else:
        print(f'database.py[login_db]: {error}')

# Function to Save products
def save_product(product_name, product_content, user_id, product_amount):
  qre = err_hd.qr_errors(product_name, product_content, product_amount)
  print(f'database.py[save_product]: {qre}')
  if qre[0] == False:
    data = {
      'description': f'{product_content}',
      'amount': f'{product_amount}',
      'name': f'{product_name}'
    }
    db.child('Users').child(f"{'UIDs'}").child(user_id).child('Products').push(data)
    db.child('Stock').child('PIDs').push(data)
    return 'Valid Product'
  else:
    return qre[1]

# Function to return stocked products
def stocked_products():
  all_products = db.child('Stock/PIDs').get()
  return_list = []
  for id in all_products.each():
    return_list.append(id.key())
  return return_list

# Function to return account information
def account_info():
  lista = []
  try:
    with open('Firebase/temp_id.json', 'r') as data:
      lista = json.load(data)
      user_info = db.child(f'Users/UIDs/{lista[0]}').get()
      for info in user_info.each():
        print(f'database.py[account_info](info.val()): {info.val()}')
    return info.val()
  except:
    raise Exception('Empty file')
