from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty

class UserScreen(MDScreen):
    user_title = ObjectProperty(None)
    user_name = ObjectProperty(None)
    user_id = ObjectProperty(None)