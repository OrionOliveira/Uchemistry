import os
from kivymd.app import MDApp
from kaki.app import App
from kivy.factory import Factory
from kivy.core.window import Window

Window.size = (300, 600)

# https://materialdesignicons.com/ - Lista com todos os ícones disponíveis

class UChemistry(MDApp, App):

    DEBUG = 1

    KV_FILES = {
        os.path.join(os.getcwd(), "Screens/screenmanager.kv"),
        os.path.join(os.getcwd(), "Screens/MenuScreen/menuscreen.kv"),
        os.path.join(os.getcwd(), "Screens/SignInScreen/signinscreen.kv"),
        os.path.join(os.getcwd(), "Screens/LoginScreen/loginscreen.kv"),
        os.path.join(os.getcwd(), "Screens/ScannerScreen/scannerscreen.kv"),
        os.path.join(os.getcwd(), "Screens/ProductScreen/productscreen.kv"),
        os.path.join(os.getcwd(), "Screens/UserScreen/userscreen.kv"),
    }

    CLASSES = {
        "MainScreenManager": "Screens.screenmanager",
        "MenuScreen": "Screens.MenuScreen.menuscreen",
        "SignInScreen": "Screens.SignInScreen.signinscreen",
        "LoginScreen": "Screens.LoginScreen.loginscreen",
        "ScannerScreen": "Screens.ScannerScreen.scannerscreen",
        "ProductScreen": "Screens.ProductScreen.productscreen",
        "UserScreen": "Screens.UserScreen.userscreen",
    }

    AUTORELOADER_PATHS = [
        (".", {"recursive": True}),
    ]

    def build_app(self):
        self.theme_cls.primary_palette = 'Purple'
        return Factory.MainScreenManager()

    def go_home(self):
        self.root.current = 'menu_screen'

if __name__=='__main__':
    UChemistry().run()
