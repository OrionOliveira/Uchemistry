from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from Firebase import database as db

class LoginScreen(MDScreen):
    user_name = ObjectProperty(None)
    user_email = ObjectProperty(None)
    user_password = ObjectProperty(None)

    def login(self):
        def show_error(local, error):
            if local == 'email':
                self.user_email.helper_text = error
                self.user_email.error = True
            else:
                self.user_password.helper_text = error
                self.user_password.error = True

        x = db.login_db(self.user_email.text, self.user_password.text)
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
            self.parent.current = 'product_screen'
            self.parent.ids.usr.user_name.text = x[0]
            self.parent.ids.usr.user_title.title = f"Uchemistry - {x[0]}"
            self.parent.ids.usr.user_id.text = x[1]