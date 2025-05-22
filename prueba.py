from kivymd.app import MDApp
from kivy.lang import Builder

KV = '''
MDScreen:
    md_bg_color: app.theme_cls.backgroundColor

    MDBoxLayout:
        orientation: "vertical"
        spacing: "20dp"
        padding: "20dp"
        adaptive_height: True
        pos_hint: {"center_x": 0.5, "center_y": 0.5}

        MDLabel:
            text: "ReflectApp - Test KivyMD"
            font_style: "H5"
            halign: "center"
            size_hint_y: None
            height: "60dp"

        MDTextField:
            id: input_field
            hint_text: "Escribe algo aquí..."
            size_hint_x: None
            width: "300dp"
            pos_hint: {"center_x": 0.5}

        MDButton:
            style: "elevated"
            pos_hint: {"center_x": 0.5}
            on_release: app.button_clicked()

            MDButtonText:
                text: "Probar"

        MDLabel:
            id: result_label
            text: "Presiona el botón para probar"
            halign: "center"
            size_hint_y: None
            height: "40dp"
'''

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def button_clicked(self):
        text = self.root.ids.input_field.text.strip()
        if text:
            self.root.ids.result_label.text = f"Escribiste: {text}"
        else:
            self.root.ids.result_label.text = "El campo está vacío"

MainApp().run()
