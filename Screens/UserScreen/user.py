from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty

class UserScreen(MDScreen):
    userName = ObjectProperty(None)
    
    def get_info(self):
        return (self.userName.text, self.ids.uid.text)