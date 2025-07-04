# src/infrastructure/flet_adapter/views.py
import flet as ft
import datetime
from dateutil.relativedelta import relativedelta
from src.application.use_cases import PedidoUseCases


# --- Vista de Bienvenida ---
def vista_bienvenida(page: ft.Page):
    return ft.View(
        route="/",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Pastelería Pepe's", size=40, weight=ft.FontWeight.BOLD),
                        ft.Text("Toca para iniciar tu pedido", size=20, italic=True),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True,
                on_click=lambda _: page.go("/fecha")
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER
    )


def vista_categorias(page: ft.Page, use_cases: PedidoUseCases):
    # --- Contenedores dinámicos ---
    contenedor_formas = ft.Row(wrap=True, spacing=10, run_spacing=10, alignment=ft.MainAxisAlignment.CENTER)
    contenedor_panes = ft.Row(wrap=True, spacing=10, run_spacing=10, alignment=ft.MainAxisAlignment.CENTER)
    contenedor_rellenos = ft.Row(wrap=True, spacing=10, run_spacing=10, alignment=ft.MainAxisAlignment.CENTER)
    contenedor_coberturas = ft.Row(wrap=True, spacing=10, run_spacing=10,
                                   alignment=ft.MainAxisAlignment.CENTER)  # Nuevo

    # Secciones completas
    seccion_formas = ft.Column([ft.Text("...luego, la forma:"), contenedor_formas],
                               horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, visible=False)
    seccion_panes = ft.Column([ft.Text("...después, el tipo de pan:"), contenedor_panes],
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, visible=False)
    seccion_rellenos = ft.Column([ft.Text("...el relleno:"), contenedor_rellenos],
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, visible=False)
    seccion_coberturas = ft.Column([ft.Text("...y finalmente, la cobertura:"), contenedor_coberturas],
                                   horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10,
                                   visible=False)  # Nuevo

    acciones_finales = ft.Row(alignment=ft.MainAxisAlignment.CENTER, visible=False)


    # --- Lógica de la Interfaz ---
    def check_and_show_final_actions():
        pedido = use_cases.obtener_pedido_actual()
        if pedido.tipo_forma and pedido.tipo_pan and pedido.tipo_relleno and pedido.tipo_cobertura:  # Añadida condición
            acciones_finales.visible = True
            page.update()

    def on_cobertura_selected(e):  # Nuevo manejador
        use_cases.seleccionar_tipo_cobertura(e.control.text)
        for btn in contenedor_coberturas.controls: btn.selected = (btn == e.control)
        check_and_show_final_actions()
        page.update()

    def on_relleno_selected(e):
        use_cases.seleccionar_tipo_relleno(e.control.text)
        for btn in contenedor_rellenos.controls: btn.selected = (btn == e.control)
        check_and_show_final_actions()
        page.update()

    def on_pan_selected(e):
        id_pan_seleccionado = e.control.data
        nombre_pan_seleccionado = e.control.text

        use_cases.seleccionar_tipo_pan(nombre_pan_seleccionado)
        for btn in contenedor_panes.controls: btn.selected = (btn == e.control)

        id_categoria_actual = use_cases.obtener_pedido_actual().id_categoria

        contenedor_rellenos.controls.clear()
        lista_rellenos = use_cases.obtener_rellenos_disponibles(id_categoria_actual, id_pan_seleccionado)
        if not lista_rellenos:
            contenedor_rellenos.controls.append(ft.Text("No hay rellenos para esta combinación."))
        else:
            for nombre_relleno in lista_rellenos:
                contenedor_rellenos.controls.append(ft.FilledButton(text=nombre_relleno, on_click=on_relleno_selected))
        seccion_rellenos.visible = True

        contenedor_coberturas.controls.clear()
        lista_coberturas = use_cases.obtener_coberturas_disponibles(id_categoria_actual, id_pan_seleccionado)
        if not lista_coberturas:
            contenedor_coberturas.controls.append(ft.Text("No hay coberturas para esta combinación."))
        else:
            for nombre_cobertura in lista_coberturas:
                contenedor_coberturas.controls.append(
                    ft.FilledButton(text=nombre_cobertura, on_click=on_cobertura_selected))
        seccion_coberturas.visible = True

        check_and_show_final_actions()
        page.update()

    def on_forma_selected(e):
        use_cases.seleccionar_tipo_forma(e.control.text)
        for btn in contenedor_formas.controls: btn.selected = (btn == e.control)
        check_and_show_final_actions()
        page.update()

    def on_category_click(e):
        id_categoria = e.control.data
        use_cases.seleccionar_categoria(id_categoria)

        for cont in [contenedor_formas, contenedor_panes, contenedor_rellenos, contenedor_coberturas]: cont.controls.clear()
        for sec in [seccion_formas, seccion_panes, seccion_rellenos, seccion_coberturas, acciones_finales]: sec.visible = False

        for forma in use_cases.obtener_formas_por_categoria(id_categoria):
            contenedor_formas.controls.append(ft.FilledButton(text=forma, on_click=on_forma_selected))
        seccion_formas.visible = True

        for pan in use_cases.obtener_panes_por_categoria(id_categoria):
            contenedor_panes.controls.append(ft.FilledButton(text=pan.nombre, data=pan.id, on_click=on_pan_selected))
        seccion_panes.visible = True

        page.update()

    # --- Construcción de la Vista ---
    lista_categorias = use_cases.obtener_categorias()
    botones_categorias = [ft.ElevatedButton(text=c.nombre, data=c.id, on_click=on_category_click) for c in
                          lista_categorias]
    acciones_finales.controls.extend([
        ft.ElevatedButton("Volver", on_click=lambda _: page.go("/tamano")),
        ft.ElevatedButton("Elegir Decorado", on_click=lambda _: page.go("/decorado")),
    ])

    return ft.View(
        route="/categorias",
        controls=[
            ft.Text("Paso 3: Detalles Finales", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Primero, elige una categoría:"),
            ft.Row(controls=botones_categorias, wrap=True, spacing=10, run_spacing=10, alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=10),
            seccion_formas,
            seccion_panes,
            seccion_rellenos,
            seccion_coberturas,
            ft.Divider(height=10),
            acciones_finales,
        ],
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        scroll=ft.ScrollMode.ADAPTIVE
    )


def vista_decorado(page: ft.Page, use_cases: PedidoUseCases):
    # --- Contenedores dinámicos ---
    sub_opciones_container = ft.Column(spacing=10)
    # Nuevo contenedor para los colores
    contenedor_colores = ft.Row(alignment=ft.MainAxisAlignment.CENTER, visible=False)

    boton_continuar = ft.ElevatedButton("Continuar", on_click=lambda _: page.go("/extras"), visible=False)

    def check_continuar():
        """Verifica si se debe mostrar el botón de continuar."""
        pedido = use_cases.obtener_pedido_actual()
        if (pedido.tipo_decorado == "Liso c/s rosetones" and pedido.decorado_liso_color) or \
                (pedido.tipo_decorado == "Diseño o Temática" and pedido.decorado_tematica_detalle) or \
                (pedido.tipo_decorado == "Imágenes Predeterminadas" and pedido.decorado_imagen_id):
            boton_continuar.visible = True
        else:
            boton_continuar.visible = False
        page.update()

    def on_color_click(e):
        use_cases.seleccionar_color_decorado_liso(e.control.text)
        # Resaltar botón de color seleccionado
        for btn in contenedor_colores.controls:
            btn.selected = (btn == e.control)
        check_continuar()
        page.update()

    def on_sub_decorado_liso_click(e):
        # Guardamos el detalle (Chantilli/Chorreado)
        use_cases.guardar_detalle_decorado("Liso c/s rosetones", e.control.text)

        # Resaltamos el botón seleccionado
        for btn in sub_opciones_container.controls:
            if isinstance(btn, ft.ElevatedButton):
                btn.selected = (btn == e.control)

        # Mostramos los botones de colores
        contenedor_colores.controls.clear()
        colores = ["Blanco", "Rosa", "Azul", "Verde", "Amarillo"]
        for color in colores:
            contenedor_colores.controls.append(ft.FilledButton(text=color, on_click=on_color_click))
        contenedor_colores.visible = True

        check_continuar()
        page.update()

    def on_decorado_principal_click(e):
        tipo_decorado = e.control.text
        use_cases.seleccionar_tipo_decorado(tipo_decorado)

        # Limpiar opciones anteriores
        sub_opciones_container.controls.clear()
        contenedor_colores.visible = False
        boton_continuar.visible = False

        if tipo_decorado == "Liso c/s rosetones":
            sub_opciones_container.controls.extend([
                ft.ElevatedButton("Chantilli", on_click=on_sub_decorado_liso_click),
                ft.ElevatedButton("Chorreado", on_click=on_sub_decorado_liso_click),
            ])

        elif tipo_decorado == "Diseño o Temática":
            def on_text_change(e_text):
                use_cases.guardar_detalle_decorado(tipo_decorado, e_text.control.value)
                check_continuar()

            sub_opciones_container.controls.extend([
                ft.TextField(label="Escribe la temática o personaje", on_change=on_text_change),
                ft.Text(
                    "El material que se usará será acetato y no es comestible.",
                    italic=True,
                    size=12,
                    color=ft.Colors.GREY_600
                )
            ])

        elif tipo_decorado == "Imágenes Predeterminadas":
            sub_opciones_container.controls.append(
                ft.ElevatedButton("Ver Galería de Imágenes", on_click=lambda _: page.go("/galeria"))
            )

        page.update()

    botones_principales = [
        ft.ElevatedButton(text, on_click=on_decorado_principal_click)
        for text in ["Liso c/s rosetones", "Diseño o Temática", "Imágenes Predeterminadas"]
    ]

    return ft.View(
        route="/decorado",
        controls=[
            ft.Text("Paso 4: Decorado del Pastel", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Elige un estilo de decoración:"),
            ft.Row(controls=botones_principales, alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=15),
            sub_opciones_container,
            # Añadimos el nuevo contenedor de colores aquí
            contenedor_colores,
            ft.Divider(height=15),
            ft.Row(
                [
                    ft.ElevatedButton("Volver", on_click=lambda _: page.go("/categorias")),
                    boton_continuar,
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15, padding=20,
        scroll=ft.ScrollMode.ADAPTIVE
    )


# --- NUEVA VISTA DE GALERÍA ---
def vista_galeria(page: ft.Page, use_cases: PedidoUseCases):
    def on_image_click(e):
        id_imagen_seleccionada = e.control.data
        use_cases.seleccionar_imagen_decorado(id_imagen_seleccionada)
        page.go("/extras")  # Avanza a la siguiente pantalla

    # Usamos un GridView para mostrar las imágenes de forma atractiva
    grid = ft.GridView(expand=1, runs_count=2, max_extent=150, child_aspect_ratio=1.0, spacing=10, run_spacing=10)

    for img in use_cases.obtener_imagenes_galeria():
        grid.controls.append(
            ft.Container(
                content=ft.Stack([
                    ft.Image(src=img.url, fit=ft.ImageFit.COVER, border_radius=ft.border_radius.all(10)),
                    ft.Container(
                        content=ft.Text(img.descripcion, color="white"),
                        bgcolor=ft.Colors.BLACK45,
                        padding=5,
                        alignment=ft.alignment.bottom_center,
                        border_radius=ft.border_radius.all(10)
                    )
                ]),
                data=img.id,
                on_click=on_image_click,
                tooltip=f"Seleccionar {img.descripcion}"
            )
        )

    return ft.View(
        route="/galeria",
        controls=[
            ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/decorado")),
                    ft.Text("Galería de Imágenes", size=24, weight=ft.FontWeight.BOLD)]),
            grid
        ]
    )


def vista_extras(page: ft.Page, use_cases: PedidoUseCases):
    def on_radio_change(e):
        use_cases.seleccionar_extra(e.control.value)

    opciones_extra = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="Flor Artificial", label="Flor Artificial"),
            ft.Radio(value="Chorreado dorado", label="Chorreado dorado"),
            ft.Radio(value="Chorreado plateado", label="Chorreado plateado"),
        ]),
        on_change=on_radio_change,
        value=use_cases.obtener_pedido_actual().extra_seleccionado
    )

    return ft.View(
        route="/extras",
        controls=[
            ft.Text("Paso 5: ¿Deseas algún Extra?", size=30, weight=ft.FontWeight.BOLD),
            opciones_extra,
            ft.Row([
                ft.ElevatedButton("Volver", on_click=lambda _: page.go("/decorado")),
                ft.ElevatedButton("Ver Resumen", on_click=lambda _: page.go("/resumen"))
            ], alignment=ft.MainAxisAlignment.CENTER)
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )


def vista_resumen(page: ft.Page, use_cases: PedidoUseCases):
    pedido_actual = use_cases.obtener_pedido_actual()
    categorias = {c.id: c.nombre for c in use_cases.obtener_categorias()}
    nombre_categoria = categorias.get(pedido_actual.id_categoria, "No seleccionada")

    def create_summary_row(title: str, value: str):
        return ft.Row(
            [
                ft.Text(f"{title}:", weight=ft.FontWeight.BOLD, width=120),
                ft.Text(value or "No seleccionado", expand=True),
            ]
        )

    return ft.View(
        route="/resumen",
        controls=[
            ft.Text("Resumen de tu Pedido", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(height=20),
            ft.Column(
                controls=[
                    create_summary_row("Categoría", nombre_categoria),
                    create_summary_row("Fecha de Entrega", pedido_actual.fecha_entrega.strftime(
                        '%d/%m/%Y') if pedido_actual.fecha_entrega else None),
                    create_summary_row("Tamaño (Personas)", pedido_actual.tamano_pastel),
                    create_summary_row("Forma", pedido_actual.tipo_forma),
                    create_summary_row("Pan", pedido_actual.tipo_pan),
                    create_summary_row("Relleno", pedido_actual.tipo_relleno),
                    create_summary_row("Cobertura", pedido_actual.tipo_cobertura),
                    create_summary_row("Decorado", pedido_actual.tipo_decorado),
                    create_summary_row("Mensaje", pedido_actual.mensaje_pastel),
                    create_summary_row("Detalle Liso", pedido_actual.decorado_liso_detalle),
                    create_summary_row("Detalle Temática", pedido_actual.decorado_tematica_detalle),
                    create_summary_row("ID Imagen", str(pedido_actual.decorado_imagen_id)),
                    create_summary_row("Extra", pedido_actual.extra_seleccionado),
                    create_summary_row("Color", pedido_actual.decorado_liso_color),

                ],
                spacing=10
            ),
            ft.Divider(height=40),
            ft.Row(
                [
                    ft.ElevatedButton("Modificar Pedido", on_click=lambda _: page.go("/categorias")),
                    ft.ElevatedButton("Continuar", on_click=lambda _: page.go("/datos_cliente")),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )

# --- Vista de Selección de Fecha ---
def vista_fecha(page: ft.Page, use_cases: PedidoUseCases):
    # 1. Lógica de Fechas (se mantiene igual)
    fecha_hoy = datetime.date.today()
    fecha_inicial_valida = fecha_hoy + datetime.timedelta(days=4)
    fecha_final_valida = fecha_hoy + relativedelta(months=+6)

    # 2. Control para mostrar la fecha seleccionada
    texto_fecha = ft.Text("Ninguna fecha seleccionada", size=18)
    pedido_actual = use_cases.obtener_pedido_actual()
    if pedido_actual.fecha_entrega:
        texto_fecha.value = f"Fecha seleccionada: {pedido_actual.fecha_entrega.strftime('%d/%m/%Y')}"

    # 3. Manejadores de eventos
    def on_date_change(e):
        """Se ejecuta cuando el usuario selecciona una fecha en el DatePicker."""
        # 'e.control.value' es la fecha que viene del DatePicker
        fecha_seleccionada = e.control.value.date()
        use_cases.seleccionar_fecha(fecha_seleccionada)
        texto_fecha.value = f"Fecha seleccionada: {fecha_seleccionada.strftime('%d/%m/%Y')}"
        page.update()

    def open_date_picker(e):
        """
        Crea y abre el DatePicker usando page.open(), el método correcto
        para tu versión de Flet.
        """
        page.open(
            ft.DatePicker(
                first_date=fecha_inicial_valida,
                last_date=fecha_final_valida,
                on_change=on_date_change,
                on_dismiss=lambda e: print("DatePicker cerrado."),  # Opcional
                # Para mejor UX, el picker se abre en la fecha ya seleccionada o en la inicial
                value=pedido_actual.fecha_entrega if pedido_actual.fecha_entrega else fecha_inicial_valida
            )
        )

    def reiniciar_fecha(e):
        use_cases.reiniciar_fecha()
        texto_fecha.value = "Ninguna fecha seleccionada"
        page.update()

    def continuar(e):
        pedido = use_cases.obtener_pedido_actual()
        if not pedido.fecha_entrega:
            page.snack_bar = ft.SnackBar(ft.Text("Debes seleccionar una fecha para continuar."), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()
        else:
            page.go("/tamano")

    # 4. Construcción de la Vista (View)
    return ft.View(
        route="/fecha",
        controls=[
            ft.Text("Elige la fecha de entrega", size=30),
            ft.ElevatedButton(
                "Seleccionar fecha",
                icon=ft.Icons.CALENDAR_TODAY,  # El icono compatible
                on_click=open_date_picker  # La función que usa page.open()
            ),
            texto_fecha,
            ft.Divider(),


            ft.Row([
                ft.ElevatedButton("Reiniciar", on_click=reiniciar_fecha),
                ft.ElevatedButton("Continuar", on_click=continuar),
            ], alignment=ft.MainAxisAlignment.CENTER)
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )


# --- Vista de Selección de Tamaño ---
def vista_tamano(page: ft.Page, use_cases: PedidoUseCases):
    use_cases.obtener_tamanos()  # Carga los tamaños y establece el inicial
    pedido_actual = use_cases.obtener_pedido_actual()

    texto_tamano = ft.Text(pedido_actual.tamano_pastel or "No disponible", size=20, text_align=ft.TextAlign.CENTER)

    def anterior(e):
        use_cases.seleccionar_anterior_tamano()
        texto_tamano.value = use_cases.obtener_pedido_actual().tamano_pastel
        page.update()

    def siguiente(e):
        use_cases.seleccionar_siguiente_tamano()
        texto_tamano.value = use_cases.obtener_pedido_actual().tamano_pastel
        page.update()

    def reiniciar(e):
        use_cases.reiniciar_tamano()
        texto_tamano.value = use_cases.obtener_pedido_actual().tamano_pastel
        page.update()

    return ft.View(
        route="/tamano",
        controls=[
            ft.Text("Elige el tamaño del pastel", size=30),
            ft.Row([
                ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, on_click=anterior),
                ft.Container(texto_tamano, expand=False),
                ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, on_click=siguiente),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.ElevatedButton("Volver", on_click=lambda _: page.go("/fecha")),
                ft.ElevatedButton("Reiniciar", on_click=reiniciar),
                ft.ElevatedButton("Continuar", on_click=lambda _: page.go("/categorias")),
            ], alignment=ft.MainAxisAlignment.CENTER)
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )


def vista_datos_cliente(page: ft.Page, use_cases: PedidoUseCases):
    # Creamos un TextField para cada campo solicitado
    nombre = ft.TextField(label="Nombre completo")
    telefono = ft.TextField(label="Teléfono", keyboard_type=ft.KeyboardType.PHONE)
    direccion = ft.TextField(label="Dirección (Calle)")
    num_ext = ft.TextField(label="Número exterior", width=150)
    entre_calles = ft.TextField(label="Entre calles")
    cp = ft.TextField(label="Código Postal", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    colonia = ft.TextField(label="Colonia")
    ciudad = ft.TextField(label="Ciudad")
    municipio = ft.TextField(label="Municipio")
    estado = ft.TextField(label="Estado")
    referencias = ft.TextField(label="Referencias del domicilio", multiline=True, min_lines=2)

    def finalizar_pedido(e):
        # Validación simple
        if not nombre.value or not telefono.value or not direccion.value:
            page.snack_bar = ft.SnackBar(ft.Text("Nombre, teléfono y dirección son obligatorios."),
                                         bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()
            return

        # Recopilamos los datos en un diccionario
        datos_formulario = {
            "nombre_completo": nombre.value,
            "telefono": telefono.value,
            "direccion": direccion.value,
            "numero_exterior": num_ext.value,
            "entre_calles": entre_calles.value,
            "codigo_postal": cp.value,
            "colonia": colonia.value,
            "ciudad": ciudad.value,
            "municipio": municipio.value,
            "estado": estado.value,
            "referencias": referencias.value
        }

        try:
            # 1. Ejecutamos el caso de uso y obtenemos el pedido final y el QR
            pedido_final = use_cases.guardar_datos_y_finalizar(datos_formulario)

            # 2. Guardamos los datos en la sesión de la página para pasarlos a la siguiente vista
            page.session.set("pedido_final", pedido_final)

            # 3. Navegamos a la pantalla final
            page.go("/confirmacion")
        except Exception as ex:
            print(f"ERROR: Ocurrió un error al finalizar el pedido: {ex}")
            page.snack_bar = ft.SnackBar(ft.Text("Error al guardar el pedido."), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()

        # Navegamos a la pantalla final
        page.go("/confirmacion")

    return ft.View(
        route="/datos_cliente",
        controls=[
            ft.Text("Datos de Entrega", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Por favor, completa la información para finalizar tu pedido."),
            nombre,
            telefono,
            direccion,
            ft.Row([num_ext, cp]),
            entre_calles,
            colonia,
            ciudad,
            municipio,
            estado,
            referencias,
            ft.Row(
                [
                    ft.ElevatedButton("Volver al Resumen", on_click=lambda _: page.go("/resumen")),
                    ft.ElevatedButton("Finalizar Pedido", on_click=finalizar_pedido),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )


def vista_confirmacion(page: ft.Page):

    pedido_final = page.session.get("pedido_final")

    if not pedido_final:
        return ft.View("/", [ft.Text("Error: No se encontraron datos del pedido.")])


    def create_summary_row(title: str, value: str):
        return ft.Row([
            ft.Text(f"{title}:", weight=ft.FontWeight.BOLD, width=100),
            ft.Text(value or "No especificado", expand=True),
        ])

    def reiniciar_app(e):
        # Limpiamos los datos del pedido en memoria para el siguiente cliente
        # (Esto requeriría un caso de uso "reiniciar_app", por ahora solo navegamos)
        page.session.clear() # Limpiamos la sesión
        page.go("/")

    ticket_controls = [
        ft.Text("¡Pedido Confirmado!", size=30, weight=ft.FontWeight.BOLD),
        ft.Text(f"Gracias, {pedido_final.datos_entrega.nombre_completo}"),
        ft.Divider(),
        ft.Text("Detalles del Pedido:", weight=ft.FontWeight.BOLD),
        create_summary_row("Categoría ID", str(pedido_final.id_categoria)),
        create_summary_row("Fecha Entrega", pedido_final.fecha_entrega.strftime('%d/%m/%Y')),
        create_summary_row("Tamaño", pedido_final.tamano_pastel),
        create_summary_row("Forma", pedido_final.tipo_forma),
        create_summary_row("Pan", pedido_final.tipo_pan),
        create_summary_row("Relleno", pedido_final.tipo_relleno),
        create_summary_row("Cobertura", pedido_final.tipo_cobertura),
        ft.Divider(),
        ft.ElevatedButton("Iniciar Nuevo Pedido", on_click=reiniciar_app, width=300)
    ]

    return ft.View(
        route="/confirmacion",
        controls=ticket_controls,
        scroll=ft.ScrollMode.ADAPTIVE,
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        padding=20
    )

