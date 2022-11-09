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

    def sign_in(self):
        x = db.sign_in_db(self.user_name.text, self.user_email.text, self.user_password.text)
        if x == 'erro':
            print("Sign In failed")
        else:
            self.parent.current = 'product_screen'
            self.parent.ids.usr.user_name.text = str(self.user_name.text)
            self.parent.ids.usr.user_title.title = f"Uchemistry - {str(self.user_name.text)}"
            self.parent.ids.usr.user_id.text = x
            print('Sing In sucessfuly!!')

class Login(MDScreen):
    user_name = ObjectProperty(None)
    user_email = ObjectProperty(None)
    user_password = ObjectProperty(None)
    error_label = ObjectProperty(None)

    def login(self):
        x = db.login_db(self.user_email.text, self.user_password.text)
        if x == 'erro_nf':
            self.user_email.text = ''
            self.user_password.text = ''
            self.error_label.text = 'Email not found'
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
    def save_product(self):
        prd_name = self.ids.product_name.text
        prd_cont = self.ids.product_value.text
        prd_amnt = self.ids.product_amount.text
        user_id = self.parent.ids.usr.user_id.text

        qrg.gerar_qrcode(prd_name, prd_cont, prd_amnt)
        db.save_product(prd_name, prd_cont, user_id, prd_amnt)

class User(MDScreen):
    user_title = ObjectProperty(None)
    user_name = ObjectProperty(None)
    user_id = ObjectProperty(None)

class UChemistry(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Purple'
        return Manager()

    def go_home(self, screen):
        self.root.current = 'menu_screen'

if __name__=='__main__':
    UChemistry().run()
