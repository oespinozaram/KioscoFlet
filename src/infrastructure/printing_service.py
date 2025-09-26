import os
import platform
from src.application.repositories import Ticket
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
import barcode
from barcode.writer import ImageWriter


class PrintingService:
    def generar_ticket_pdf(self, ticket: Ticket) -> str:
        file_path = f"ticket_{ticket.id_pedido}.pdf"

        ancho_mm = 58
        alto_mm = 120

        c = canvas.Canvas(file_path, pagesize=(ancho_mm * mm, alto_mm * mm))
        width, height = (ancho_mm * mm, alto_mm * mm)

        CODE128 = barcode.get_barcode_class('code128')
        writer = ImageWriter(format='PNG')
        codigo_barras = CODE128(str(ticket.id_pedido), writer=writer)
        barcode_path = f"barcode_{ticket.id_pedido}.png"
        codigo_barras.write(barcode_path)

        c.drawCentredString(width / 2, height - (20 * mm), "¡Pedido Confirmado!")
        c.drawString(10 * mm, height - (30 * mm), f"Folio: {ticket.id_pedido}")
        c.drawString(10 * mm, height - (35 * mm), f"Cliente: {ticket.nombre_cliente}")

        barcode_width = 45 * mm
        barcode_height = 15 * mm
        c.drawImage(
            barcode_path,
            (width - barcode_width) / 2,
            height - (60 * mm),
            width=barcode_width,
            height=barcode_height
        )

        c.save()
        os.remove(barcode_path)

        print(f"INFO: Ticket PDF generado en: {file_path}")
        return os.path.abspath(file_path)

    def enviar_a_impresora(self, file_path: str):

        if not os.path.exists(file_path):
            print(f"ERROR: El archivo a imprimir no existe: {file_path}")
            return

        if platform.system() == "Windows":
            try:
                import win32api
                import win32print
                printer_name = win32print.GetDefaultPrinter()
                print(f"INFO: Enviando a la impresora por defecto: '{printer_name}'")

                win32api.ShellExecute(
                        0,
                        "print",
                        f'"{file_path}"',  # Es importante poner la ruta entre comillas
                        f'/d:"{printer_name}"',
                        ".",
                        0
                    )
            except ImportError:
                print("ERROR: La librería 'pywin32' no está instalada. Ejecuta: pip install pywin32")
            except Exception as e:
                print(f"ERROR: No se pudo imprimir con win32api. {e}")
        else:
            print("ERROR: La impresión directa de PDF solo está configurada para Windows.")
