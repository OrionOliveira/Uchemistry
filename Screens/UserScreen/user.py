from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from Firebase import database as db
import json

class UserScreen(MDScreen):
    userName = ObjectProperty(None)
    userEmail = ObjectProperty(None)
    user_id = ObjectProperty(None)
    id = []

    def on_pre_enter(self):
        # Defines the user id
        try:
            with open('Firebase/temp_id.json', 'r') as data:
                global id
                id = json.load(data)
                self.user_id.text = id[0]

            # Defines the user name
            x = db.account_info()
            self.userName.text = x['name']

            # Defines the user email
            self.userEmail.text = x['email']
        except:
            self.userName.text = 'User'

        if self.userName.text == 'User':
            self.parent.current = 'login_screen'
        
    
    def logout(self):
        with open('Firebase/temp_id.json', 'w') as data:
            json.dump([], data)
            self.parent.current = 'menu_screen'