from django.shortcuts import render
from django.http import HttpResponse
import qrcode
import base64
from io import BytesIO  # con esto maneja las imagenes en memoria y asi crea el qr

def index(request):
    # para detectar el tipo de dispo con user agent
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    is_mobile = 'mobile' in user_agent

    apk_link = '/static/duocUc/apk/app-debug.apk'

    # genera el codigo QR cuando no es dispo movil
    qr_image_data = None
    if not is_mobile:
        apk_url = "http://192.168.23.187:8000/" + apk_link #ruta de ip local para acceder desde movil y levantar el sitio web para escanear el qr
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=4,
        )
        qr.add_data(apk_url)
        qr.make(fit=True)

        # se crea la imagen del qr en memoria usando la libreria d python
        img = qr.make_image(fill_color="black", back_color="white")
        qr_image = BytesIO() #guarda la img
        img.save(qr_image, format="PNG")
        qr_image_data = base64.b64encode(qr_image.getvalue()).decode('utf-8')  #conversor a base64

    return render(request, 'duocUc/index.html', {
        'apk_action': 'install' if is_mobile else 'download',
        'apk_link': apk_link,
        'qr_image_data': qr_image_data,  # qr en base64
    })
