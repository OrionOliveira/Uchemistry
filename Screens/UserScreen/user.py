from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
import json
import Screens.LoginScreen as lg_s

class UserScreen(MDScreen):
    userName = ObjectProperty(None)
    
    def logout(self):
        with open('Firebase/temp_id.json', 'w') as data:
            json.dump([''], data)
            self.parent.ids.sgs.user_email.text = ''
            self.parent.ids.lgs.user_email.text = ''
    #def get_info(self):