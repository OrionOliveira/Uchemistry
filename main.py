import os
from kivymd.app import MDApp
from kaki.app import App
from kivy.factory import Factory
from kivy.core.window import Window
from Firebase import database as db

Window.size = (300, 600)

# https://materialdesignicons.com/ - Lista com todos os ícones disponíveis

class UChemistry(MDApp, App):
    sm = None
    usr = None

    user_name = 'User'
    user_id = ''

    DEBUG = 1

    KV_FILES = {
        os.path.join(os.getcwd(), "Screens/screenmanager.kv"),
        os.path.join(os.getcwd(), "Screens/MenuScreen/menu.kv"),
        os.path.join(os.getcwd(), "Screens/SignInScreen/signin.kv"),
        os.path.join(os.getcwd(), "Screens/LoginScreen/login.kv"),
        os.path.join(os.getcwd(), "Screens/ScannerScreen/scanner.kv"),
        os.path.join(os.getcwd(), "Screens/ProductScreen/product.kv"),
        os.path.join(os.getcwd(), "Screens/ProductScreen/StockScreen/stock.kv"),
        os.path.join(os.getcwd(), "Screens/UserScreen/user.kv"),
    }

    CLASSES = {
        "MainScreenManager": "Screens.screenmanager",
        "MenuScreen": "Screens.MenuScreen.menu",
        "SignInScreen": "Screens.SignInScreen.signin",
        "LoginScreen": "Screens.LoginScreen.login",
        "ScannerScreen": "Screens.ScannerScreen.scanner",
        "ProductScreen": "Screens.ProductScreen.product",
        "StockScreen": "Screens.ProductScreen.StockScreen.stock",
        "UserScreen": "Screens.UserScreen.user",
    }

    AUTORELOADER_PATHS = [
        (".", {"recursive": True}),
    ]

    def build_app(self):
        self.theme_cls.primary_palette = 'Purple'
        self.sm = Factory.MainScreenManager()
        self.usr = Factory.UserScreen()
        return self.sm

    def on_start(self):
        x = db.stocked_products()

    def change_screen(self, btn):
        self.btn = btn
        try:
            user_name = db.account_info()
        except:
            user_name = 'User'

        def go_screen(scr):
            if btn == 'prd' or btn == 'usr':
                if user_name == 'User':
                    self.sm.current = 'login_screen'
                else:
                    self.sm.current = scr
            else:
                print(scr)
                self.sm.current = scr

        if btn == 'prd':
            if user_name == 'User':
                go_screen('login_screen')
            else:
                go_screen('product_screen')
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
        elif btn == 'stck':
            go_screen('stock_screen')

if __name__=='__main__':
    UChemistry().run()
