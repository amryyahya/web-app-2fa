import qrcode
import io
import base64
qr = qrcode.QRCode(
version=1,
error_correction=qrcode.constants.ERROR_CORRECT_L,
box_size=10,
border=4,
)
data = "Hello, QR Code!"
qr.add_data(data)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img_buffer = io.BytesIO()
img.save(img_buffer)
img_buffer.seek(0)
img_str = base64.b64encode(img_buffer.read()).decode('utf-8')

print(type(img))