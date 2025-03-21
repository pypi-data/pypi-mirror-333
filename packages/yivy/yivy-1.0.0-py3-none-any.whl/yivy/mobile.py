from kivy.app import App
from kivy.uix.label import Label as KivyLabel
from kivy.uix.button import Button as KivyButton
from kivy.uix.boxlayout import BoxLayout

class MobileApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        label = KivyLabel(text="Hello from Yivy Mobile!")
        button = KivyButton(text="Click Me")
        layout.add_widget(label)
        layout.add_widget(button)
        return layout