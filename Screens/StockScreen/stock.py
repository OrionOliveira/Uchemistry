from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import BoxLayout

class Content(BoxLayout):
    pass

class StockScreen(MDScreen):
    dialog = None

    def add_product(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Add Product:",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        on_release = self.close_dialog
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, obj):
        # Close the dialog box
        self.dialog.dismiss()