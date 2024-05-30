
# mydash.plotly.datamining
Đây là website trực quan hóa dữ liệu nhiệt độ của Việt Nam giai đoạn 2013-2024. Sử dụng ngôn ngữ Python và các thư viện liên quan như Pandas, json, Dash Plotly, request, datetime.


## Authors

ngoctrung.data@gmail.com


# Các bước thực hiện
## 1. Lấy dữ liệu:
Để lấy được dữ liệu nhiệt độ từ 2013 đến nay thì hiện tại trên mạng có rất nhiều nguồn. Thế nhưng đa phần đều charge chúng ta một khoản vì dữ liệu dạng historical được khai thác và lưu trữ rất tốn kém. Đây là diều dễ hiểu.
Nhưng năm 2023 mình đã tìm được open data từ một trang web nhưng nó chỉ cung cấp dữ liệu từ 2013 đến 2022 (khoảng 10 năm) và không update nữa. Do đó chúng ta cần phải tìm phần bị thiếu là tháng 9/2022 đến nay. 
Mình có đăng ký API Free của Openweather để lấy dữ liệu nhưng nó chỉ cho ra dữ liệu của một thời gian cụ thể như trong hình

![Screenshot from 2024-05-30 21-16-18](https://github.com/trungcoding/mydash.plotly.datamining/assets/85286015/fc5b3fe7-edd7-40b1-b737-0b846eb35761)

Như đã thấy thì dữ liệu lấy ra chỉ là trong 1 mốc thời gian cố định trong ngày và chỉ có temperature mình đoán trong vòng 2 tiếng đồng hồ khi mình truy xuất. Như vậy là data truy xuất được chưa đủ quality và quantity. Hiện tại OpenWeather cũng cho đăng ký free gói OneCall API. Gói này nâng cấp hơn gói Free mặc định là dữ liệu được trải dài suốt ngày và khi mình truy xuất được, nó cho ra dữ liệu của 12 lần truy xuất trong ngày (tức là cứ 2 tiếng 1 lần update dữ liệu).

![Screenshot from 2024-05-30 16-51-05](https://github.com/trungcoding/mydash.plotly.datamining/assets/85286015/6b222715-d3bd-4a45-a803-37a1e5b58fcb)

Bây giờ dataset của ta đã rực rỡ hơn. Tiếp theo ta phải phân tích trong json có những mục nào. Đây là toàn bộ Field có trong gói API của OpenWeather:
>lat Latitude of the location, decimal (−90; 90)
>timezone Timezone name for the requested location
>timezone_offset Shift in seconds from UTC
>current Current weather data API response
>current.dt Current time, Unix, UTC
>current.sunrise Sunrise time, Unix, UTC. For polar areas in midnight sun and polar night periods this parameter is not returned in the response
current.sunset Sunset time, Unix, UTC. For polar areas in midnight sun and polar night periods this parameter is not returned in the response
current.temp Temperature. Units - default: kelvin, metric: Celsius, imperial: Fahrenheit. How to change units used
current.feels_like Temperature. This temperature parameter accounts for the human perception of weather. Units – default: kelvin, metric: Celsius, imperial: Fahrenheit.
current.pressure Atmospheric pressure on the sea level, hPa
current.humidity Humidity, %
current.dew_point Atmospheric temperature (varying according to pressure and humidity) below which water droplets begin to condense and dew can form. Units – default: kelvin, metric: Celsius, imperial: Fahrenheit.
current.clouds Cloudiness, %
current.uvi Current UV index
current.visibility Average visibility, metres. The maximum value of the visibility is 10km
current.wind_speed Wind speed. Wind speed. Units – default: metre/sec, metric: metre/sec, imperial: miles/hour. How to change units used
current.wind_gust (where available) Wind gust. Units – default: metre/sec, metric: metre/sec, imperial: miles/hour. How to change units used
current.wind_deg Wind direction, degrees (meteorological)
current.rain
current.rain.1h (where available) Precipitation, mm/h. Please note that only mm/h as units of measurement are available for this parameter
current.snow
current.snow.1h (where available) Precipitation, mm/h. Please note that only mm/h as units of measurement are available for this parameter
current.weather
current.weather.id Weather condition id
current.weather.main Group of weather parameters (Rain, Snow, Clouds etc.)
current.weather.description Weather condition within the group (full list of weather conditions). Get the output in your language
current.weather.icon Weather icon id. How to get icons
minutely Minute forecast weather data API response
minutely.dt Time of the forecasted data, unix, UTC
minutely.precipitation Precipitation, mm/h. Please note that only mm/h as units of measurement are available for this parameter
hourly Hourly forecast weather data API response
hourly.dt Time of the forecasted data, Unix, UTC
hourly.temp Temperature. Units – default: kelvin, metric: Celsius, imperial: Fahrenheit. How to change units used
hourly.feels_like Temperature. This accounts for the human perception of weather. Units – default: kelvin, metric: Celsius, imperial: Fahrenheit.
hourly.pressure Atmospheric pressure on the sea level, hPa
hourly.humidity Humidity, %
hourly.dew_point Atmospheric temperature (varying according to pressure and humidity) below which water droplets begin to condense and dew can form. Units – default: kelvin, metric: Celsius, imperial: Fahrenheit.
hourly.uvi UV index
hourly.clouds Cloudiness, %
hourly.visibility Average visibility, metres. The maximum value of the visibility is 10km
hourly.wind_speed Wind speed. Units – default: metre/sec, metric: metre/sec, imperial: miles/hour.How to change units used
hourly.wind_gust (where available) Wind gust. Units – default: metre/sec, metric: metre/sec, imperial: miles/hour. How to change units used
hourly.wind_deg Wind direction, degrees (meteorological)
hourly.pop Probability of precipitation. The values of the parameter vary between 0 and 1, where 0 is equal to 0%, 1 is equal to 100%
hourly.rain
hourly.rain.1h (where available) Precipitation, mm/h. Please note that only mm/h as units of measurement are available for this parameter
hourly.snow
hourly.snow.1h (where available) Precipitation, mm/h. Please note that only mm/h as units of measurement are available for this parameter
hourly.weather
hourly.weather.id Weather condition id
hourly.weather.main Group of weather parameters (Rain, Snow, Clouds etc.)
hourly.weather.description Weather condition within the group (full list of weather conditions). Get the output in your language
hourly.weather.icon Weather icon id. How to get icons
daily Daily forecast weather data API response
daily.dt Time of the forecasted data, Unix, UTC
daily.sunrise Sunrise time, Unix, UTC. For polar areas in midnight sun and polar night periods this parameter is not returned in the response
daily.sunset Sunset time, Unix, UTC. For polar areas in midnight sun and polar night periods this parameter is not returned in the response
daily.moonrise The time of when the moon rises for this day, Unix, UTC
daily.moonset The time of when the moon sets for this day, Unix, UTC
daily.moon_phase Moon phase. and are 'new moon', is 'first quarter moon', is 'full moon' and is 'last quarter moon'. The periods in between are called 'waxing crescent', 'waxing gibbous', 'waning gibbous', and 'waning crescent', respectively. Moon phase calculation algorithm: if the moon phase values between the start of the day and the end of the day have a round value (0, 0.25, 0.5, 0.75, 1.0), then this round value is taken, otherwise the average of moon phases for the start of the day and the end of the day is taken. 010.250.50.75
summaryHuman-readable description of the weather conditions for the day
daily.temp Units – default: kelvin, metric: Celsius, imperial: Fahrenheit. How to change units used
daily.temp.morn Morning temperature.
daily.temp.day Day temperature.
daily.temp.eve Evening temperature.
daily.temp.night Night temperature.
daily.temp.min Min daily temperature.
daily.temp.max Max daily temperature.
daily.feels_like This accounts for the human perception of weather. Units – default: kelvin, metric: Celsius, imperial: Fahrenheit. How to change units used
daily.feels_like.morn Morning temperature.
daily.feels_like.day Day temperature.
daily.feels_like.eve Evening temperature.
daily.feels_like.night Night temperature.
daily.pressure Atmospheric pressure on the sea level, hPa
daily.humidity Humidity, %
daily.dew_point Atmospheric temperature (varying according to pressure and humidity) below which water droplets begin to condense and dew can form. Units – default: kelvin, metric: Celsius, imperial: Fahrenheit.
daily.wind_speed Wind speed. Units – default: metre/sec, metric: metre/sec, imperial: miles/hour. How to change units used
daily.wind_gust (where available) Wind gust. Units – default: metre/sec, metric: metre/sec, imperial: miles/hour. How to change units used
daily.wind_deg Wind direction, degrees (meteorological)
daily.clouds Cloudiness, %
daily.uvi The maximum value of UV index for the day
daily.pop Probability of precipitation. The values of the parameter vary between 0 and 1, where 0 is equal to 0%, 1 is equal to 100%
daily.rain (where available) Precipitation volume, mm. Please note that only mm as units of measurement are available for this parameter
daily.snow (where available) Snow volume, mm. Please note that only mm as units of measurement are available for this parameter
daily.weather
daily.weather.id Weather condition id
daily.weather.main Group of weather parameters (Rain, Snow, Clouds etc.)
daily.weather.description Weather condition within the group (full list of weather conditions). Get the output in your language
daily.weather.icon Weather icon id. How to get icons
alerts National weather alerts data from major national weather warning systems
alerts.sender_name Name of the alert source. Please read here the full list of alert sources
alerts.event Alert event name
alerts.start Date and time of the start of the alert, Unix, UTC
alerts.end Date and time of the end of the alert, Unix, UTC
alerts.description Description of the alert
alerts.tags Type of severe weather
