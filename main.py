from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from Firebase import database as db
from QRCode import qrcode_generator as qrg
import json

Window.size = (300, 600)

# https://materialdesignicons.com/ - Lista com todos os ícones disponíveis

class Manager(MDScreenManager):
    pass

class MenuScreen(MDScreen):
    pass

class ScannerScreen(MDScreen):
    def read_qr(self, data):
        url = data.decode()
        converted_in_dict = eval(url)
        print(converted_in_dict)

        self.ids.qr_name.text = f"Name: {converted_in_dict['name']}"
        self.ids.qr_cas_num.text = f"CAS Number: {converted_in_dict['cas_num']}"
        self.ids.qr_quantity.text = f"Quantity: {converted_in_dict['quantity']}"
        self.ids.qr_date.text = f"Data: {converted_in_dict['date']}"

    def clear(self):
        self.ids.qr_name.text = ''
        self.ids.qr_cas_num.text = ''
        self.ids.qr_quantity.text = ''
        self.ids.qr_date.text = ''

class SignInScreen(MDScreen):
    user_name = ObjectProperty(None)
    user_email = ObjectProperty(None)
    user_password = ObjectProperty(None)
    repeated_password = ObjectProperty(None)

    def on_pre_enter(self):
        self.user_name.text = ''
        self.user_email.text = ''
        self.user_password.text = ''
        self.repeated_password.text = ''

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
        user_info.append(x)
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
            self.parent.current = 'menu_screen'
            with open('Firebase/temp_id.json', 'w') as data:
                json.dump(user_info, data)

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

class UserScreen(MDScreen):
    userName = ObjectProperty(None)
    userEmail = ObjectProperty(None)
    user_id = ObjectProperty(None)

    def on_pre_enter(self):
        x = db.account_info()

        # Defines the user email
        self.userEmail.text = x[0]
        
        # Defines the user name
        self.userName.text = x[1]

        # Defines the user id
        self.user_id.text = x[2]

        if self.userName.text == 'User':
            self.parent.current = 'login_screen'
        
    
    def logout(self):
        with open('Firebase/temp_id.json', 'w') as data:
            json.dump([], data)
            self.parent.current = 'menu_screen'

class ProductScreen(MDScreen):
    dialog = None
    prd_name = ObjectProperty(None)
    cas_num = ObjectProperty(None)
    prd_qtde = ObjectProperty(None)
    prd_date = ObjectProperty(None)
    sv_lbl = ObjectProperty(None)

    def on_pre_enter(self):
        self.prd_name.text = ''
        self.cas_num.text = ''
        self.prd_qtde.text = ''
        self.prd_date.text = ''
        self.sv_lbl.text = ''

    def save_product(self):
        user_id = db.account_info()[2]

        def show_popup():
            if not self.dialog:
                self.dialog = MDDialog(
                    text="Generate QR Code?",
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            theme_text_color="Custom",
                            on_release = self.close_popup
                        ),
                        MDFlatButton(
                            text="GENERATE",
                            theme_text_color="Custom",
                            on_release = self.generate_qr_code,
                        ),
                    ],
                )
            self.dialog.open()

        def show_errors(local, error):
            if local == 'prd_name':
                self.prd_name.helper_text = error
                self.prd_name.error = True
            elif local == 'cas_num':
                self.cas_num.helper_text = error
                self.cas_num.error = True
            elif local == 'prd_qtde':
                self.prd_qtde.helper_text = error
                self.prd_qtde.error = True
            elif local == 'prd_date':
                self.prd_date.helper_text = error
                self.prd_date.error = True
    
        e = db.save_product(self.prd_name.text, self.cas_num.text, user_id, self.prd_qtde.text, self.prd_date.text)


        if e == 'prd_name_emp':
            show_errors('prd_name', 'Product Name')
        elif e == 'cas_num_emp':
            show_errors('cas_num', 'Product CAS Number')
        elif e == 'prd_qtde_emp':
            show_errors('prd_qtde', 'Product Quantity')
        elif e == 'prd_date_emp':
            show_errors('prd_date', 'Product Date')
        else:
            self.sv_lbl.text = 'Product saved successfully!'
            self.add_product(self.prd_name.text)
            show_popup()

    def add_product(self, name):
        self.parent.ids.stck.prd_box.add_widget(Product(name))

    def close_popup(self, obj):
        self.dialog.dismiss()

    def generate_qr_code(self, obj):
        qrg.gerar_qrcode(self.prd_name.text, self.cas_num.text, self.prd_qtde.text, self.prd_date.text)
        self.dialog.dismiss()

class Product(MDBoxLayout):
    def __init__(self, text = '', **kwargs):
        super().__init__(**kwargs)
        self.ids.prd_label.text = text
            
class StockScreen(MDScreen):
    prd_box = ObjectProperty(None)
    def on_pre_enter(self):
        pass
        #x = db.stocked_products()
        #print(f'stocked products: {x}')
class UChemistry(MDApp):
    user_name = 'User'

    # Function to build the app
    def build(self):
        self.theme_cls.primary_palette = 'Purple'
        return Manager()

    def on_start(self):
        pass
        # return all save products
        #x = db.stocked_products()
        #print(f'stocked products: {x}')
        # create a widget for each product

# Function to change screen
    def change_screen(self, btn):
        self.btn = btn
        try:
            user_name = db.account_info()[1]
        except:
            user_name = 'User'

        # General function to go to screen
        def go_screen(scr):
            if btn == 'stck' or btn == 'usr':
                if user_name == 'User':
                    self.root.current = 'login_screen'
                else:
                    self.root.current = scr
            else:
                self.root.current = scr

        if btn == 'stck':
            if user_name == 'User':
                go_screen('login_screen')
            else:
                go_screen('stock_screen')
        elif btn == 'scan':
            go_screen('scanner_screen')
        elif btn == 'menu':
            go_screen('menu_screen')
        elif btn == 'usr':
            if user_name == 'User':
                go_screen('login_screen')
            else:
                go_screen('user_screen')
        elif btn == 'sgn':
            go_screen('signin_screen')

if __name__=='__main__':
    UChemistry().run()
