import os
import platform
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from src.application.repositories import Ticket
import barcode
from barcode.writer import ImageWriter


class PrintingService:
    def generar_ticket_pdf(self, ticket: Ticket) -> str:
        file_path = f"ticket_{ticket.id_pedido}.pdf"

        # --- 1. Generar la imagen del código de barras ---
        CODE128 = barcode.get_barcode_class('code128')
        # El writer guarda la imagen como PNG
        writer = ImageWriter(format='PNG')
        codigo_barras = CODE128(str(ticket.id_pedido), writer=writer)

        # Guardamos el código de barras en un archivo de imagen temporal
        barcode_path = f"barcode_{ticket.id_pedido}.png"
        codigo_barras.write(barcode_path)

        # --- 2. Crear el PDF e insertar la imagen ---
        c = canvas.Canvas(file_path, pagesize=(3 * inch, 6 * inch))
        width, height = (3 * inch, 6 * inch)

        c.drawString(72, height - (1 * inch), "¡Pedido Confirmado!")
        c.drawString(30, height - (1.5 * inch), f"Cliente: {ticket.nombre_cliente}")

        # Dibujamos la imagen del código de barras en el PDF
        # Posición: 0.5 pulgadas desde la izquierda, 3 pulgadas desde abajo
        c.drawImage(barcode_path, 0.5 * inch, 3 * inch, width=2 * inch, height=0.8 * inch)

        # Escribimos el folio debajo del código de barras para legibilidad
        c.drawCentredString(1.5 * inch, 2.8 * inch, f"Folio: {ticket.id_pedido}")

        c.save()
        print(f"INFO: Ticket con código de barras generado en: {file_path}")

        # (Opcional) Borramos la imagen temporal del código de barras
        os.remove(barcode_path)

        return os.path.abspath(file_path)

    def enviar_a_impresora(self, file_path: str):
        if not os.path.exists(file_path):
            print(f"ERROR: El archivo a imprimir no existe: {file_path}")
            return

        # Este método es específico para Windows y más robusto
        if platform.system() == "Windows":
            try:
                import win32api
                import win32print

                # Obtenemos el nombre de la impresora por defecto
                printer_name = win32print.GetDefaultPrinter()
                print(f"INFO: Enviando a la impresora por defecto: '{printer_name}'")

                # El comando 'print' de win32api es más directo que os.startfile
                win32api.ShellExecute(
                    0,
                    "print",
                    f'"{file_path}"',  # Es importante poner la ruta entre comillas
                    f'/d:"{printer_name}"',
                    ".",
                    0
                )
                print(f"INFO: Archivo '{file_path}' enviado a la cola de impresión.")

            except ImportError:
                print("ERROR: La librería 'pywin32' no está instalada. Ejecuta: pip install pywin32")
            except Exception as e:
                print(f"ERROR: No se pudo imprimir con win32api. {e}")
        else:
            # Mantenemos la lógica para otros sistemas operativos
            os.system(f"lp {file_path}")