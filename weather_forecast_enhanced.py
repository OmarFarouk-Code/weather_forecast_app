import requests
import os
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv

# ------------------------------------------------------------------
# DOCUMENTATION & CONFIGURATION
# ------------------------------------------------------------------
# Purpose: A GUI-based Weather Application using OpenWeatherMap API.
# Features: Real-time weather data, unit conversion (Metric), 
#           error handling for invalid cities, and keyboard support.
# ------------------------------------------------------------------

load_dotenv()
API_KEY = os.getenv("OPEN_WEATHER_MAP_API_KEY")

def get_weather(event=None):

    city = Entry_Box.get().strip()

    #Check if entry is empty
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    # Visual feedback: Let the user know we are fetching data
    Temp_label.config(text="Fetching data...", fg="blue")
    
    API_CALL_URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(API_CALL_URL, timeout=5)
        data = response.json()

        # Handle API errors (e.g., City Not Found)
        if data.get("cod") != 200:
            error_msg = data.get("message", "City not found").capitalize()
            Temp_label.config(text=error_msg, fg="red")
            # Clear other labels if search fails
            for label in Label_List[1:]:
                label.config(text=label.cget("text").split(":")[0] + ": --")
        else:
            # Successfully retrieved data
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            windspeed = data['wind']['speed']
            # Get rain if available, otherwise default to 0
            precipitation = data.get('rain', {}).get('1h', 0)

            # Update GUI with bold colors for better readability
            Temp_label.config(text=f"Temperature: {temp}°C", fg="black")
            Humd_label.config(text=f"Humidity: {humidity}%", fg="black")
            Wind_label.config(text=f"Wind Speed: {windspeed} m/s", fg="black")
            Press_label.config(text=f"Pressure: {pressure} hPa", fg="black")
            Prec_label.config(text=f"Precipitation: {precipitation} mm", fg="black")
            

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Error", "Check your internet connection.")
        Temp_label.config(text="Connection Error", fg="red")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# ------------------------------------------------------------------
# GRAPHICAL USER INTERFACE (GUI)
# ------------------------------------------------------------------
window = tk.Tk()
window.title("Weather Forecast")
window.geometry("900x450")  # Set a default window size
window.configure(padx=20, pady=20 )



# Grid Configuration
for i in range(6):
    window.rowconfigure(i, weight=1)
for i in range(3):
    window.columnconfigure(i, weight=1)

# Input Section
Locat_label = tk.Label(window, text="Location:", font=("Arial", 12, "bold"))
Locat_label.grid(row=0, column=0, sticky="e", padx=5)

Entry_Box = tk.Entry(window, width=25, font=("Arial", 12))
Entry_Box.grid(row=0, column=1, padx=5)
Entry_Box.focus() # Auto-focus on entry box for better UX

btn_search = tk.Button(window, text="Search", command=get_weather, 
                       bg="#4a90e2", fg="white", font=("Arial", 10, "bold"), 
                       padx=10, cursor="hand2")
btn_search.grid(row=0, column=2, sticky="w", padx=5)

# Display Labels
Temp_label = tk.Label(window, text="Temperature: --", font=("Arial", 14))
Humd_label = tk.Label(window, text="Humidity: --", font=("Arial", 12))
Wind_label = tk.Label(window, text="Wind Speed: --", font=("Arial", 12))
Press_label = tk.Label(window, text="Pressure: --", font=("Arial", 12))
Prec_label = tk.Label(window, text="Precipitation: --", font=("Arial", 12))

Label_List = [Temp_label, Humd_label, Wind_label, Press_label, Prec_label]

# Grid the labels using a loop
for index, lbl in enumerate(Label_List):
    lbl.grid(row=index + 1, column=0, columnspan=3, pady=10)

# Bind "Enter" key for easier searching
window.bind("<Return>", get_weather)

window.mainloop()