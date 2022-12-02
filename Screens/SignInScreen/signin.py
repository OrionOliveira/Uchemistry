from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from Firebase import database as db
import json

class SignInScreen(MDScreen):
    user_name = ObjectProperty(None)
    user_email = ObjectProperty(None)
    user_password = ObjectProperty(None)
    repeated_password = ObjectProperty(None)

    def sign_in(self):
        user_info = []
        def show_error(local, error):
            if local == 'email':
                self.user_email.helper_text = error
                self.user_email.error = True
            elif local == 'pssw':
                self.user_password.helper_text = error
                self.user_password.error = True
            elif local == 'rpt_pssw':
                self.repeated_password.helper_text = error
                self.repeated_password.error = True
            else:
                self.user_name.helper_text = error
                self.user_name.error = True

        # Cadastra o usuário no Firebase
        x = db.sign_in_db(self.user_name.text, self.user_email.text, self.user_password.text, self.repeated_password.text)
        print(x)
        user_info.append(x[1])
        # Tratamento de erros
        if x == '':
            pass
        elif x == 'inv_email':
            show_error('email', 'Invalid Email')
        elif x == 'email_exst':
            show_error('email', 'Email Exists')
        elif x == 'pssw_nc':
            show_error('rpt_pssw', 'The password does not match')
        elif x == 'wk_pssw':
            show_error('pssw', 'Password should be at least 6 characters')
        elif x == 'pssw_emp':
            show_error('pssw', 'Password')
        elif x == 'rpt_pssw_emp':
            show_error('rpt_pssw', 'Repeat password')
        elif x == 'nm_emp':
            show_error('name', 'Name')
        elif x == 'email_emp':
            show_error('email','Email')
        elif x == 'inv_prv':
            show_error('email','Invalid email provider (@xxx)')
        else:
            self.parent.current = 'stock_screen'
            with open('Firebase/temp_id.json', 'w') as data:
                json.dump(user_info, data)
            