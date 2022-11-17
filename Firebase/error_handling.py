# Tratamentos de erros
p = ['gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com']

def signin_errors(_name, _email, _password, _rpt_pssw):
    # Campo nome vazio
    if _name == '':
      return True, 'nm_emp'
    # Campo email vazio
    elif _email == '':
      return True, 'email_emp'
    # Campo senha vazio
    elif _password == '':
      return True, 'pssw_emp'
    # Campo repita a senha vazio
    elif _rpt_pssw == '':
      return True, 'rpt_pssw_emp'
    # Senhas não conferem
    elif _password != _rpt_pssw:
      return True, 'pssw_nc'
    # Senha tem menos de 6 caracteres
    elif len(_password) < 6:
      return True, 'wk_pssw'
  # Provedor de email inválido
    elif p[0] not in _email or p[1] not in _email or p[2] not in _email or p[3] not in _email:
      if p[0] in _email:
        print(f'Email possue o provedor {p[0]}')
        return False, 'Valid Email'
      elif p[1] in _email:
        print(f'Email possue o provedor {p[1]}')
        return False, 'Valid Email'
      elif p[2] in _email:
        print(f'Email possue o provedor {p[2]}')
        return False, 'Valid Email'
      elif p[3] in _email:
        print(f'Email possue o provedor {p[3]}')
        return False, 'Valid Email'
      else:
        print(f'Email não pertence a provedores válidos')
        return True, 'inv_prv'

def qr_errors(prd_name, prd_contents, prd_amount):
  if prd_name == '':
    return True, 'prd_name_emp'
  elif prd_contents == '':
    return True, 'prd_cont_emp'
  elif prd_amount == '':
    return True, 'prd_amt_emp'
  else:
    return False, 'Valid Product'