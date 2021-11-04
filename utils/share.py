import qrcode


#: 分享二维码
def shareQR():
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=10, )
    qr.add_data('http://www.cnblogs.com/sfnz/')
    qr.make(fit=True)
    img = qr.make_image()
    img.show()


shareQR()