import qrcode

def gerar_qrcode(name, cas_num, quantity, date):
    imagem_qrcode = qrcode.make({
    'name': str(name), 
    'cas_num': str(cas_num),
    'quantity': str(quantity),
    'date': str(date)
    })
    imagem_qrcode.save(f"Images/QRCodes/{name}_qrcode.png")
