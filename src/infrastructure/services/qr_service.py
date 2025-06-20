# src/infrastructure/services/qr_service.py
import qrcode
import base64
from io import BytesIO


class QRService:
    def generar_qr_base64(self, data: str) -> str:
        """
        Toma un string de datos, genera un código QR y lo devuelve
        como una imagen PNG codificada en base64.
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Guardar la imagen en un buffer en memoria en lugar de un archivo
        buffered = BytesIO()
        img.save(buffered, format="PNG")

        # Codificar los bytes de la imagen en base64
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return img_str