import sys
from PySide6.QtWidgets import QApplication, QWidget, QTableView, QVBoxLayout
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from ui_form import Ui_Widget
import requests
from datetime import datetime, timedelta

class WeatherControl:
    @staticmethod
    def get_location():
        """Получение местоположения пользователя по IP адресу."""
        response = requests.get("http://ip-api.com/json/")
        if response.status_code == 200:
            data = response.json()
            city = data.get("city")
            lat = data.get("lat")
            lon = data.get("lon")

            if city:
                print(f"Определенное местоположение: {city}")
                return city, lat, lon
        print("Не удалось определить местоположение.")
        return "Неизвестный город", None, None

    @staticmethod
    def get_weather_data(lat, lon):
        """Получение данных о погоде с помощью Open-Meteo API."""
        if lat is None or lon is None:
            return None
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,weathercode",
            "timezone": "auto"
        }
        response = requests.get("https://api.open-meteo.com/v1/forecast", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print("Ошибка при получении данных о погоде:", response.status_code)
            return None

    @staticmethod
    def get_weather_description(code):
        """Расшифровка кода погоды Open-Meteo."""
        weather_codes = {
            0: "Ясно",
            1: "Преимущественно ясно",
            2: "Переменная облачность",
            3: "Пасмурно",
            45: "Туман",
            48: "Туман с изморозью",
            51: "Лёгкая морось",
            61: "Слабый дождь",
            63: "Умеренный дождь",
            65: "Сильный дождь",
            71: "Лёгкий снег",
            73: "Умеренный снег",
            75: "Сильный снег",
            95: "Гроза",
        }
        return weather_codes.get(code, "Неизвестное состояние")

    @staticmethod
    def parse_three_day_forecast(data):
        """Парсинг прогноза погоды для ближайших 3 дней по временным интервалам."""
        if not data:
            return []

        hourly_data = data["hourly"]
        time = hourly_data["time"]
        temperatures = hourly_data["temperature_2m"]
        weather_codes = hourly_data["weathercode"]

        forecast = []
        now = datetime.now()

        for day_offset in range(5):
            current_date = (now + timedelta(days=day_offset)).strftime('%Y-%m-%d')
            daily_forecast = {"date": current_date, "hours": []}

            for hour in range(0, 24, 3):  # Интервалы через каждые 3 часа
                target_time = f"{current_date}T{hour:02}:00"
                if target_time in time:
                    idx = time.index(target_time)
                    temp = temperatures[idx]
                    condition = WeatherControl.get_weather_description(weather_codes[idx])
                    daily_forecast["hours"].append(f"{hour:02}:00\n{condition}\n{temp}°C")
            forecast.append(daily_forecast)
        return forecast


class WeatherTableModel(QAbstractTableModel):
    def __init__(self, forecast_data, parent=None):
        super().__init__(parent)
        self.forecast_data = forecast_data
        self.headers = ["Дата"] + [f"{hour:02}:00" for hour in range(0, 24, 3)]

    def rowCount(self, parent=QModelIndex()):
        return len(self.forecast_data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        column = index.column()

        if role == Qt.DisplayRole:
            day = self.forecast_data[row]
            if column == 0:
                return day["date"]
            else:
                hour_index = column - 1
                if hour_index < len(day["hours"]):
                    hour_data = day["hours"][hour_index]
                    return hour_data
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]
            else:
                return str(section + 1)


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        # Получение города и установка в метку
        city, lat, lon = WeatherControl.get_location()
        self.ui.label_w1.setText(city)

        # Скрыть заголовки для таблицы
        self.ui.tableView_w.horizontalHeader().setVisible(False)
        self.ui.tableView_w.verticalHeader().setVisible(False)

        # Сделать TableView прозрачным и убрать рамки
        self.ui.tableView_w.setStyleSheet("""
            QTableView {
                background-color: transparent;

            }
            QTableView::item {
                border: none;
                padding: 2px;
            }
        """)

        weather_data = WeatherControl.get_weather_data(lat, lon)
        if weather_data:
            forecast = WeatherControl.parse_three_day_forecast(weather_data)
            self.populate_table(forecast)

    def populate_table(self, forecast):
        """Добавление данных прогноза в TableView."""
        model = WeatherTableModel(forecast)
        self.ui.tableView_w.setModel(model)
        self.ui.tableView_w.resizeColumnsToContents()
        self.ui.tableView_w.resizeRowsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
