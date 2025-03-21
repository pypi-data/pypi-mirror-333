from requests import get


class Wttr:
    def __init__(self):
        self.base_url = "https://wttr.in/"

    def get_weather(self, city="", state="", country="USA"):
        city = self.text_fixer(city)
        state = self.text_fixer(state)
        output_format = r"?format=Condition:+%C+\nPrecip:+%p/3 hours+\nTemps:+%t(%f)"
        url = f"{self.base_url}{city}+{state}+{country}{output_format}"
        weather = get(url, timeout=5)
        return weather.text

    def text_fixer(self, text=""):
        counter = 0
        text = list(text)
        for character in text:
            if text[counter] == " ":
                text[counter] = "+"
            counter += 1

        return "".join(text)

