import requests
from datetime import datetime
import csv
from collections import Counter
API_KEY=""
import os
def reset_file():
    if os.path.exists("weather_search_history.csv"):
        os.remove("weather_search_history.csv")
        print("🗑️ Old file deleted. A new one will be created automatically.")
def show_history():
    try:
        with open("weather_search_history.csv","r",encoding="utf-8") as f:
            reader=csv.reader(f)
            next(reader)
            print("\n📜 Weather Search History:")
            for row in reader:
                city, country, temp, description, humidity, wind_speed, time = row
                print(f"📍 {city}, {country} | 🌡 {temp}°C | 🌤 {description} | 💧 {humidity}% | 💨 {wind_speed} m/s | 🕒 {time}")
    except FileNotFoundError:
        print("⚠️ No history file found. Try searching for a city first.")
def function():
    sums = {}
    counts = {}

    with open("weather_search_history.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        data = list(reader)

    print(f"📂 Have {len(data)} saved entries")

    # Đếm số lần xuất hiện của thành phố
    city_list = [row[0].strip() for row in data]
    city_count = Counter(city_list)
    print("📊 Top thành phố được tìm nhiều nhất:", city_count.most_common(3))

    # Tính tổng nhiệt độ và số lần
    for row in data:
        try:
            temp = float(row[2])
        except ValueError:
            continue
        city = row[0].strip()
        if city not in sums:
            sums[city] = 0
            counts[city] = 0
        sums[city] += temp
        counts[city] += 1

    # Tính trung bình sau khi đã có sums & counts
    averages = {c: sums[c] / counts[c] for c in sums}

    print("\n📊 Nhiệt độ trung bình theo thành phố:")
    for c, avg in averages.items():
        print(f"  - {c}: {avg:.2f}°C ({counts[c]} bản ghi)")

    # Thời gian lần đầu & lần cuối
    times = [row[6] for row in data]
    print("⏰ Lần đầu tiên tra cứu:", min(times))
    print("⏰ Lần gần nhất tra cứu:", max(times))
def find_temperature():
    try:
        highest_temperature = float("-inf")
        lowest_temperature = float("inf")
        enter_city=input("type the city: ")
        with open("weather_search_history.csv","r",encoding="utf-8") as f:
            reader=csv.reader(f)
            next(reader)
            found= False
            for row in reader:
                city = row[0].strip().lower()
                temp=float(row[2])
                if city==enter_city:
                    found= True
                    if temp > highest_temperature:
                        highest_temperature = temp
                    if temp < lowest_temperature:
                        lowest_temperature = temp
        if found:
            print(f"🌡 Highest temperature in {enter_city.title()}: {highest_temperature}°C")
            print(f"🌡 Lowest temperature in {enter_city.title()}: {lowest_temperature}°C")
        else:
            print(f"⚠️ No records found for {enter_city.title()}")
        return highest_temperature
                
    except FileNotFoundError:
        print("⚠️ No history file found. Try searching for a city first.")
def show_weather(city):
    url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response=requests.get(url)
    data=response.json()
    if response.status_code == 200:
        temp = data["main"]["temp"] - 273.15
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        country = data["sys"]["country"]
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Hiển thị kết quả
        print(f"\n📍 {city}, {country}")
        print(f"🌡 Temp: {round(temp,1)}°C")
        print(f"🌤 Description: {description}")
        print(f"💧 Humidity: {humidity}%")
        print(f"💨 Wind Speed: {wind_speed} m/s")

        # Lưu vào CSV
        file_exists = os.path.isfile("weather_search_history.csv")
        with open("weather_search_history.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:   # chỉ ghi header nếu file chưa tồn tại
                writer.writerow(["City", "Country", "Temp(°C)", "Description", "Humidity", "Wind Speed", "Time"])
            writer.writerow([city, country, round(temp,1), description, humidity, wind_speed, time_now])
print("welcome to the weather app")
delete=input("Do you want to reset the old history file? (yes/no): ")
if delete.lower()=="yes":
    reset_file()
while True:
    city = input("Type the city (or 'exit' to quit, 'history' to view search history, 'trach' to show the highest/lowest of a city),'thanh' for another function: ")
    if city.lower() == "exit":
        print("Goodbye 👋")
        break
    elif city.lower() == "history":
        show_history()
    elif city.lower() == "trach":
        find_temperature()
    elif city.lower() == "thanh":
        function()
    else:
        show_weather(city)
