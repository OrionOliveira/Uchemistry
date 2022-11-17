from kivymd.uix.screen import MDScreen

class ScannerScreen(MDScreen):
    def read_qr(self, data):
        url = data.decode()
        converted_in_dict = eval(url)

        self.ids.qr_name.text = f"Name: {converted_in_dict['name']}"
        self.ids.qr_contents.text = f"Contents: {converted_in_dict['contents']}"
        self.ids.qr_amount.text = f"Amount: {converted_in_dict['amount']}"

    def clear(self):
        self.ids.qr_name.text = ''
        self.ids.qr_contents.text = ''
        self.ids.qr_amount.text = ''