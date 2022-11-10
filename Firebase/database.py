# https://github.com/thisbejim/Pyrebase
import pyrebase as pb
import requests
import json

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

# Função de cadastro
def sign_in_db(name, email, password, rpt_pssw):

# Tratamentos de erros
  p = ['gmail', 'outlook', 'hotmail', 'yahoo']

  # Campo nome vazio
  if name == '':
    return 'nm_emp'
  # Campo email vazio
  elif email == '':
    return 'email_emp'
  # Campo senha vazio
  elif password == '':
    return 'pssw_emp'
  # Campo repita a senha vazio
  elif rpt_pssw == '':
    return ''
  # Senhas não conferem
  elif password != rpt_pssw:
    return 'pssw_nc'
  # Senha tem menos de 6 caracteres
  elif len(password) < 6:
    return 'wk_pssw'

  # Tratar o erro de provedor de e-mail (senão o usuário poderá digitar "gmaail", por exemplo)
  #elif p[0] not in email or p[1] not in email or p[2] not in email or p[3] not in email:
  #  return 'inv_email'

  # Caso não haja nenhum erro na digitação das informações, tenta cadastrar
  else:
    try:
      auth_token = auth.create_user_with_email_and_password(email, password)
      token_id = auth_token['idToken']

      UserID = auth.get_account_info(token_id)['users'][0]['localId']
      
      data = {
        'email': email,
        'name': name
      }
      db.child('Users').child('UIDs').child(UserID).set(data)
      return UserID
    # Se houver erro no cadastro:
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        print(error)
        if error == 'INVALID_EMAIL':
          return 'inv_email'
        elif error == 'EMAIL_EXISTS':
          return 'email_exst'
        elif error == 'WEAK_PASSWORD':
          return 'wk_pssw'

# Função de Login
def login_db(email, senha):
  if email == '':
    return ''
  else:
    try:
      auth_token = auth.sign_in_with_email_and_password(email, senha)
      token_id = auth_token['idToken']
      # Retorna ID do usuário
      UserID = auth.get_account_info(token_id)['users'][0]['localId']

      # Retorna nome de usuário
      users = db.child('Users').child('UIDs').get()
      converted_to_dict = dict(users.val())
      user_name = converted_to_dict[UserID]['name']
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
        print(error)

def save_product(product_name, product_content, user_id, product_amount):
  data = {
    'description': f'{product_content}',
    'amount': f'{product_amount}',
    'name': f'{product_name}'
  }
  res = db.child('Users').child(f"{'UIDs'}").child(user_id).child('Products').push(data)
