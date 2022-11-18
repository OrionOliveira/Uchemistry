from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty

class UserScreen(MDScreen):
    user_title = ObjectProperty(None)
    user_id = ObjectProperty(None)

    def save_user_info(self, name, uid): #Dar um jeito de essa função modificar permanentemente o título
        self.ids.user_title.title = name
        self.ids.user_id.text = uid

    def get_info(self):
        return (self.ids.user_title.title, self.ids.user_id.text)