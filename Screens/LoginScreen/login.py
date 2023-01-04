from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from Firebase import database as db
import json

class LoginScreen(MDScreen):
    user_name = ObjectProperty(None)
    user_email = ObjectProperty(None)
    user_password = ObjectProperty(None)

    def on_pre_enter(self):
        self.user_email.text = ''
        self.user_password.text = ''

    def login(self):
        user_info = []

        def show_error(local, error):
            if local == 'email':
                self.user_email.helper_text = error
                self.user_email.error = True
            else:
                self.user_password.helper_text = error
                self.user_password.error = True

        x = db.login_db(self.user_email.text, self.user_password.text)
        user_info.append(x[1])
        if x == 'email_emp':
            show_error('email', 'Email')
        elif x == 'email_nf':
            show_error('email','Email Not found')
        elif x == 'inv_email':
            show_error('email','Invalid Email')
        elif x == 'mss_pssw':
            show_error('password','Password')
        elif x == 'inv_pssw':
            show_error('password','Incorrect Password')
        elif x == None:
            print('Senha vazia')
        else:
            self.parent.current = 'menu_screen'
            with open('Firebase/temp_id.json', 'w') as data:
                json.dump(user_info, data)