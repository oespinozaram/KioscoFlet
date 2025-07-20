# src/infrastructure/flet_adapter/views.py
import flet as ft
import datetime
from dateutil.relativedelta import relativedelta
from src.application.use_cases import PedidoUseCases


# --- Vista de Bienvenida ---
def vista_bienvenida(page: ft.Page):
    """
    Crea la vista de bienvenida con un diseño responsivo que se adapta
    a diferentes tamaños de pantalla.
    """

    # --- Controles ---
    banner_superior = ft.Container(
        bgcolor="#89C5B0",
        padding=15,
        content=ft.ResponsiveRow(
            controls=[
                ft.Text(
                    "Para envío gratuito en compras de $500 o más",
                    color=ft.Colors.WHITE,
                    font_family="Bebas Neue",
                    size=24,
                    text_align=ft.TextAlign.CENTER,
                    col={"xs": 12}
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    texto_bienvenida = ft.Text(
        "¡ Bienvenidos a nuestra pastelería !",
        color=ft.Colors.BLACK,
        size=50,
        font_family="Bebas Neue",
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.BOLD
    )

    boton_continuar = ft.Container(
        width=255,
        height=77,
        bgcolor="#DC6262",
        border_radius=ft.border_radius.all(20),
        content=ft.Text(
            "Continuar",
            color=ft.Colors.WHITE,
            size=36,
            font_family="Bebas Neue",
        ),
        alignment=ft.alignment.center,
        on_click=lambda _: page.go("/fecha")
    )

    # --- Layout Principal ---
    # Usamos un Container con fondo de imagen y una Columna para centrar el contenido.
    contenido_superpuesto = ft.Column(
        expand=True,
        controls=[
            banner_superior,
            ft.Container(expand=True),  # Espaciador flexible
            ft.ResponsiveRow(
                controls=[
                    ft.Container(col={"lg": 2, "xl": 3}),
                    ft.Column(
                        controls=[
                            texto_bienvenida,
                            ft.Container(height=50),
                            boton_continuar
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        col={"xs": 12, "sm": 12, "md": 8, "lg": 8, "xl": 6}
                    ),
                    ft.Container(col={"lg": 2, "xl": 3}),
                ]
            ),
            ft.Container(expand=True),  # Espaciador flexible
        ]
    )

    # --- Layout Final usando Stack ---
    # Este es el método correcto para poner un fondo de imagen en tu versión.
    layout_final = ft.Stack(
        controls=[
            # Capa 1 (Fondo): La imagen que ocupa todo el espacio.
            ft.Image(
                src="https://placehold.co/1024x1366",
                fit=ft.ImageFit.COVER,
                expand=True,
            ),
            # Capa 2 (Frente): Todo el contenido interactivo.
            contenido_superpuesto,
        ]
    )

    return ft.View(
        route="/",
        controls=[
            layout_final
        ],
        padding=0,
    )


def vista_fecha(page: ft.Page, use_cases: PedidoUseCases):
    # --- 1. Lógica y Manejadores de Eventos (Actualizados) ---

    # Primero, definimos el control que mostrará el texto, para poder actualizarlo después.
    texto_del_boton = ft.Text(
        # Si ya hay una fecha guardada en el pedido, la mostramos.
        value=f"Fecha: {use_cases.obtener_pedido_actual().fecha_entrega.strftime('%d/%m/%Y')}" if use_cases.obtener_pedido_actual().fecha_entrega else "Elige la fecha de entrega",
        color=ft.Colors.WHITE,
        size=40,
        font_family="Bebas Neue",
        weight=ft.FontWeight.W_400,
    )

    def on_date_change(e):
        """Se ejecuta cuando el usuario selecciona una fecha en el calendario."""
        fecha_seleccionada = e.control.value.date()
        use_cases.seleccionar_fecha(fecha_seleccionada)

        # --- CAMBIO: Escribimos la fecha seleccionada en la pantalla ---
        # Actualizamos el valor del control de texto que definimos antes.
        texto_del_boton.value = f"Fecha: {fecha_seleccionada.strftime('%d/%m/%Y')}"
        page.update()

    # Calculamos las fechas válidas para el DatePicker
    fecha_hoy = datetime.date.today()
    fecha_inicial_valida = fecha_hoy + datetime.timedelta(days=4)
    fecha_final_valida = fecha_hoy + relativedelta(months=+6)

    def open_date_picker(e):
        """Abre el selector de fecha."""
        page.open(
            ft.DatePicker(
                first_date=fecha_inicial_valida,
                last_date=fecha_final_valida,
                on_change=on_date_change,
                value=use_cases.obtener_pedido_actual().fecha_entrega or fecha_inicial_valida
            )
        )

    def continuar(e):
        """Verifica si hay una fecha antes de continuar."""
        pedido = use_cases.obtener_pedido_actual()

        # --- CAMBIO: Añadimos la validación ---
        if not pedido.fecha_entrega:
            # Si no hay fecha, mostramos un mensaje de error.
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Por favor, selecciona una fecha para continuar."),
                bgcolor=ft.Colors.RED_ACCENT_700
            )
            page.snack_bar.open = True
            page.update()
        else:
            # Si hay fecha, navegamos a la siguiente pantalla.
            page.go("/tamano")

    # --- 2. Construcción del Layout ---

    # El botón principal ahora usa el control de texto que definimos al inicio.
    boton_fecha = ft.Container(
        width=580,
        height=110,
        bgcolor="#89C5B0",
        border_radius=ft.border_radius.all(20),
        shadow=ft.BoxShadow(
            spread_radius=1, blur_radius=10,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(4, 4),
        ),
        content=texto_del_boton,  # Usamos el control de texto aquí
        alignment=ft.alignment.center,
        on_click=open_date_picker,
        animate_scale=ft.Animation(600, ft.AnimationCurve.EASE_OUT_BACK)
    )

    # El layout con el fondo y el panel semitransparente
    layout_con_fondo = ft.Stack(
        controls=[
            ft.Image(
                src="https://images.pexels.com/photos/1070945/pexels-photo-1070945.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
                fit=ft.ImageFit.COVER,
                expand=True,
            ),
            ft.Container(
                bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.WHITE),
                border_radius=ft.border_radius.all(20),
                padding=30,
                content=ft.Column(
                    [
                        ft.Text("Paso 1", size=20, color=ft.Colors.BLACK),
                        ft.Text("Fecha de Entrega", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                        ft.Container(height=30),
                        boton_fecha,
                        ft.Container(height=30),
                        ft.Row(
                            [
                                ft.ElevatedButton("Volver", on_click=lambda _: page.go("/")),
                                # --- CAMBIO: El botón ahora llama a nuestra función de validación ---
                                ft.ElevatedButton("Continuar", on_click=continuar),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )

    return ft.View(
        route="/fecha",
        controls=[
            layout_con_fondo
        ],
        padding=0
    )


# --- VISTA DE TAMAÑO (CON NUEVO DISEÑO) ---
def vista_tamano(page: ft.Page, use_cases: PedidoUseCases):
    # --- 1. Lógica y Manejadores de Eventos (Sin cambios) ---
    use_cases.obtener_tamanos()
    pedido_actual = use_cases.obtener_pedido_actual()

    texto_tamano = ft.Text(
        value=pedido_actual.tamano_pastel or "N/A",
        size=48,
        font_family="Bebas Neue",
        color="#623F19",
        text_align=ft.TextAlign.CENTER
    )

    def anterior(e):
        use_cases.seleccionar_anterior_tamano()
        texto_tamano.value = use_cases.obtener_pedido_actual().tamano_pastel
        page.update()

    def siguiente(e):
        use_cases.seleccionar_siguiente_tamano()
        texto_tamano.value = use_cases.obtener_pedido_actual().tamano_pastel
        page.update()

    # --- 2. Construcción del Panel Interactivo ---
    # Este es el recuadro blanco donde el usuario interactúa.
    panel_interactivo = ft.Container(
        width=600,  # Ligeramente más angosto para mejor visibilidad
        padding=30,
        bgcolor=ft.Colors.with_opacity(0.95, ft.Colors.WHITE),
        border_radius=ft.border_radius.all(40),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(4, 4),
        ),
        content=ft.Column(
            [
                ft.Text(
                    '¿Para cuántas personas es tu pastel?',
                    size=48,
                    font_family="Bebas Neue",
                    color="#815E43",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=20),

                # El contador interactivo
                ft.Container(
                    width=333,
                    height=95,
                    border=ft.border.all(5, color=ft.Colors.with_opacity(0.77, "#623F19")),
                    border_radius=ft.border_radius.all(20),
                    content=ft.Row(
                        [
                            ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, icon_size=40, on_click=anterior),
                            ft.Container(content=texto_tamano, expand=True, alignment=ft.alignment.center),
                            ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, icon_size=40, on_click=siguiente),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ),
                ft.Container(height=30),

                # Botones de navegación
                ft.Row(
                    [
                        ft.Container(
                            width=137,
                            height=45,
                            bgcolor=ft.Colors.BLUE_GREY_300,  # Un color neutro
                            border_radius=ft.border_radius.all(10),
                            content=ft.Text("Volver", color=ft.Colors.WHITE, size=20, font_family="Bebas Neue"),
                            alignment=ft.alignment.center,
                            on_click=lambda _: page.go("/fecha"),
                        ),
                        ft.Container(
                            width=137,
                            height=45,
                            bgcolor="#E5ADAD",
                            border_radius=ft.border_radius.all(10),
                            content=ft.Text("Continuar", color=ft.Colors.WHITE, size=20, font_family="Bebas Neue"),
                            alignment=ft.alignment.center,
                            on_click=lambda _: page.go("/categorias"),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # --- 3. Construcción del Layout Final ---
    layout_final = ft.Stack(
        controls=[
            # Capa 1: La imagen de fondo que ocupa todo el espacio.
            ft.Image(
                src="https://images.pexels.com/photos/1721934/pexels-photo-1721934.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
                fit=ft.ImageFit.COVER,
                expand=True,  # Clave para que la imagen llene el fondo del Stack.
            ),

            # Capa 2: Un Container que centra el panel interactivo encima de la imagen.
            ft.Container(
                content=panel_interactivo,
                alignment=ft.alignment.center,
                expand=True,  # Clave para que el centrado funcione correctamente.
            ),
        ]
    )

    return ft.View(
        route="/tamano",
        controls=[
            layout_final
        ],
        padding=0
    )

def vista_categorias(page: ft.Page, use_cases: PedidoUseCases):
    # --- Contenedores dinámicos ---
    contenedor_formas = ft.Row(wrap=True, spacing=10, run_spacing=10, alignment=ft.MainAxisAlignment.CENTER)
    contenedor_panes = ft.Row(wrap=True, spacing=10, run_spacing=10, alignment=ft.MainAxisAlignment.CENTER)
    contenedor_rellenos = ft.Row(wrap=True, spacing=10, run_spacing=10, alignment=ft.MainAxisAlignment.CENTER)

    # Secciones completas
    seccion_formas = ft.Column([ft.Text("Selecciona la forma:"), contenedor_formas],
                               horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, visible=False)
    seccion_panes = ft.Column([ft.Text("Selecciona el tipo de pan:"), contenedor_panes],
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, visible=False)
    seccion_rellenos = ft.Column([ft.Text("Selecciona el relleno:"), contenedor_rellenos],
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, visible=False)

    acciones_finales = ft.Row(alignment=ft.MainAxisAlignment.CENTER, visible=False)


    # --- Lógica de la Interfaz ---
    def check_and_show_final_actions():
        pedido = use_cases.obtener_pedido_actual()
        if pedido.tipo_forma and pedido.tipo_pan and pedido.tipo_relleno:  # Añadida condición
            acciones_finales.visible = True
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

        for cont in [contenedor_formas, contenedor_panes, contenedor_rellenos]: cont.controls.clear()
        for sec in [seccion_formas, seccion_panes, seccion_rellenos, acciones_finales]: sec.visible = False

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
            ft.Text("Elige una categoría:"),
            ft.Row(controls=botones_categorias, wrap=True, spacing=10, run_spacing=10, alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=10),
            seccion_formas,
            seccion_panes,
            seccion_rellenos,
            ft.Divider(height=10),
            acciones_finales,
        ],
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        scroll=ft.ScrollMode.ADAPTIVE
    )


def vista_decorado(page: ft.Page, use_cases: PedidoUseCases):
    # --- 1. Definición de Controles de la Interfaz ---
    # Se definen todos los controles que se manipularán dinámicamente.

    contenedor_coberturas = ft.Row(wrap=True, spacing=10, run_spacing=10, alignment=ft.MainAxisAlignment.CENTER)

    campo_mensaje = ft.TextField(
        label="Mensaje en el pastel (opcional)",
        value=use_cases.obtener_pedido_actual().mensaje_pastel or ""
    )

    # Contenedores para las opciones que aparecen y desaparecen
    sub_opciones_container = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    tematica_container = ft.Column(
        visible=False,
        controls=[
            ft.TextField(label="Escribe la temática o personaje"),
            ft.Text(
                "El material que se usará será acetato y no es comestible.",
                italic=True,
                size=12,
                color=ft.Colors.GREY_600  # Sintaxis correcta: ft.colors
            )
        ]
    )
    dd_color1 = ft.Dropdown(label="Color Principal", expand=True)
    dd_color2 = ft.Dropdown(label="Color Secundario (opcional)", expand=True)
    contenedor_colores = ft.Row(controls=[dd_color1, dd_color2], visible=False)

    boton_continuar = ft.ElevatedButton(
        "Continuar a Extras",
        on_click=lambda _: page.go("/extras"),
        visible=False
    )

    # Panel principal para las opciones de decorado, inicialmente oculto
    panel_decorado = ft.Column(
        visible=False,
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # --- 2. Lógica y Manejadores de Eventos ---

    def check_continuar():
        """Verifica si se debe mostrar el botón de continuar basado en las selecciones."""
        pedido = use_cases.obtener_pedido_actual()
        listo_para_continuar = False

        if pedido.tipo_cobertura:
            if pedido.tipo_decorado == "Liso c/s Conchas de Betún":
                if pedido.decorado_liso_detalle and pedido.decorado_liso_color1:
                    if pedido.decorado_liso_detalle == "Diseño o Temática":
                        if pedido.decorado_tematica_detalle:
                            listo_para_continuar = True
                    else:
                        listo_para_continuar = True

        boton_continuar.visible = listo_para_continuar
        page.update()

    def on_color_change(e):
        """Guarda los colores seleccionados y verifica si se puede continuar."""
        use_cases.seleccionar_colores_decorado(dd_color1.value, dd_color2.value)
        check_continuar()

    dd_color1.on_change = on_color_change
    dd_color2.on_change = on_color_change

    def on_sub_opcion_liso_click(e):
        """Manejador para 'Chantilli', 'Chorreado' y 'Diseño'."""
        detalle = e.control.text
        use_cases.guardar_detalle_decorado("Liso c/s Conchas de Betún", detalle)

        for btn in sub_opciones_container.controls:
            if isinstance(btn, ft.ElevatedButton): btn.selected = (btn == e.control)

        # Siempre muestra los selectores de color
        colores_disponibles = use_cases.obtener_colores_disponibles()
        opciones_color = [ft.dropdown.Option(color) for color in colores_disponibles] or [
            ft.dropdown.Option(key="no-color", text="No hay opciones", disabled=True)]

        dd_color1.options = opciones_color
        dd_color2.options = opciones_color
        dd_color1.value = None
        dd_color2.value = None
        contenedor_colores.visible = True

        # Muestra el campo de texto de temática solo si es necesario
        if detalle == "Diseño o Temática":
            def on_text_tematica_change(e_text):
                use_cases.guardar_detalle_decorado("Liso c/s Conchas de Betún", detalle, e_text.control.value)
                check_continuar()

            tematica_container.controls[0].on_change = on_text_tematica_change
            tematica_container.visible = True
        else:
            tematica_container.visible = False

        check_continuar()
        page.update()

    def on_decorado_principal_click(e):
        """Manejador para 'Liso...' o 'Imágenes...'."""
        tipo_decorado = e.control.text
        use_cases.seleccionar_tipo_decorado(tipo_decorado)
        use_cases.guardar_mensaje_pastel(campo_mensaje.value)

        if tipo_decorado == "Imágenes Predeterminadas":
            page.go("/galeria")
            return

        sub_opciones_container.controls.clear()
        contenedor_colores.visible = False
        tematica_container.visible = False
        boton_continuar.visible = False

        sub_opciones_container.controls.extend([
            ft.ElevatedButton("Chantilli", on_click=on_sub_opcion_liso_click),
            ft.ElevatedButton("Chorreado", on_click=on_sub_opcion_liso_click),
            ft.ElevatedButton("Diseño o Temática", on_click=on_sub_opcion_liso_click),
        ])
        page.update()

    def on_cobertura_click(e):
        """Manejador principal que activa el resto de las opciones de la pantalla."""
        use_cases.seleccionar_tipo_cobertura(e.control.text)

        for btn in contenedor_coberturas.controls:
            if isinstance(btn, ft.FilledButton): btn.selected = (btn == e.control)

        # Resetea las opciones de decorado para una nueva selección
        use_cases.seleccionar_tipo_decorado(None)
        sub_opciones_container.controls.clear()
        contenedor_colores.visible = False
        tematica_container.visible = False
        boton_continuar.visible = False

        panel_decorado.visible = True
        page.update()

    # --- 3. Construcción del Layout ---

    # Se define el contenido estático del panel de decorado
    panel_decorado.controls = [
        ft.Divider(height=10),
        ft.Text("Después, elige un estilo de decoración:"),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ElevatedButton("Liso c/s Conchas de Betún", on_click=on_decorado_principal_click),
                ft.ElevatedButton("Imágenes Predeterminadas", on_click=on_decorado_principal_click),
            ]
        ),
        ft.Divider(height=15),
        sub_opciones_container,
        tematica_container,
        contenedor_colores,
    ]

    # Carga inicial de las coberturas al entrar a la vista
    pedido_actual = use_cases.obtener_pedido_actual()
    if pedido_actual.id_categoria and pedido_actual.tipo_pan:
        panes_disponibles = use_cases.obtener_panes_por_categoria(pedido_actual.id_categoria)
        pan_obj = next((p for p in panes_disponibles if p.nombre == pedido_actual.tipo_pan), None)

        if pan_obj:
            lista_coberturas = use_cases.obtener_coberturas_disponibles(pedido_actual.id_categoria, pan_obj.id)
            if lista_coberturas:
                for cobertura in lista_coberturas:
                    contenedor_coberturas.controls.append(ft.FilledButton(text=cobertura, on_click=on_cobertura_click))
            else:
                contenedor_coberturas.controls.append(ft.Text("No hay coberturas disponibles para esta selección."))
        else:
            contenedor_coberturas.controls.append(ft.Text("Error al cargar coberturas.", color=ft.Colors.RED))
    else:
        contenedor_coberturas.controls.append(ft.Text("Selección de categoría o pan inválida.", color=ft.Colors.RED))

    # Se retorna la vista final ensamblada
    return ft.View(
        route="/decorado",
        controls=[
            ft.Text("Paso 4: Cobertura y Decorado", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Primero, elige la cobertura:"),
            contenedor_coberturas,

            # El campo de mensaje se sitúa después de la cobertura
            campo_mensaje,

            # Panel con el resto de opciones de decorado
            panel_decorado,

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
    # --- Controles de la Interfaz ---
    grid = ft.GridView(
        expand=1,
        runs_count=2,
        max_extent=180,  # Un poco más de espacio para las imágenes
        child_aspect_ratio=0.8,  # Ajustado para imagen + texto
        spacing=10,
        run_spacing=10
    )

    # --- Manejadores de Eventos ---
    def on_image_click(e):
        id_imagen_seleccionada = e.control.data
        use_cases.seleccionar_imagen_decorado(id_imagen_seleccionada)
        page.go("/extras")

    def actualizar_galeria(e=None):  # Ahora acepta el evento 'e'
        categoria_filtro = filtro_categoria.value if filtro_categoria.value != "Todas" else None
        termino_busqueda = campo_busqueda.value

        grid.controls.clear()

        imagenes = use_cases.buscar_imagenes_galeria(categoria_filtro, termino_busqueda)
        for img in imagenes:
            grid.controls.append(
                ft.Container(
                    data=img.id,
                    on_click=on_image_click,
                    tooltip=f"Seleccionar {img.descripcion}",
                    border_radius=ft.border_radius.all(10),
                    content=ft.Stack(
                        # --- CÓDIGO CORREGIDO AQUÍ ---
                        # Reemplazamos el '...' con los controles de imagen y texto reales.
                        [
                            ft.Image(
                                src=img.url,
                                fit=ft.ImageFit.COVER,
                                border_radius=ft.border_radius.all(10)
                            ),
                            ft.Container(
                                content=ft.Text(img.descripcion, color="white", weight=ft.FontWeight.BOLD),
                                bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
                                padding=8,
                                alignment=ft.alignment.bottom_center,
                                border_radius=ft.border_radius.all(10),
                                gradient=ft.LinearGradient(
                                    begin=ft.alignment.top_center,
                                    end=ft.alignment.bottom_center,
                                    colors=[ft.Colors.TRANSPARENT, ft.Colors.BLACK],
                                )
                            )
                        ]
                        # -----------------------------
                    )
                )
            )
        page.update()

    # --- Controles de Filtro y Búsqueda ---
    filtro_categoria = ft.Dropdown(
        label="Filtrar por categoría",
        options=[ft.dropdown.Option("Todas"), ft.dropdown.Option("Infantil"), ft.dropdown.Option("Floral")],
        value="Todas",
        on_change=actualizar_galeria,
        expand=True
    )
    campo_busqueda = ft.TextField(
        label="Buscar...",
        on_change=actualizar_galeria,
        expand=True
    )

    # Carga inicial de la galería
    actualizar_galeria()

    # --- Construcción de la Vista ---
    return ft.View(
        route="/galeria",
        controls=[
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/decorado"), tooltip="Volver"),
                ft.Text("Galería de Imágenes", size=24, weight=ft.FontWeight.BOLD)
            ]),
            ft.Row([filtro_categoria, campo_busqueda]),
            # El GridView se expandirá para usar el espacio restante
            grid
        ]
    )


def vista_extras(page: ft.Page, use_cases: PedidoUseCases):
    def on_radio_change(e):
        use_cases.seleccionar_extra(e.control.value)

    opciones_extra = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="Ninguno", label="Ninguno"),
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
    # 1. Obtenemos el estado final del pedido desde los casos de uso
    pedido_actual = use_cases.obtener_pedido_actual()

    # Para mostrar el nombre de la categoría en lugar de solo el ID
    categorias = {c.id: c.nombre for c in use_cases.obtener_categorias()}
    nombre_categoria = categorias.get(pedido_actual.id_categoria, "No seleccionada")

    # --- 2. Función de Ayuda para Crear Filas ---
    def create_summary_row(title: str, value: str | None):
        """
        Crea una fila de resumen consistente. Si el valor es None o está vacío,
        muestra 'No especificado' para mayor claridad.
        """
        return ft.Row(
            [
                ft.Text(f"{title}:", weight=ft.FontWeight.BOLD, width=150),
                ft.Text(value if value else "No especificado", expand=True),
            ]
        )

    # --- 3. Construcción de la Lista de Controles del Resumen ---
    # Creamos una lista para añadir dinámicamente solo los detalles relevantes.

    controles_resumen = [
        # --- Detalles Generales ---
        create_summary_row("Categoría", nombre_categoria),
        create_summary_row("Fecha de Entrega",
                           pedido_actual.fecha_entrega.strftime('%d/%m/%Y') if pedido_actual.fecha_entrega else None),
        create_summary_row("Tamaño (personas)", pedido_actual.tamano_pastel),
        create_summary_row("Forma", pedido_actual.tipo_forma),
        create_summary_row("Pan", pedido_actual.tipo_pan),
        create_summary_row("Relleno", pedido_actual.tipo_relleno),
        create_summary_row("Cobertura", pedido_actual.tipo_cobertura),
        create_summary_row("Extra", pedido_actual.extra_seleccionado),
        ft.Divider(),

        # --- Detalles del Decorado ---
        ft.Text("Detalles del Decorado:", weight=ft.FontWeight.BOLD, size=18),
        create_summary_row("Mensaje en Pastel", pedido_actual.mensaje_pastel),
        create_summary_row("Estilo Principal", pedido_actual.tipo_decorado),
    ]

    # --- Lógica Condicional para mostrar solo los detalles relevantes ---
    if pedido_actual.tipo_decorado == "Liso c/s Conchas de Betún":
        controles_resumen.append(create_summary_row("  ↳ Detalle", pedido_actual.decorado_liso_detalle))
        # --- CAMBIO: Mostramos los colores y la temática si existen ---
        if pedido_actual.decorado_liso_detalle == "Diseño o Temática":
            controles_resumen.append(create_summary_row("  ↳ Temática", pedido_actual.decorado_tematica_detalle))

        # Mostramos los colores para TODAS las opciones de "Liso"
        controles_resumen.append(create_summary_row("  ↳ Color Principal", pedido_actual.decorado_liso_color1))
        controles_resumen.append(create_summary_row("  ↳ Color Secundario", pedido_actual.decorado_liso_color2))

    elif pedido_actual.tipo_decorado == "Imágenes Predeterminadas":
        controles_resumen.append(create_summary_row("  ↳ ID de Imagen", str(pedido_actual.decorado_imagen_id)))
        if pedido_actual.decorado_imagen_id:
            url_imagen = use_cases.obtener_url_imagen_galeria_por_id(pedido_actual.decorado_imagen_id)
            if url_imagen:
                controles_resumen.append(
                    ft.Row([
                        ft.Text("  ↳ Miniatura:", weight=ft.FontWeight.BOLD, width=150),
                        ft.Image(src=url_imagen, width=100, height=100, fit=ft.ImageFit.CONTAIN, border_radius=ft.border_radius.all(5)),
                    ])
                )

    # --- 4. Construcción del Layout Final de la Vista ---
    return ft.View(
        route="/resumen",
        controls=[
            ft.Text("Resumen de tu Pedido", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Por favor, verifica que toda la información sea correcta."),
            ft.Divider(height=20),

            # Usamos la lista de controles que acabamos de construir
            ft.Column(controls=controles_resumen, spacing=8),

            ft.Divider(height=30),
            ft.Row(
                [
                    ft.ElevatedButton("Modificar Pedido", on_click=lambda _: page.go("/decorado")),
                    ft.ElevatedButton("Continuar", on_click=lambda _: page.go("/datos_cliente")),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
        padding=20,
        scroll=ft.ScrollMode.ADAPTIVE
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

