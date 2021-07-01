from tkinter.constants import BOTH, BOTTOM, LEFT, X
import requests
from bs4 import BeautifulSoup
from tkinter import Button, Canvas, Entry, Frame, Listbox, PhotoImage, Scrollbar, Tk 
from tkinter import Label
from tkinter import ttk
from PIL import Image, ImageTk
import time 
import re

# root window
root = Tk()
root.title("Weather App")
root.iconphoto(False, PhotoImage(file="Images/weatherImage.png")) # weather image for the window
root.geometry("1400x750") # size of the window
root.config(bg = "white")

# Weather image class 
class WeatherImage():
    def getImage(self, condition):
        img_path = "E:\Visual Studio (Projects)\Python Projects\Images\\" 

        theConditions = ["Fair", "Sunny", "Mostly Sunny", "Cloudy", "Partly Cloudy", "Mostly Cloudy", "Showers"
                            "Few Showers", "Light Rain", "Rain", "Thunderstorms", "Isolated Thunderstorms", 
                            "Scattered Thunderstorms", "Snow", "Light Snow", "Snow Showers", "Clear", "Mostly Clear"]
        for c in theConditions:
            if c == condition:
                img_path += str(c) + ".png"
                break
    
        global img
        # open and resize the image 
        img = Image.open(img_path)
        img = img.resize((180,150))
        img = ImageTk.PhotoImage(img) # tkinter readable 
        return img
        
'''
    Today's weather : Frame 1 (current weather info) and Frame 2 (Additional weather info)
'''
class TodayWeather:
    
    # defalult constructor
    def __init__(self, zip_code):
        self.zipCode = zip_code
    
    # current time 
    def getTime(self):
        current_time = time.strftime("%I:%M %p")
        timeLabel.config(text=f"As of {current_time}", fg="#5C5C5C")
        timeLabel.after(1000, self.getTime)

    # method to obtain the current weather data for frame 1
    def getWeather(self):
        url_today_weather = "https://weather.com/weather/today/l/" + str(self.zipCode)
        page = requests.get(url_today_weather)
        soup = BeautifulSoup(page.content, "html.parser") # parse into html
        location = soup.find("h1", class_=re.compile("CurrentConditions--location")).text
        temperature = soup.find("span", class_=re.compile("CurrentConditions--tempValue")).text
        weatherCondition = soup.find("div", class_=re.compile("CurrentConditions--phraseValue")).text
        
        # show label on the root window 
        locationLabel.config(text=location)
        temperatureLabel.config(text=temperature + "F")
        weatherConditionLabel.config(text=weatherCondition)

        # set the image
        weather_img = WeatherImage.getImage(self,weatherCondition)
        imageLabel.config(image=weather_img, text='No Weather Image')
    
        # update temperature and weather condition after a minute
        temperatureLabel.after(120000, self.getWeather)

        #root.after(60000, self.getWeather)
        
        
    def getWeatherInfo(self):
        url_today_weather = "https://weather.com/weather/today/l/" + str(self.zipCode)
        page = requests.get(url_today_weather)
        soup = BeautifulSoup(page.content, "html.parser") # parse into html
        feels_temp = soup.find("span", class_=re.compile("TodayDetailsCard--feelsLikeTempValue")).text
        sunrise_sunset = soup.find_all("p", class_=re.compile("SunriseSunset--dateValue"))
        air_quality_index = soup.find("div", class_=re.compile("AirQuality--col")).text
        air_quality_text = soup.find("span", class_=re.compile("AirQualityText--severity")).text
        all_info = soup.find_all("div", class_=re.compile("WeatherDetailsListItem--wxData"))
    
        # show label on the screen
        feels_temp_label.config(text=feels_temp)
        feels_text_label.config(text="Feels Like")

        sunrise_sunset_label.config(text="Sunrise:  " + sunrise_sunset[0].text + "\n" + "Sunset:   " + sunrise_sunset[1].text)
        air_quality_label.config(text="%s \n%s %10s" %("Air Quality", air_quality_index, air_quality_text))

        high_low_label.config(text="\n"+ "%-17s %s"%("High / Low", all_info[0].text))
        wind_label.config(text="\n"+ "%-21s %s"%("Wind", all_info[1].text.replace("Wind Direction", "")))
        humidity_label.config(text="%-18s %s"%("Humidity", all_info[2].text))
        dew_point_label.config(text="%-18s %s"%("Dew Point", all_info[3].text))
        pressure_label.config(text="%-17s %s"%("Pressure", all_info[4].text.replace("Arrow Down", "").replace("Arrow Up", "")))
        uv_index_label.config(text="%-19s %s"%("UV Index", all_info[5].text))
        visibility_label.config(text="%-18s   %s"%("Visibility", all_info[6].text))
        moon_phase_label.config(text="%-16s %s"%("Moon Phase", all_info[7].text))

    # Frame 1 - displays the current weather
    def frame_1(self):
        global locationLabel, temperatureLabel, weatherConditionLabel, imageLabel, timeLabel
        frame1 = Frame(root, highlightbackground='#E48330', highlightthickness=3.5, bg="white")
        frame1.grid(row=1, column=0, padx=10, pady=10, ipadx=10, ipady=5)

        # location label
        locationLabel = Label(frame1, font=("Normal", 20, "bold"), bg="white")
        locationLabel.grid(row=0, padx=45, sticky="N")

        # temerature label
        temperatureLabel = Label(frame1, font=("Normal", 50), bg="white")
        temperatureLabel.grid(row=1, padx=20, sticky="W")

        # image label 
        imageLabel = Label(frame1, bg="white")
        imageLabel.grid(row=1, padx=10, sticky="E")

        # time label
        timeLabel = Label(frame1, font=("Normal", 15), bg = "white")
        timeLabel.grid(row=2, sticky="W", padx=20)

        # weather condition label
        weatherConditionLabel = Label(frame1, font=("Normal", 17), bg="white")
        weatherConditionLabel.grid(row=2, padx=(270,0), sticky="W")

        # get current weather 
        self.getWeather()
        self.getTime()
        
    # Frame 2 - additional weather info
    def frame_2(self):
        global headerLabel, feels_temp_label, feels_text_label, sunrise_sunset_label, air_quality_label
        global high_low_label, wind_label, humidity_label, dew_point_label, pressure_label, uv_index_label
        global visibility_label, moon_phase_label

        frame2 = Frame(root, highlightbackground='#BDB76B', highlightthickness=3.5, bg="white")
        frame2.grid(row=0, column=1, rowspan=2, padx=10, pady=10, ipadx=10, ipady=5)

        headerLabel = Label(frame2, text="Additional Weather info", font=("Normal", 20, "bold"), bg="white")
        headerLabel.grid(row=0, sticky="N")

        feels_temp_label = Label(frame2, font=("Normal", 50), bg="white")
        feels_temp_label.grid(row=1, padx=20, sticky="W")

        feels_text_label = Label(frame2, font=("Normal", 15), fg= "#5C5C5C", bg="white")
        feels_text_label.grid(row=2, padx=20, sticky="W")

        sunrise_sunset_label = Label(frame2, font=("Normal", 15), bg="white")
        sunrise_sunset_label.grid(row=1, padx=(350,10), sticky="W")

        inner_frame2 = Frame(frame2, highlightbackground='#BDB76B', highlightthickness=2, bg="white")
        inner_frame2.grid(row=2, padx=(350,10), sticky="W")
        air_quality_label = Label(inner_frame2, font=("Normal", 15, "bold"), bg="white")
        air_quality_label.grid(padx=10, sticky="W")

        high_low_label = Label(frame2, font=("Normal", 15), bg="white")
        high_low_label.grid(row=3, padx=20, sticky="W")

        wind_label = Label(frame2, font=("Normal", 15), bg="white")
        wind_label.grid(row=3, padx=(350,10), sticky="W")

        humidity_label = Label(frame2, font=("Normal", 15), bg="white")
        humidity_label.grid(row=4, padx=20, sticky="W")

        dew_point_label = Label(frame2, font=("Normal", 15), bg="white")
        dew_point_label.grid(row=4, padx=(350,10), sticky="W")

        pressure_label = Label(frame2, font=("Normal", 15), bg="white")
        pressure_label.grid(row=5, padx=20, sticky="W")
        
        uv_index_label = Label(frame2, font=("Normal", 15), bg="white")
        uv_index_label.grid(row=5, padx=(350,10), sticky="W")

        visibility_label = Label(frame2, font=("Normal", 15), bg="white")
        visibility_label.grid(row=6, padx=20, sticky="W")
    
        moon_phase_label = Label(frame2, font=("Normal", 15), bg="white")
        moon_phase_label.grid(row=6, padx=(350,10), sticky="W")

        # get additional weather info
        self.getWeatherInfo()

'''
    Hourly Weather Info
'''
class HourlyWeather:
    
    # defalult constructor
    def __init__(self, zip_code):
        self.zipCode = zip_code
        url_hourly_weather = "https://weather.com/weather/hourbyhour/l/" + str(self.zipCode)
        page = requests.get(url_hourly_weather)
        self.soup = BeautifulSoup(page.content, "html.parser") # parse into html

    def image(self, condition):
        global _img, the_img
        _img = Image.open("E:\Visual Studio (Projects)\Python Projects\Images\\" + str(condition) + ".png")
        _img = _img.resize((70,50))
        the_img = ImageTk.PhotoImage(_img)
        return the_img

    # current time 
    def getTime(self):
        current_time = time.strftime("%I:%M %p")
        time_label2.config(text=f"As of {current_time}", fg="#5C5C5C")
        time_label2.after(1000, self.getTime)

    def hourlyForecast(self, time_label, img_label, temp_label):
        hourly_weather = self.soup.find_all("div", class_=re.compile("DetailsSummary--DetailsSummary"))
        temp_value = self.soup.find_all("span", class_=re.compile("DetailsSummary--tempValue"))
        weather_condition = self.soup.find_all("span", class_=re.compile("DetailsSummary--extendedData"))
        
        hour = []
        temp = []
        condition = []
       
        for h in hourly_weather: 
            hour.append(h.h2.text) 

        for t in temp_value:
            temp.append(t.text)
        
        for w in weather_condition:
            condition.append(w.text)
        
  
        # show label on the frame
        for i in range(48):
            time_label[i].config(text=hour[i])

            #theImage = self.image(condition[i])
            #img_label[i].config(image=the_img, text='No Weather Image')
            if len(condition[i].split()) == 2:
                img_label[i].config(text=condition[i].split()[0] + "\n" + condition[i].split()[1])
            else:
                img_label[i].config(text=condition[i])
                
            temp_label[i].config(text=temp[i])

        
        # update temperature and weather condition after a minute
        #forecast_label.after(60000, self.hourlyForecast)
        
    # Hourly forecast
    def frame_3(self):
        global time_label2

        # frames for hourly weather 
        frame3 = Frame(root, highlightbackground="#D4AC0D", highlightthickness=3.5, bg="white")
        frame3.grid(row=2, column=0, padx=10, pady=10, ipadx=10, ipady=5)

        inner_frame1 = Frame(frame3, bg="white")
        inner_frame1.grid(row=0, padx=5, pady=(0,15), sticky="W")

        inner_frame2 = Frame(frame3)
        inner_frame2.grid(row=1, sticky="W")

        # add scroll bar        
        c = Canvas(inner_frame2, width=650, height=120, bg="red") ## ~~ ADJUST width AND height ~~ ##
        c.pack(fill="both", expand="yes")
        scroll_bar = ttk.Scrollbar(inner_frame2, orient="horizontal", command=c.xview)
        scroll_bar.pack(side=BOTTOM, fill=X, expand=1)
        c.configure(xscrollcommand=scroll_bar.set)
        c.bind('<Configure>', lambda e: c.configure(scrollregion = c.bbox('all')))
        
        # inner label frame
        label_frame = Frame(c, bg="white")
        c.create_window((0,0), window=label_frame, anchor="w")

        headerLabel = Label(inner_frame1, text="Hourly Weather:-", font=("Normal", 20, "bold"), bg="white")
        headerLabel.grid(row=0, padx= 20, sticky="N")

        time_label2 = Label(inner_frame1, font=("Normal", 15), bg = "white")
        time_label2.grid(row=1, padx=20, sticky="W")

        forecast_time = []
        forecast_condition = []
        forecast_temp = []
        for i in range(48):
            forecast_label1 = Label(label_frame, font=("Normal", 15), bg = "white")
            forecast_label1.grid(row=0, column=i, padx=10)
            forecast_label2 = Label(label_frame, font=("Normal", 12), bg = "white")
            forecast_label2.grid(row=1, column=i, padx=10, pady= 10)
            forecast_label3 = Label(label_frame, font=("Normal", 15, "bold"), bg = "white")
            forecast_label3.grid(row=2, column=i, padx=10)

            forecast_time.append(forecast_label1)
            forecast_condition.append(forecast_label2)
            forecast_temp.append(forecast_label3)

        self.hourlyForecast(forecast_time, forecast_condition, forecast_temp)
        self.getTime()

'''
    Daily Weather Info
'''
class DailyWeather():

    

    # defalult constructor
    def __init__(self, zip_code):
        self.zipCode = zip_code
        url_daily_weather = "https://weather.com/weather/tenday/l/" + str(self.zipCode)
        page = requests.get(url_daily_weather)
        self.soup = BeautifulSoup(page.content, "html.parser") # parse into html
        
    # current time 
    def getTime(self):
        current_time = time.strftime("%I:%M %p")
        time_label3.config(text=f"As of {current_time}", fg="#5C5C5C")
        time_label3.after(1000, self.getTime)

    def dailyForecast(self, theDay, theCondition, theTemperature):
        day_value = self.soup.find_all("h2", class_=re.compile("DetailsSummary--daypartName"))
        temp_value = self.soup.find_all("div", class_=re.compile("DetailsSummary--temperature"))
        weather_condition = self.soup.find_all("span", class_=re.compile("DetailsSummary--extendedData"))

        day = [] 
        condition = []
        temperature = []
       
        for d in day_value: 
            day.append(d.text) 
        for w in weather_condition:
            condition.append(w.text)
        for t in temp_value:
            temperature.append(t.text)

        # show label on the frame
        for i in range(0,len(temperature)):
            theDay[i].config(text=day[i]) 
            if len(condition[i].split()) == 2:
                theCondition[i].config(text=condition[i].split()[0] + "\n" + condition[i].split()[1])
            else:
                theCondition[i].config(text=condition[i])
            theTemperature[i].config(text=temperature[i])

    def frame4(self):
        global time_label3

        frame4 = Frame(root, highlightbackground="#7391B7", highlightthickness=3.5, bg="white")
        frame4.grid(row=2, column=1, padx=10, pady=10, ipadx=10, ipady=5)

        inner_frame1 = Frame(frame4, bg="white")
        inner_frame1.grid(row=0, padx=5, pady=(0,15), sticky="W")

        inner_frame2 = Frame(frame4)
        inner_frame2.grid(row=1, sticky="W")

        # add scroll bar        
        c = Canvas(inner_frame2, width=650, height=120, bg="red") ## ~~ ADJUST width AND height ~~ ##
        c.pack(fill="both", expand="yes")
        scroll_bar = ttk.Scrollbar(inner_frame2, orient="horizontal", command=c.xview)
        scroll_bar.pack(side=BOTTOM, fill=X, expand=1)
        c.configure(xscrollcommand=scroll_bar.set)
        c.bind('<Configure>', lambda e: c.configure(scrollregion = c.bbox('all')))
        
        # inner label frame
        label_frame = Frame(c, bg="white")
        c.create_window((0,0), window=label_frame, anchor="w")

        headerLabel = Label(inner_frame1, text="Daily Weather:-", font=("Normal", 20, "bold"), bg="white")
        headerLabel.grid(row=0, padx= 20, sticky="N")

        time_label3 = Label(inner_frame1, font=("Normal", 15), bg = "white")
        time_label3.grid(row=1, padx=20, sticky="W")

        
        _day = []
        _conditions = []
        _temperature = [] 
        for i in range(0,15):
            _label1 = Label(label_frame, font=("Normal", 15), bg = "white")
            _label1.grid(row=0, column=i, padx=10)
            _label2 = Label(label_frame, font=("Normal", 12), bg = "white")
            _label2.grid(row=1, column=i, padx=10, pady=10)
            _label3 = Label(label_frame, font=("Normal", 15, "bold"), bg = "white")
            _label3.grid(row=2, column=i, padx=10)

            _day.append(_label1)
            _conditions.append(_label2)
            _temperature.append(_label3)

        self.dailyForecast(_day, _conditions, _temperature)
        self.getTime()

class FindLocation():
    
    def enter(self, event=None):
        zip_code = entry_box.get()
        entry_box.delete(0,"end")  
        
        # display today's (current) weather 
        today_weather = TodayWeather(zip_code)
        today_weather.frame_1()
        today_weather.frame_2()

        # display hourly weather
        hourly = HourlyWeather(zip_code) 
        hourly.frame_3()

        # display daily weather
        daily = DailyWeather(zip_code)
        daily.frame4()

    def location_frame(self):
        locationFrame = Frame(root, highlightbackground="#806F91", highlightthickness=3.5, bg="#112843")
        locationFrame.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=5)

        global entry_box
        text_entry = Label(locationFrame, text="Search by zip code:", font=("Normal", 20, "bold"), bg="#112843", fg="white")
        text_entry.grid(row=0, padx=(20,0), pady=(5,0), sticky="W")

        entry_box = Entry(locationFrame, width=12, borderwidth=5, font=("Normal", 17, "bold"))
        entry_box.bind("<Return>", self.enter)
        entry_box.grid(row=0, column=1, padx=5, pady=5)

        button = Button(locationFrame, text="Enter", command=self.enter)
        button.grid(row=1, column=1, padx=10)


def main():
    zipCode = 92833 # default city - Fullerton, CA
   
    # display today's (current) weather 
    today_weather = TodayWeather(zipCode)
    today_weather.frame_1()
    today_weather.frame_2()

    # display hourly weather
    hourly = HourlyWeather(zipCode) 
    hourly.frame_3()

    # display daily weather
    daily = DailyWeather(zipCode)
    daily.frame4()

    # search the weather location
    city = FindLocation()
    city.location_frame()

    root.mainloop()

if __name__=="__main__":
    main()


