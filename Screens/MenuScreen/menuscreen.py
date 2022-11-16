from kivymd.uix.screen import MDScreen

class MenuScreen(MDScreen):

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