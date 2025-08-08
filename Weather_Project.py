import requests
#import pandas as pd
import datetime
import matplotlib.pyplot as plt
import csv
from collections import Counter
import os
from dotenv import load_dotenv
import logging
from logging.handlers import TimedRotatingFileHandler


#tải biến môi trường từ file .env
load_dotenv("OPEN_WEATHER_API_KEY.env.txt")

API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
city = input("Nhập tên thành phố (viết theo chuẩn quốc tế Vd: Hanoi , London , Tokyo ...) : ") #Viết theo chuẩn quốc tế
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
url1 = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
response = requests.get(url)
response1 = requests.get(url1)
file_path = "weather_project.csv" #Lưu kết quả vào file csv

#Tạo file log để lưu
os.makedirs("logs",exist_ok=True)
#Tạo logger
logger = logging.getLogger("WeatherLogger")
logger.setLevel(logging.INFO)

# Handler xoay file log mỗi ngày (hoặc mỗi giờ)
handler = TimedRotatingFileHandler(
    "logs/weather.log",
    when="midnight",      # "s"=giây, "m"=phút, "h"=giờ, "midnight"=0h mỗi ngày
    interval=1,           # Mỗi 1 đơn vị 'when' tạo file mới
    backupCount=7,        # Giữ 7 file log gần nhất
    encoding="utf-8"
)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


weather_translation = {
    "Clear": "Trời quang, nắng",
    "Clouds": "Có mây",
    "Rain": "Mưa",
    "Drizzle": "Mưa phùn",
    "Thunderstorm": "Dông",
    "Snow": "Tuyết",
    "Mist": "Sương mù nhẹ",
    "Smoke": "Khói",
    "Haze": "Sương khô",
    "Dust": "Bụi",
    "Fog": "Sương mù",
    "Sand": "Cát",
    "Ash": "Tro núi lửa",
    "Squall": "Gió giật",
    "Tornado": "Lốc xoáy"
}
description_vi = {
    # Thunderstorm
    "thunderstorm with light rain": "Dông kèm mưa nhẹ",
    "thunderstorm with rain": "Dông kèm mưa",
    "thunderstorm with heavy rain": "Dông kèm mưa to",
    "light thunderstorm": "Dông nhẹ",
    "thunderstorm": "Dông",
    "heavy thunderstorm": "Dông lớn",
    "ragged thunderstorm": "Dông không đều",
    "thunderstorm with light drizzle": "Dông kèm mưa phùn nhẹ",
    "thunderstorm with drizzle": "Dông kèm mưa phùn",
    "thunderstorm with heavy drizzle": "Dông kèm mưa phùn to",

    # Drizzle
    "light intensity drizzle": "Mưa phùn nhẹ",
    "drizzle": "Mưa phùn",
    "heavy intensity drizzle": "Mưa phùn to",
    "light intensity drizzle rain": "Mưa phùn pha mưa nhẹ",
    "drizzle rain": "Mưa phùn pha mưa",
    "heavy intensity drizzle rain": "Mưa phùn pha mưa to",
    "shower rain and drizzle": "Mưa rào và mưa phùn",
    "heavy shower rain and drizzle": "Mưa rào to và mưa phùn",
    "shower drizzle": "Mưa phùn từng cơn",

    # Rain
    "light rain": "Mưa nhẹ",
    "moderate rain": "Mưa vừa",
    "heavy intensity rain": "Mưa to",
    "very heavy rain": "Mưa rất to",
    "extreme rain": "Mưa cực to",
    "freezing rain": "Mưa đóng băng",
    "light intensity shower rain": "Mưa rào nhẹ",
    "shower rain": "Mưa rào",
    "heavy intensity shower rain": "Mưa rào to",
    "ragged shower rain": "Mưa rào không đều",

    # Snow
    "light snow": "Tuyết nhẹ",
    "snow": "Tuyết",
    "heavy snow": "Tuyết to",
    "sleet": "Mưa tuyết pha",
    "light shower sleet": "Mưa tuyết pha nhẹ",
    "shower sleet": "Mưa tuyết pha",
    "light rain and snow": "Tuyết pha mưa nhẹ",
    "rain and snow": "Tuyết pha mưa",
    "light shower snow": "Tuyết rơi nhẹ",
    "shower snow": "Tuyết rơi",
    "heavy shower snow": "Tuyết rơi to",

    # Atmosphere
    "mist": "Sương mù nhẹ",
    "smoke": "Khói",
    "haze": "Sương khô",
    "sand/dust whirls": "Lốc bụi",
    "fog": "Sương mù",
    "sand": "Cát",
    "dust": "Bụi",
    "volcanic ash": "Tro núi lửa",
    "squalls": "Gió giật",
    "tornado": "Lốc xoáy",

    # Clear
    "clear sky": "Trời quang, nắng",

    # Clouds
    "few clouds": "Mây thưa",
    "scattered clouds": "Mây rải rác",
    "broken clouds": "Mây từng đám",
    "overcast clouds": "Mây u ám, phủ kín"
}
#kiểm tra trạng thái đường link
if response.status_code == 200 and response1.status_code == 200 :
    weather_data = response.json()
    forecast = response1.json()
    weather_forecast_data = forecast["list"]
    logger.info("Bắt đầu chương trình Weather Project")
    logger.info(f"Đang gọi API thời tiết cho thành phố {city}")
    #xác định vị trí xem xét thời tiết
    location_name = weather_data.get("name","")
    coord_lon = weather_data.get("coord",{}).get("lon",0)
    coord_lat = weather_data.get("coord",{}).get("lat",0)
    print(f"Thành phố hiện tại : {location_name} , có vị trí tọa độ với kinh độ : {coord_lon} và vĩ độ : {coord_lat}")


    #chuyển đổi sang giờ địa phương
    dt_txt = weather_data.get("dt", 0)
    dt_object_local = datetime.datetime.fromtimestamp(dt_txt)
    print(f"⏰Thời gian dự báo tại thời điểm này : {dt_object_local}")


    #trích xuất nhiệt độ
    temp_now = weather_data.get("main",{}).get("temp",0)
    temp_min = weather_data.get("main",{}).get("temp_min",0)
    temp_max = weather_data.get("main",{}).get("temp_max",0)
    feel_temp = weather_data.get("main",{}).get("feels_like",0)
    print(f"Nhiệt độ tại thời điểm hiện tại : {temp_now}")
    print(f"Nhiệt độ thấp nhất trong ngày : {temp_min}")
    print(f"Nhiệt độ cao nhất trong ngày : {temp_max}")
    print(f"Nhiệt độ tại thời điểm mà cơ thể cảm nhận được {feel_temp}")


    #phân tích độ ẩm và so sánh độ ẩm tại thời điểm 3 giờ trước
    humidity_now = weather_data.get("main",{}).get("humidity",0)
    print(f"Độ ẩm tại thời điểm hiện tại : {humidity_now}")

    #so sánh độ ẩm giữa thời điểm hiện tại và 3 tiếng trước
    current = weather_forecast_data[0] #thời điểm gần nhất
    previous = weather_forecast_data[1] #thời điểm 3 tiếng trước
    #trích xuất độ ẩm và thời gian  
    current_time = current["dt_txt"]
    current_humidity = current.get("main",{}).get("humidity",0)
    previous_time = previous["dt_txt"]
    previous_humidity = previous.get("main",{}).get("humidity",0)

    diff = current_humidity - previous_humidity
    print(f"Độ ẩm tại thời điểm {current_time} : {current_humidity}")
    print(f"Độ ẩm tại thời điểm {previous_time} : {previous_humidity}")
    if diff > 0:
        print(f"Độ ẩm hiện tại đang tăng {abs(diff)}%")
    else :
        print(f"Độ ẩm hiện tại đang giảm {abs(diff)}% ")


    #Mô tả thời tiết

    weather_id = weather_data.get("weather",[])[0].get("id",0)
    print(f"ID : {weather_id}")
    weather_m = weather_data["weather"][0]["main"]
    weather_main = weather_translation.get(weather_m,"")
    print(f"Thời tiết hiện tại : {weather_main}")
    weather_d = weather_data.get("weather",[])[0].get("description","")
    weather_desc = description_vi.get(weather_d,"")
    print(f"Mô tả chi tiết thời tiết hiện tại : {weather_desc}")
    weather_icon = weather_data.get("weather",[])[0].get("icon","")
    url_image= f"http://openweathermap.org/img/wn/{weather_icon}@2x.png"
    print(f"Đường link xem hình ảnh mô tả {url_image} ")
    # Mức độ mây
    weather_cloud = weather_data.get("clouds",{}).get("all",0)
    print(f"Mức độ mây : {weather_cloud} %")

    #Hướng gió
    def classify_wind_speed(wind_speed) :
        if wind_speed < 0.3 :
            return "Lặng gió"
        elif wind_speed < 1.6 :
            return "Gió rất nhẹ"
        elif wind_speed <3.4 :
            return "Gió nhẹ"
        elif wind_speed < 5.5 :
            return "Gió nhẹ vừa"
        elif wind_speed <8.0 :
            return "Gió vừa"
        elif wind_speed < 10.8 :
            return "Gió mạnh vừa"
        else :
            return "Gió rất mạnh"
    #Tốc độ gió
    wind_speed = weather_data.get("wind",{}).get("speed",0)
    print(f"Tốc độ gió hiện tại : {wind_speed} m/s -{classify_wind_speed(wind_speed)}")
    #Hướng gió
    deg = weather_data.get("wind", {}).get("deg", 0)
    def wind_direction(deg):
        directions = [
            "Bắc", "Bắc Đông Bắc", "Đông Bắc", "Đông Đông Bắc",
            "Đông", "Đông Đông Nam", "Đông Nam", "Nam Đông Nam",
            "Nam", "Nam Tây Nam", "Tây Nam", "Tây Tây Nam",
            "Tây", "Tây Tây Bắc", "Tây Bắc", "Bắc Tây Bắc"
        ]
        idx = int((deg+11.25)% 360 /22.5)
        return directions[idx]
    print(f"Hướng gió {wind_direction(deg)}")

    dt_rise = weather_data.get("sys",{}).get("sunrise",0)
    dt_set = weather_data.get("sys",{}).get("sunset",0)
    sunrise_time = datetime.datetime.fromtimestamp(dt_rise).strftime('%H:%M:%S')
    sunset_time = datetime.datetime.fromtimestamp(dt_set).strftime('%H:%M:%S')
    print(f"🌅 Mặt trời mọc: {sunrise_time}")
    sunrise_set = datetime.datetime.fromtimestamp(dt_set).strftime('%H:%M:%S')
    print(f"🌇 Mặt trời lặn: {sunset_time}")


    #Vẽ biểu đồ nhiệt theo thời gian của các ngày sắp tới
    def plot_temperature():
        dt_times =[]
        temps =[]

        for items in weather_forecast_data :
            dt = datetime.datetime.fromtimestamp(items["dt"])
            temp = items.get("main",{}).get("temp")
            dt_times.append(dt)
            temps.append(temp)

        #Vẽ biểu đồ
        plt.figure(figsize=(10,5)) #tạo một khung hình
        plt.plot(dt_times,temps,marker = 'o',linestyle='-',color='tomato')

        #Tạo tiêu đề
        plt.title("Biểu đồ nhiệt theo thời gian ")
        plt.xlabel("THỜI GIAN")
        plt.ylabel("NHIỆT ĐỘ (°C)")
        plt.xticks(rotation =45)
        plt.grid(True) #hiển thị lưới
        plt.tight_layout()
        plt.show()


    #Vẽ biểu đồ độ ẩm theo thời gian
    def plot_humidities():
        humidities =[]
        dt_times =[]

        for items in weather_forecast_data :
            dt = datetime.datetime.fromtimestamp(items["dt"])
            humidity = items.get("main",{}).get("humidity",0)
            dt_times.append(dt)
            humidities.append(humidity)

        plt.figure(figsize =(10,5))
        plt.plot(dt_times,humidities,marker='o',linestyle='-',color='green')

        plt.title("Biểu đồ độ ẩm theo thời gian")
        plt.xlabel("THỜI GIAN")
        plt.ylabel("ĐỘ ẨM")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_wind():
        dt_times = []
        winds =[]

        for items in weather_forecast_data :
            dt = datetime.datetime.fromtimestamp(items["dt"])
            wind = items.get("wind",{}).get("speed",0)
            dt_times.append(dt)
            winds.append(wind)

        plt.figure(figsize = (10,5))
        colors = ['red' if v > 8 else 'skyblue' for v in winds]
        plt.bar(dt_times,winds,color=colors,width=0.6)

        plt.title("Biểu đồ cột tốc độ gió theo thời gian")
        plt.xlabel("THỜI GIAN")
        plt.ylabel("TỐC ĐỘ GIÓ")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_weather():
        weather_mains = []
        for items in weather_forecast_data :
            main = items.get("weather",[])[0].get("main","")
            weather_mains.append(main)

        counter = Counter(weather_mains) #Đếm số lần xuất hiện mỗi loại thời tiết

        #chuẩn bị dữ liệu
        labels = list(counter.keys())
        sizes = list(counter.values())
        colors = ['gold', 'lightblue', 'lightgray', 'lightgreen', 'violet', 'orange'][:len(labels)]

        plt.figure(figsize = (6,6))
        plt.pie(sizes,labels = labels ,colors = colors ,startangle =90,autopct='%1.1f%%')
        plt.title("Biểu đồ phân loại ")
        plt.axis('equal')
        plt.tight_layout()
        plt.show()


    def main():
        while True:
            print("\n=== MENU BIỂU ĐỒ ===")
            print("1. Biểu đồ nhiệt độ")
            print("2. Biểu đồ nhiệt độ cảm nhận")
            print("3. Biểu đồ độ ẩm")
            print("4. Biểu đồ tốc độ gió")
            print("0. Thoát")
            choice = int(input("Nhập lựa chọn của bạn (0-4): "))
            if choice == 1 :
                plot_temperature()
            elif choice == 2 :
                plot_humidities()
            elif choice == 3:
                plot_wind()
            elif choice == 4 :
                plot_weather()
            elif choice ==0 :
                print("Đã thoát")
                break
            else :
                print("❌ Chỉ nhập từ 0-4")

    main()
    #lưu trữ vào CSV

    #kiểm tra các dòng có bị trùng không

    file_exists = os.path.isfile(file_path)
    write_header = not file_exists or os.stat(file_path).st_size == 0
    row = [location_name,dt_object_local,temp_now,humidity_now,weather_id,weather_main,
                             weather_desc,weather_cloud,wind_speed, classify_wind_speed(wind_speed),wind_direction(deg),
                             sunrise_time,sunset_time]

    def check_for_duplicate_lines(row,filename="weather_project.csv"):
        if not os.path.exists(filename): #kiểm tra file có tồn tại không
            return False
        with open(filename ,mode='r',encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader,None) #bỏ qua phần tiêu đề
            change_row = [str(item) for item in row]
            for items in reader :
                if change_row == items :
                    return True
        return False # trả về giá trị False nêus không tím thấy bất kỳ hàng nào trùng khớp
    try :
        if not check_for_duplicate_lines(row,file_path):
            with open(file_path,mode="a",newline ="",encoding="utf-8") as file :
                writer = csv.writer(file)
                if write_header :
                    writer.writerow(["Thành phố","Thời gian","Nhiệt độ","Độ ẩm","ID","Thời tiết hiện tại","Mô tả","Mức độ mây","Tốc độ",
                                     "Mô tả gió","Hướng gió","Thời gian mặt trời mọc", "Thời gian mặt trời lăn"])
                writer.writerow(row)
            print("Đã ghi vào file thành công ")
        else :
            print("Kết quả đã trong file , Không ghi lại ")
    except Exception as e :
        print("Lỗi khi lưu csv ",e)

else :
    logger.error(f"Lỗi API: {response.status_code}")
    print(f"Nội dung lỗi : {response.text}")
