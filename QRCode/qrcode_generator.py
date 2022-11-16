import qrcode

def gerar_qrcode(name, contents, amount):
    imagem_qrcode = qrcode.make({'name': str(name), 
    'contents': str(contents),
    'amount': str(amount)})
    imagem_qrcode.save(f"Images/QRCodes/{name}_qrcode.png")
