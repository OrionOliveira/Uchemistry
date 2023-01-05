import os
from kivymd.app import MDApp
from kaki.app import App
from kivy.factory import Factory
from kivy.core.window import Window
from Firebase import database as db
import json

Window.size = (300, 600)

# https://materialdesignicons.com/ - Lista com todos os ícones disponíveis

class UChemistry(MDApp, App):
    sm = None
    usr = None
    sgs = None
    lgs = None

    user_name = 'User'
    userid = []

    DEBUG = 1

    KV_FILES = {
        os.path.join(os.getcwd(), "Screens/screenmanager.kv"),
        os.path.join(os.getcwd(), "Screens/MenuScreen/menu.kv"),
        os.path.join(os.getcwd(), "Screens/ProductScreen/"),
        os.path.join(os.getcwd(), "Screens/SignInScreen/signin.kv"),
        os.path.join(os.getcwd(), "Screens/LoginScreen/login.kv"),
        os.path.join(os.getcwd(), "Screens/ScannerScreen/scanner.kv"),
        os.path.join(os.getcwd(), "Screens/StockScreen/stock.kv"),
        os.path.join(os.getcwd(), "Screens/UserScreen/user.kv"),
    }

    CLASSES = {
        "MainScreenManager": "Screens.screenmanager",
        "MenuScreen": "Screens.MenuScreen.menu",
        "SignInScreen": "Screens.SignInScreen.signin",
        "LoginScreen": "Screens.LoginScreen.login",
        "ScannerScreen": "Screens.ScannerScreen.scanner",
        "StockScreen": "Screens.StockScreen.stock",
        "UserScreen": "Screens.UserScreen.user",
    }

    AUTORELOADER_PATHS = [
        (".", {"recursive": False}),
    ]

    # Function to build the app
    def build_app(self):
        self.theme_cls.primary_palette = 'Purple'
        self.sm = Factory.MainScreenManager()
        self.usr = Factory.UserScreen()
        self.sgs = Factory.SignInScreen()
        return self.sm

    def on_start(self):
        # return all save products
        x = db.stocked_products()
        print(f'stocked products: {x}')
        # create a widget for each product

# Function to change screen
    def change_screen(self, btn):
        self.btn = btn
        try:
            user_name = db.account_info()
        except:
            user_name = 'User'

        # General function to go to screen
        def go_screen(scr):
            if btn == 'stck' or btn == 'usr':
                if user_name == 'User':
                    self.sm.current = 'login_screen'
                else:
                    self.sm.current = scr
            else:
                print(scr)
                self.sm.current = scr

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
