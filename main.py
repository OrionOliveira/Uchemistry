from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
import QRCode.qrcode_generator as qrg
import Firebase.database as db
from kivy.core.window import Window

Window.size = (300, 600)

class Manager(MDScreenManager):
    pass

class Menu(MDScreen):

    def go_sign(self):
        user_name = self.parent.ids.usr.user_name.text
        if user_name == 'User':
            self.parent.current = 'login_screen'
        else:
            self.parent.current = 'user_screen'

    def product_screen(self):
        user_name = self.parent.ids.usr.user_name.text
        if user_name == 'User':
            self.parent.current = 'login_screen'
        else:
            self.parent.current = 'product_screen'

class SignIn(MDScreen):
    user_name = ObjectProperty(None)
    user_email = ObjectProperty(None)
    user_password = ObjectProperty(None)
    repeated_password = ObjectProperty(None)

    def sign_in(self):
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
        print(f'X = {x}')

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
            self.parent.current = 'product_screen'
            self.parent.ids.usr.user_name.text = str(self.user_name.text)
            self.parent.ids.usr.user_title.title = f"Uchemistry - {str(self.user_name.text)}"
            self.parent.ids.usr.user_id.text = x

class Login(MDScreen):
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

class Scanner(MDScreen):
    def read_qr(self, data):
        url = data.decode()
        converted_in_dict = eval(url)

        self.ids.qr_name.text = f"Name: {converted_in_dict['name']}"
        self.ids.qr_contents.text = f"Contents: {converted_in_dict['contents']}"
        self.ids.qr_amount.text = f"Amount: {converted_in_dict['amount']}"

    def clear(self):
        self.ids.qr_name.text = ''
        self.ids.qr_contents.text = ''
        self.ids.qr_amount.text = ''

class Products(MDScreen):
    prd_name = ObjectProperty(None)
    prd_cont = ObjectProperty(None)
    prd_amt = ObjectProperty(None)

    def save_product(self):
        user_id = self.parent.ids.usr.user_id.text

        def show_errors(local, error):
            if local == 'prd_name':
                self.prd_name.helper_text = error
                self.prd_name.error = True
            elif local == 'prd_cont':
                self.prd_cont.helper_text = error
                self.prd_cont.error = True
            elif local == 'prd_amt':
                self.prd_amt.helper_text = error
                self.prd_amt.error = True
    
        e = db.save_product(self.prd_name.text, self.prd_cont.text, user_id, self.prd_amt.text)

        if e == 'prd_name_emp':
            show_errors('prd_name', 'Product Name')
        elif e == 'prd_cont_emp':
            show_errors('prd_cont', 'Product Contents')
        elif e == 'prd_amt_emp':
            show_errors('prd_amt', 'Product Amount')
        else:
            qrg.gerar_qrcode(self.prd_name.text, self.prd_cont.text, self.prd_amt.text)


class User(MDScreen):
    user_title = ObjectProperty(None)
    user_name = ObjectProperty(None)
    user_id = ObjectProperty(None)

class UChemistry(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Purple'
        return Manager()

    def go_home(self):
        self.root.current = 'menu_screen'

if __name__=='__main__':
    UChemistry().run()
