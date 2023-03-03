from flask import Flask

__all__ = ["App"]


class App(Flask):
    def __init__(self, name):
        super().__init__(name, static_folder='./static', template_folder='./templates')
        self.config.update(debug=True)
        self.debug_value = False
