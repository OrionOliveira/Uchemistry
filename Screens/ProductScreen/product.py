from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from Firebase import database as db
from QRCode import qrcode_generator as qrg

class ProductScreen(MDScreen):
    prd_name = ObjectProperty(None)
    prd_cont = ObjectProperty(None)
    prd_amt = ObjectProperty(None)

    def save_product(self):
        user_id = self.parent.ids.usr.user_id.text

        def show_errors(local, error):
            if local == 'prd_name':
                self.prd_name.helper_text = error
                self.prd_name.error = True
            elif local == 'prd_cont':
                self.prd_cont.helper_text = error
                self.prd_cont.error = True
            elif local == 'prd_amt':
                self.prd_amt.helper_text = error
                self.prd_amt.error = True
    
        e = db.save_product(self.prd_name.text, self.prd_cont.text, user_id, self.prd_amt.text)

        if e == 'prd_name_emp':
            show_errors('prd_name', 'Product Name')
        elif e == 'prd_cont_emp':
            show_errors('prd_cont', 'Product Contents')
        elif e == 'prd_amt_emp':
            show_errors('prd_amt', 'Product Amount')
        else:
            qrg.gerar_qrcode(self.prd_name.text, self.prd_cont.text, self.prd_amt.text)