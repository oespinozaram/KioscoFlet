import os
import platform
from src.application.repositories import Ticket
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
import barcode
from barcode.writer import ImageWriter
from escpos.printer import Network


class PrintingService:
    def __init__(self):
        # --- CAMBIO: Ya no usamos IDs. Usamos el nombre del PC y el nombre del recurso compartido ---
        nombre_pc = "AVALOST"  # <-- REEMPLAZA CON EL NOMBRE DE TU PC
        nombre_impresora_compartida = "POS-80" # <-- REEMPLAZA CON EL NOMBRE QUE LE DISTE

        # Formato para impresoras compartidas en Windows
        self.PRINTER_PATH = f"\\\\{nombre_pc}\\{nombre_impresora_compartida}"

    def print_ticket(self, ticket: Ticket):
        try:
            p = Network(self.PRINTER_PATH)

            p.hw("init")  # Resetea la impresora
            p.charcode("CP850")

            # --- Título ---
            p.set(align='center', width=2, height=2)
            p.textln("¡Pedido Confirmado!")

            p.set(align='center', text_type='A')  # Reset a tamaño normal
            p.textln("Pastelería Pepe")
            p.textln("================================")

            # --- Detalles del Pedido ---
            p.set(align='left')
            p.textln(f"Folio: {ticket.id_pedido}")
            p.textln(f"Cliente: {ticket.nombre_cliente}")
            p.textln(f"Fecha Entrega: {ticket.fecha_entrega}")
            p.ln(1)  # Añade un salto de línea

            p.textln("--- DETALLES ---")
            p.textln(f"Pan: {ticket.tipo_pan}, Forma: {ticket.tipo_forma}")
            p.textln(f"Relleno: {ticket.tipo_relleno}")
            # ... puedes añadir más detalles del pedido aquí ...
            p.textln("================================")

            # --- Código de Barras ---
            p.set(align='center')
            p.barcode(str(ticket.id_pedido).zfill(8), 'CODE128', height=60, width=3)
            p.ln(1)

            # --- Mensaje Final ---
            p.textln("Gracias por su compra!")
            p.ln(3)  # Espacio extra antes de cortar

            p.cut()

        except Exception as e:
            print(f"ERROR al imprimir ticket: {e}")

    def generar_ticket_pdf(self, ticket: Ticket) -> str:
        file_path = f"ticket_{ticket.id_pedido}.pdf"

        ancho_mm = 80
        # Reducimos la altura para un ticket más compacto
        alto_mm = 160

        c = canvas.Canvas(file_path, pagesize=(ancho_mm * mm, alto_mm * mm))
        width, height = (ancho_mm * mm, alto_mm * mm)

        # --- 1. Generar la imagen del código de barras ---
        CODE128 = barcode.get_barcode_class('code128')
        writer = ImageWriter(format='PNG')
        # Usamos zfill para asegurar una longitud mínima, es una buena práctica
        folio_str = str(ticket.id_pedido).zfill(6)
        codigo_barras = CODE128(folio_str, writer=writer)
        barcode_path = f"barcode_{ticket.id_pedido}.png"
        codigo_barras.write(barcode_path)

        # --- 2. Dibujar el Ticket en el PDF ---
        y = height - (10 * mm)  # Posición vertical inicial

        # Encabezado
        c.drawCentredString(width / 2, y, "Pastelería Pepe")
        y -= (5 * mm)
        c.drawCentredString(width / 2, y, "¡Pedido Confirmado!")
        y -= (15 * mm)  # Espacio para el código de barras

        # Código de Barras (ahora va arriba)
        barcode_width = 45 * mm
        barcode_height = 15 * mm
        c.drawImage(
            barcode_path,
            (width - barcode_width) / 2, y,
            width=barcode_width, height=barcode_height
        )
        y -= (15 * mm)
        c.drawCentredString(width / 2, y, f"Folio: {folio_str}")
        y -= (10 * mm)

        # Detalles del Pedido
        margen_izquierdo = 5 * mm
        c.drawString(margen_izquierdo, y, f"Cliente: {ticket.nombre_cliente}")
        y -= (5 * mm)
        c.drawString(margen_izquierdo, y, f"Fecha de Entrega: {ticket.fecha_entrega}")
        y -= (5 * mm)
        c.drawString(margen_izquierdo, y, f"Hora de Entrega: {ticket.hora_entrega}")
        y -= (8 * mm)

        c.drawString(margen_izquierdo, y, "--- Detalles del Pastel ---")
        y -= (5 * mm)
        c.drawString(margen_izquierdo, y, f"Pastel: {ticket.nombre_categoria}")
        y -= (5 * mm)
        c.drawString(margen_izquierdo, y, f"Pan: {ticket.tipo_pan}")
        y -= (5 * mm)
        c.drawString(margen_izquierdo, y, f"Forma: {ticket.tipo_forma}")
        y -= (5 * mm)
        c.drawString(margen_izquierdo, y, f"Relleno: {ticket.tipo_relleno}")
        y -= (5 * mm)
        c.drawString(margen_izquierdo, y, f"Cobertura: {ticket.tipo_cobertura}")
        y -= (5 * mm)
        c.drawString(margen_izquierdo, y, f"Tamaño (personas): {ticket.tamano_pastel}")
        y -= (8 * mm)

        # Precios
        c.drawString(margen_izquierdo, y, f"Costo Pastel: ${(ticket.precio_pastel or 0.0):.2f}")
        y -= (5 * mm)
        c.drawString(margen_izquierdo, y, f"Costo Extra: ${(ticket.extra_costo or 0.0):.2f}")
        y -= (5 * mm)
        c.drawString(margen_izquierdo, y, f"Total: ${(ticket.total or 0.0):.2f}")
        y -= (8 * mm)

        c.drawCentredString(width / 2, y, "¡Gracias por su compra!")

        c.save()
        os.remove(barcode_path)

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
