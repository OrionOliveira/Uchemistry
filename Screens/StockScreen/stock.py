from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivy.properties import ObjectProperty
from Firebase import database as db
from QRCode import qrcode_generator as qrg

class Product(MDBoxLayout):
    prd_name = ObjectProperty(None)
    cas_num = ObjectProperty(None)
    prd_qtde = ObjectProperty(None)

    def save_product(self):
        user_id = db.get_id()

        def show_errors(local, error):
            if local == 'prd_name':
                self.prd_name.helper_text = error
                self.prd_name.error = True
            elif local == 'cas_num':
                self.cas_num.helper_text = error
                self.cas_num.error = True
            elif local == 'prd_qtde':
                self.prd_qtde.helper_text = error
                self.prd_qtde.error = True

        e = db.save_product(self.prd_name.text, self.cas_num.text, user_id, self.prd_qtde.text)

        if e == 'prd_name_emp':
            show_errors('prd_name', 'Product Name')
        elif e == 'cas_num_emp':
            show_errors('cas_num', 'Product Contents')
        elif e == 'prd_amt_emp':
            show_errors('prd_qtde', 'Product Amount')
        else:
            pass
        
    def teste(self, obj):
        print(self.prd_name.text)

class StockScreen(MDScreen):
    dialog = None
    p = Product()

    def add_product(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Add Product:",
                type="custom",
                content_cls=Product(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        on_release = self.close_popup
                    ),
                    MDFlatButton(
                        text="SAVE",
                        theme_text_color="Custom",
                        on_release = self.save
                    ),
                ],
            )
        self.dialog.open()

    def close_popup(self, obj):
        self.dialog.dismiss()

    def save(self, obj):
        user_id = db.get_id()
        prd_name = self.p.prd_name
        cas_num = self.p.cas_num
        prd_qtde = self.p.prd_qtde

        def show_errors(local, error):
            if local == 'prd_name':
                prd_name.helper_text = error
                prd_name.error = True
            elif local == 'cas_num':
                cas_num.helper_text = error
                cas_num.error = True
            elif local == 'prd_qtde':
                prd_qtde.helper_text = error
                prd_qtde.error = True

        e = db.save_product(prd_name.text, cas_num.text, user_id, prd_qtde.text)

        if e == 'prd_name_emp':
            show_errors('prd_name', 'Product Name')
        elif e == 'cas_num_emp':
            show_errors('cas_num', 'Product Contents')
        elif e == 'prd_amt_emp':
            show_errors('prd_qtde', 'Product Amount')
        else:
            pass
