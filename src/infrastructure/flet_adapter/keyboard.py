import flet as ft


class VirtualKeyboard:
    def __init__(self, page: ft.Page, on_key, on_enter=None, on_hide=None):
        super().__init__()
        self.page = page
        self.on_key = on_key
        self.on_enter = on_enter
        self.on_hide = on_hide
        self.shift_active = False
        self.keyboard_control = self._build_controls()

    def _create_key(self, text: str, data: str, expand: int = 1):
        """Función de ayuda para crear cada tecla."""
        return ft.Container(
            content=ft.Text(text, size=20),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.WHITE24,
            border_radius=5,
            expand=expand,
            on_click=self._key_click,
            data=data,
        )

    def _key_click(self, e):
        key_data = e.control.data

        if key_data == "SHIFT":
            self.shift_active = not self.shift_active
            self._update_keys()

        elif key_data == "ENTER":
            if self.on_enter:
                self.on_enter(e)

        elif key_data == "HIDE":
            if self.on_hide:
                self.on_hide(e)
        else:

            if self.shift_active:
                self.on_key(key_data.upper())
                self.shift_active = False
                self._update_keys()
            else:
                self.on_key(key_data)

    def _update_keys(self):

        for row in self.keyboard_control.content.controls:
            for key in row.controls:
                key_text = key.content.value
                if len(key_text) == 1:
                    key.content.value = key_text.upper() if self.shift_active else key_text.lower()
        self.page.update()

    def _build_controls(self):

        keys_layout = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l", "ñ"],
            ["SHIFT", "z", "x", "c", "v", "b", "n", "m", "BACKSPACE"],
            ["HIDE", "SPACE", "ENTER"]
        ]

        keyboard_rows = []
        for row_keys in keys_layout:
            keys_in_row = []
            for key in row_keys:
                if key == "SHIFT":
                    keys_in_row.append(self._create_key("⇧", "SHIFT", 2))
                elif key == "BACKSPACE":
                    keys_in_row.append(self._create_key("⌫", "BACKSPACE", 2))
                elif key == "SPACE":
                    keys_in_row.append(self._create_key(" ", " ", 6))
                elif key == "ENTER":
                    keys_in_row.append(self._create_key("ENTRAR", "ENTER", 3))
                elif key == "HIDE":
                    keys_in_row.append(self._create_key("▼", "HIDE", 2))
                else:
                    keys_in_row.append(self._create_key(key, key))
            keyboard_rows.append(ft.Row(controls=keys_in_row, spacing=5, height=50))

        return ft.Container(
            ft.Column(controls=keyboard_rows, spacing=5),
            padding=10,
            bgcolor=ft.Colors.BLACK26,
            border_radius=10
        )

    def build(self):
        return self.keyboard_control