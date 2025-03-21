"""
GUI front-end to https://wttr.in/.
"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QComboBox,
    QGridLayout,
    QLabel,
)

from wttrman.wttr import Wttr
from wttrman.yaml_file_handler import YamlFileHandler

config_file = YamlFileHandler("resources/configs/config.yaml")
config = config_file.load_yaml_file()

themes_file = YamlFileHandler("resources/configs/themes.yaml")
themes = themes_file.load_yaml_file()

locations_file = YamlFileHandler("resources/configs/locations.yaml")
locations = locations_file.load_yaml_file()


class Wttrman(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.show()

        # * Set window default settings
        self.setWindowTitle(config["window_title"])
        self.setFixedSize(
            config["window_size"]["width"], config["window_size"]["height"]
        )

        # * Create widgets
        self.get_weather = QPushButton("Get Weather")

        self.city = QComboBox()
        self.city.addItem("Select City")

        self.state = QComboBox()
        self.state.addItem("Select State")
        self.state.addItems(state for state in locations["states"])

        self.theme_toggle = QPushButton("Dark")

        self.weather = QLabel(
            " ", alignment=Qt.AlignmentFlag.AlignCenter, wordWrap=True
        )
        self.weather.setFixedWidth(config["weather_widget_width"])

        # * Define button connections
        self.get_weather.pressed.connect(self.wttr)
        self.state.currentIndexChanged.connect(self.update_cities)
        self.theme_toggle.pressed.connect(self.toggle_theme)

        # * Create layouts
        self.page = QGridLayout()
        self.inputs = QGridLayout()
        self.inputs.setVerticalSpacing(5)
        self.outputs = QGridLayout()

        # * Add widgets to layouts
        self.inputs.addWidget(self.get_weather, 0, 0, 1, 2)
        self.inputs.addWidget(self.state, 1, 0, 1, 2)
        self.inputs.addWidget(self.city, 2, 0, 1, 2)
        self.inputs.addWidget(self.theme_toggle, 3, 0, 1, 2)

        self.outputs.addWidget(self.weather, 0, 0, 1, 2)

        # * Setup overall page layout and set default window theme
        self.page.addLayout(self.inputs, 0, 0)
        self.page.addLayout(self.outputs, 0, 1)

        self.gui = QWidget()
        self.gui.setLayout(self.page)

        self.setCentralWidget(self.gui)

        self.apply_theme(self.theme_toggle.text().lower())
        self.set_font()

    def wttr(self):
        forecast = Wttr()
        if self.state.currentText() == "Select State":
            self.weather.setText("You must select a state!")
        elif self.city.currentText() == "Select City":
            self.weather.setText("You must select a city!")
        else:
            self.weather.setText(
                forecast.get_weather(
                    self.city.currentText(),
                    self.state.currentText(),
                )
            )

    def update_cities(self):
        self.city.clear()
        self.city.addItem("Select City")
        self.city.addItems(
            city for city in locations["cities"][self.state.currentText()]
        )

    def toggle_theme(self):
        if self.theme_toggle.text() == "Dark":
            self.theme_toggle.setText("Light")
            theme = self.theme_toggle.text()
        else:
            self.theme_toggle.setText("Dark")
            theme = self.theme_toggle.text()

        self.apply_theme(theme.lower())

    def apply_theme(self, theme):
        self.main_stylesheet = f"""
            background-color: {themes[theme]["background-color"]};
            color: {themes[theme]["color"]};
            border: {themes[theme]["border"]};
            border-radius: {themes["general"]["border-radius"]};
            padding: {themes["general"]["padding"]};
            """
        self.widget_stylesheet = f"""
            background-color: {themes[theme]["widget-background-color"]};
            """
        self.setStyleSheet(self.main_stylesheet)
        self.get_weather.setStyleSheet(self.widget_stylesheet)
        self.city.setStyleSheet(self.widget_stylesheet)
        self.state.setStyleSheet(self.widget_stylesheet)
        self.weather.setStyleSheet(self.widget_stylesheet)
        self.theme_toggle.setStyleSheet(self.widget_stylesheet)

        (
            self.theme_toggle.setText("Dark")
            if theme == "dark"
            else self.theme_toggle.setText("Light")
        )

    def set_font(self):
        font = QFont("Commit Mono Nerd Font", 10)
        weather_font = QFont("Commit Mono Nerd Font", 12)

        self.setFont(font)
        self.get_weather.setFont(font)
        self.city.setFont(font)
        self.state.setFont(font)
        self.weather.setFont(weather_font)
        self.theme_toggle.setFont(font)


def main():
    app = QApplication(sys.argv)
    main_window = Wttrman()  # noqa: F841
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
