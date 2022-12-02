from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
import json

class UserScreen(MDScreen):
    userName = ObjectProperty(None)
    
    def logout(self):
        with open('Firebase/temp_id.json', 'w') as data:
            json.dump([''], data)
    #def get_info(self):
    #    db.account_info()
    #    return (self.userName.text, self.ids.uid.text)