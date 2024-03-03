import tkinter as tk
from tkinter import ttk
import requests

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")

        self.location_label = ttk.Label(root, text="Enter Location:")
        self.location_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.location_entry = ttk.Entry(root, width=30)
        self.location_entry.grid(row=0, column=1, padx=5, pady=5)

        self.get_weather_button = ttk.Button(root, text="Get Weather", command=self.get_weather)
        self.get_weather_button.grid(row=0, column=2, padx=5, pady=5)

        self.weather_icon_label = ttk.Label(root, text="")
        self.weather_icon_label.grid(row=1, column=0, padx=5, pady=5)

        self.weather_info_label = ttk.Label(root, text="")
        self.weather_info_label.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)

        self.unit_label = ttk.Label(root, text="Select Unit:")
        self.unit_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.unit_var = tk.StringVar()
        self.unit_var.set("metric")  # Default to Celsius
        self.unit_dropdown = ttk.Combobox(root, textvariable=self.unit_var, values=["metric", "imperial"])
        self.unit_dropdown.grid(row=2, column=1, padx=5, pady=5)

        self.check_again_button = ttk.Button(root, text="Check Weather Again", command=self.reset)
        self.exit_button = ttk.Button(root, text="Exit", command=root.quit)

    def get_weather(self):
        location = self.location_entry.get()
        units = self.unit_var.get()
        api_key = "9fbde3685ad2ac19a2ba8828a2963b05"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units={units}"

        try:
            response = requests.get(url)
            data = response.json()

            city = data['name']
            country = data['sys']['country']
            temperature = data['main']['temp']
            weather_desc = data['weather'][0]['description']
            weather_icon = data['weather'][0]['icon']

            # Display weather icon
            icon_url = f"http://openweathermap.org/img/wn/{weather_icon}.png"
            icon_data = requests.get(icon_url, stream=True).content
            self.weather_icon = tk.PhotoImage(data=icon_data)
            self.weather_icon_label.config(image=self.weather_icon)

            # Display weather info
            weather_info = f"City: {city}, {country}\n"
            weather_info += f"Temperature: {temperature}°{'C' if units == 'metric' else 'F'}\n"
            weather_info += f"Weather: {weather_desc}"

            self.weather_info_label.config(text=weather_info)
            self.display_buttons()
        except Exception as e:
            self.weather_info_label.config(text="Error fetching weather data")

    def display_buttons(self):
        self.check_again_button.grid(row=3, column=0, padx=5, pady=5)
        self.exit_button.grid(row=3, column=1, padx=5, pady=5)

    def reset(self):
        self.weather_icon_label.config(image="")
        self.weather_info_label.config(text="")
        self.check_again_button.grid_forget()
        self.exit_button.grid_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()