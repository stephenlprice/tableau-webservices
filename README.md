# Tableau Web Services

Proof of Concept for Tableau connectivity to Web Services via Table Extensions.

# API Calls

</br>

## Geo location

### Requests
```python
# Austin
http://api.openweathermap.org/geo/1.0/direct?q=austin,tx,840&appid=API_KEY
```

### Coordinates

```json
  "Austin": {
    "lon": -97.7436995,
    "lat": 30.2711286,
  },
  "Dallas": {
    "lon": -96.7969,
    "lat": 32.7763
  },
  "Houston": {
    "lon": -95.3677,
    "lat": 29.7589
  },
  "San Antonio": {
    "lon": -98.4936,
    "lat": 29.4241
  },
  "Denver": {
    "lon": -104.9847,
    "lat": 39.7392
  },
  "New Orleans": {
    "lon": -90.0701,
    "lat": 29.9499
  },
  "Tulsa": {
    "lon": -95.9929,
    "lat": 36.1557
  },
  "Oklahoma City": {
    "lon": -97.5171,
    "lat": 35.473
  },
  "Santa Fe": {
    "lon": -105.9506,
    "lat": 35.5167
  },
  "Albuquerque": {
    "lon": -106.6511,
    "lat": 35.0845
  },
  "Monterrey": {
    "lon": -100.3167,
    "lat": 25.6667
  },
  "Mexico City": {
    "lon": -99.1277,
    "lat": 19.4285
  },
  "Havana": {
    "lon": -82.383,
    "lat": 23.133
  }
```

### Sample Response
```json
{
  "name": "Austin",
  "local_names": {
  "be": "Остын",
  "eo": "Aŭstino",
  "de": "Austin",
  "he": "אוסטין",
  "ko": "오스틴",
  "te": "ఆస్టిన్",
  "ku": "Austin",
  "ur": "آسٹن",
  "en": "Austin",
  "ru": "Остин",
  "it": "Austin",
  "el": "Ώστιν",
  "fr": "Austin",
  "bn": "অস্টিন",
  "zh": "奥斯汀 / 柯士甸",
  "ja": "オースティン",
  "ta": "ஆஸ்டின்",
  "vi": "Austin",
  "fa": "آستین",
  "tr": "Austin",
  "es": "Austin",
  "ar": "أوستن",
  "uk": "Остін",
  "pt": "Austin",
  "pl": "Austin",
  "sr": "Остин",
  "hi": "ऑस्टिन",
  "gr": "Αὐγούστα"
  },
  "lat": 30.2711286,
  "lon": -97.7436995,
  "country": "US",
  "state": "Texas"
}
```
</br>

## Current Weather

### Requests
```python
# Austin
https://api.openweathermap.org/data/2.5/weather?lat=30.2711286&lon=-97.7436995&appid=API_KEY&units=imperial
```

### Sample Response
```json
{
  "coord": {
  "lon": -97.7437,
  "lat": 30.2711
  },
  "weather": [
  {
  "id": 804,
  "main": "Clouds",
  "description": "overcast clouds",
  "icon": "04n"
  }
  ],
  "base": "stations",
  "main": {
  "temp": 295.54,
  "feels_like": 296.24,
  "temp_min": 294.41,
  "temp_max": 296.51,
  "pressure": 1021,
  "humidity": 92
  },
  "visibility": 10000,
  "wind": {
  "speed": 2.68,
  "deg": 90,
  "gust": 4.47
  },
  "clouds": {
  "all": 100
  },
  "dt": 1667961627,
  "sys": {
  "type": 2,
  "id": 2073627,
  "country": "US",
  "sunrise": 1667911851,
  "sunset": 1667950720
  },
  "timezone": -21600,
  "id": 4671654,
  "name": "Austin",
  "cod": 200
}
```
</br>

## 5 Day Forecast

### Requests
```python
# Austin
https://api.openweathermap.org/data/2.5/forecast?lat=30.2711286&lon=-97.7436995&appid=API_KEY&units=imperial
```

### Sample Response
```json
{
"cod": "200",
"message": 0,
"cnt": 40,
"list": [
{
"dt": 1667973600,
"main": {
"temp": 294.96,
"feels_like": 295.57,
"temp_min": 293.95,
"temp_max": 294.96,
"pressure": 1021,
"sea_level": 1021,
"grnd_level": 1003,
"humidity": 91,
"temp_kf": 1.01
},
"weather": [
{
"id": 804,
"main": "Clouds",
"description": "overcast clouds",
"icon": "04n"
}
],
"clouds": {
"all": 100
},
"wind": {
"speed": 3.33,
"deg": 157,
"gust": 10.3
},
"visibility": 10000,
"pop": 0.11,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-09 06:00:00"
},
{
"dt": 1667984400,
"main": {
"temp": 293.89,
"feels_like": 294.47,
"temp_min": 293.1,
"temp_max": 293.89,
"pressure": 1021,
"sea_level": 1021,
"grnd_level": 1002,
"humidity": 94,
"temp_kf": 0.79
},
"weather": [
{
"id": 804,
"main": "Clouds",
"description": "overcast clouds",
"icon": "04n"
}
],
"clouds": {
"all": 95
},
"wind": {
"speed": 2.29,
"deg": 163,
"gust": 7.94
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-09 09:00:00"
},
{
"dt": 1667995200,
"main": {
"temp": 292.66,
"feels_like": 293.15,
"temp_min": 292.66,
"temp_max": 292.66,
"pressure": 1020,
"sea_level": 1020,
"grnd_level": 1002,
"humidity": 95,
"temp_kf": 0
},
"weather": [
{
"id": 804,
"main": "Clouds",
"description": "overcast clouds",
"icon": "04n"
}
],
"clouds": {
"all": 96
},
"wind": {
"speed": 1.86,
"deg": 137,
"gust": 6.02
},
"visibility": 5521,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-09 12:00:00"
},
{
"dt": 1668006000,
"main": {
"temp": 294.93,
"feels_like": 295.36,
"temp_min": 294.93,
"temp_max": 294.93,
"pressure": 1021,
"sea_level": 1021,
"grnd_level": 1003,
"humidity": 84,
"temp_kf": 0
},
"weather": [
{
"id": 804,
"main": "Clouds",
"description": "overcast clouds",
"icon": "04d"
}
],
"clouds": {
"all": 100
},
"wind": {
"speed": 3.34,
"deg": 145,
"gust": 6.99
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "d"
},
"dt_txt": "2022-11-09 15:00:00"
},
{
"dt": 1668016800,
"main": {
"temp": 299.94,
"feels_like": 300.66,
"temp_min": 299.94,
"temp_max": 299.94,
"pressure": 1020,
"sea_level": 1020,
"grnd_level": 1002,
"humidity": 55,
"temp_kf": 0
},
"weather": [
{
"id": 804,
"main": "Clouds",
"description": "overcast clouds",
"icon": "04d"
}
],
"clouds": {
"all": 99
},
"wind": {
"speed": 5.52,
"deg": 157,
"gust": 7.87
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "d"
},
"dt_txt": "2022-11-09 18:00:00"
},
{
"dt": 1668027600,
"main": {
"temp": 301.48,
"feels_like": 301.51,
"temp_min": 301.48,
"temp_max": 301.48,
"pressure": 1016,
"sea_level": 1016,
"grnd_level": 998,
"humidity": 45,
"temp_kf": 0
},
"weather": [
{
"id": 803,
"main": "Clouds",
"description": "broken clouds",
"icon": "04d"
}
],
"clouds": {
"all": 64
},
"wind": {
"speed": 5.72,
"deg": 158,
"gust": 7.66
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "d"
},
"dt_txt": "2022-11-09 21:00:00"
},
{
"dt": 1668038400,
"main": {
"temp": 297.96,
"feels_like": 298.01,
"temp_min": 297.96,
"temp_max": 297.96,
"pressure": 1016,
"sea_level": 1016,
"grnd_level": 998,
"humidity": 58,
"temp_kf": 0
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03n"
}
],
"clouds": {
"all": 44
},
"wind": {
"speed": 4.73,
"deg": 143,
"gust": 9.08
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-10 00:00:00"
},
{
"dt": 1668049200,
"main": {
"temp": 295.61,
"feels_like": 295.82,
"temp_min": 295.61,
"temp_max": 295.61,
"pressure": 1017,
"sea_level": 1017,
"grnd_level": 999,
"humidity": 73,
"temp_kf": 0
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03n"
}
],
"clouds": {
"all": 37
},
"wind": {
"speed": 4.95,
"deg": 155,
"gust": 11.2
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-10 03:00:00"
},
{
"dt": 1668060000,
"main": {
"temp": 293.77,
"feels_like": 294.08,
"temp_min": 293.77,
"temp_max": 293.77,
"pressure": 1017,
"sea_level": 1017,
"grnd_level": 998,
"humidity": 84,
"temp_kf": 0
},
"weather": [
{
"id": 803,
"main": "Clouds",
"description": "broken clouds",
"icon": "04n"
}
],
"clouds": {
"all": 54
},
"wind": {
"speed": 3.74,
"deg": 159,
"gust": 10.49
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-10 06:00:00"
},
{
"dt": 1668070800,
"main": {
"temp": 292.5,
"feels_like": 292.84,
"temp_min": 292.5,
"temp_max": 292.5,
"pressure": 1015,
"sea_level": 1015,
"grnd_level": 996,
"humidity": 90,
"temp_kf": 0
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01n"
}
],
"clouds": {
"all": 6
},
"wind": {
"speed": 3.22,
"deg": 160,
"gust": 10.14
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-10 09:00:00"
},
{
"dt": 1668081600,
"main": {
"temp": 292.39,
"feels_like": 292.88,
"temp_min": 292.39,
"temp_max": 292.39,
"pressure": 1014,
"sea_level": 1014,
"grnd_level": 995,
"humidity": 96,
"temp_kf": 0
},
"weather": [
{
"id": 801,
"main": "Clouds",
"description": "few clouds",
"icon": "02n"
}
],
"clouds": {
"all": 22
},
"wind": {
"speed": 2.9,
"deg": 145,
"gust": 9.45
},
"visibility": 3899,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-10 12:00:00"
},
{
"dt": 1668092400,
"main": {
"temp": 293.98,
"feels_like": 294.47,
"temp_min": 293.98,
"temp_max": 293.98,
"pressure": 1014,
"sea_level": 1014,
"grnd_level": 996,
"humidity": 90,
"temp_kf": 0
},
"weather": [
{
"id": 500,
"main": "Rain",
"description": "light rain",
"icon": "10d"
}
],
"clouds": {
"all": 95
},
"wind": {
"speed": 3.84,
"deg": 157,
"gust": 7.53
},
"visibility": 10000,
"pop": 0.2,
"rain": {
"3h": 0.11
},
"sys": {
"pod": "d"
},
"dt_txt": "2022-11-10 15:00:00"
},
{
"dt": 1668103200,
"main": {
"temp": 298.65,
"feels_like": 298.87,
"temp_min": 298.65,
"temp_max": 298.65,
"pressure": 1012,
"sea_level": 1012,
"grnd_level": 994,
"humidity": 62,
"temp_kf": 0
},
"weather": [
{
"id": 500,
"main": "Rain",
"description": "light rain",
"icon": "10d"
}
],
"clouds": {
"all": 94
},
"wind": {
"speed": 4.11,
"deg": 185,
"gust": 5.86
},
"visibility": 10000,
"pop": 0.2,
"rain": {
"3h": 0.19
},
"sys": {
"pod": "d"
},
"dt_txt": "2022-11-10 18:00:00"
},
{
"dt": 1668114000,
"main": {
"temp": 301.69,
"feels_like": 301.64,
"temp_min": 301.69,
"temp_max": 301.69,
"pressure": 1009,
"sea_level": 1009,
"grnd_level": 992,
"humidity": 44,
"temp_kf": 0
},
"weather": [
{
"id": 801,
"main": "Clouds",
"description": "few clouds",
"icon": "02d"
}
],
"clouds": {
"all": 19
},
"wind": {
"speed": 3.43,
"deg": 170,
"gust": 4.38
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "d"
},
"dt_txt": "2022-11-10 21:00:00"
},
{
"dt": 1668124800,
"main": {
"temp": 296.73,
"feels_like": 297.08,
"temp_min": 296.73,
"temp_max": 296.73,
"pressure": 1009,
"sea_level": 1009,
"grnd_level": 991,
"humidity": 74,
"temp_kf": 0
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03n"
}
],
"clouds": {
"all": 27
},
"wind": {
"speed": 4.02,
"deg": 129,
"gust": 7.55
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-11 00:00:00"
},
{
"dt": 1668135600,
"main": {
"temp": 295.83,
"feels_like": 296.27,
"temp_min": 295.83,
"temp_max": 295.83,
"pressure": 1010,
"sea_level": 1010,
"grnd_level": 992,
"humidity": 81,
"temp_kf": 0
},
"weather": [
{
"id": 803,
"main": "Clouds",
"description": "broken clouds",
"icon": "04n"
}
],
"clouds": {
"all": 66
},
"wind": {
"speed": 3.63,
"deg": 153,
"gust": 8.16
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-11 03:00:00"
},
{
"dt": 1668146400,
"main": {
"temp": 294.79,
"feels_like": 295.26,
"temp_min": 294.79,
"temp_max": 294.79,
"pressure": 1010,
"sea_level": 1010,
"grnd_level": 992,
"humidity": 86,
"temp_kf": 0
},
"weather": [
{
"id": 803,
"main": "Clouds",
"description": "broken clouds",
"icon": "04n"
}
],
"clouds": {
"all": 83
},
"wind": {
"speed": 3.53,
"deg": 185,
"gust": 7.53
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-11 06:00:00"
},
{
"dt": 1668157200,
"main": {
"temp": 294.6,
"feels_like": 295.1,
"temp_min": 294.6,
"temp_max": 294.6,
"pressure": 1009,
"sea_level": 1009,
"grnd_level": 991,
"humidity": 88,
"temp_kf": 0
},
"weather": [
{
"id": 804,
"main": "Clouds",
"description": "overcast clouds",
"icon": "04n"
}
],
"clouds": {
"all": 100
},
"wind": {
"speed": 3.79,
"deg": 182,
"gust": 8.08
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-11 09:00:00"
},
{
"dt": 1668168000,
"main": {
"temp": 293.99,
"feels_like": 294.53,
"temp_min": 293.99,
"temp_max": 293.99,
"pressure": 1009,
"sea_level": 1009,
"grnd_level": 990,
"humidity": 92,
"temp_kf": 0
},
"weather": [
{
"id": 804,
"main": "Clouds",
"description": "overcast clouds",
"icon": "04n"
}
],
"clouds": {
"all": 100
},
"wind": {
"speed": 4.05,
"deg": 186,
"gust": 8.83
},
"visibility": 10000,
"pop": 0.01,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-11 12:00:00"
},
{
"dt": 1668178800,
"main": {
"temp": 295.04,
"feels_like": 295.53,
"temp_min": 295.04,
"temp_max": 295.04,
"pressure": 1011,
"sea_level": 1011,
"grnd_level": 993,
"humidity": 86,
"temp_kf": 0
},
"weather": [
{
"id": 500,
"main": "Rain",
"description": "light rain",
"icon": "10d"
}
],
"clouds": {
"all": 100
},
"wind": {
"speed": 2.4,
"deg": 217,
"gust": 4.75
},
"visibility": 10000,
"pop": 0.53,
"rain": {
"3h": 0.53
},
"sys": {
"pod": "d"
},
"dt_txt": "2022-11-11 15:00:00"
},
{
"dt": 1668189600,
"main": {
"temp": 292.33,
"feels_like": 292.63,
"temp_min": 292.33,
"temp_max": 292.33,
"pressure": 1012,
"sea_level": 1012,
"grnd_level": 994,
"humidity": 89,
"temp_kf": 0
},
"weather": [
{
"id": 501,
"main": "Rain",
"description": "moderate rain",
"icon": "10d"
}
],
"clouds": {
"all": 100
},
"wind": {
"speed": 6.44,
"deg": 2,
"gust": 8.05
},
"visibility": 10000,
"pop": 1,
"rain": {
"3h": 4.78
},
"sys": {
"pod": "d"
},
"dt_txt": "2022-11-11 18:00:00"
},
{
"dt": 1668200400,
"main": {
"temp": 286.05,
"feels_like": 285.59,
"temp_min": 286.05,
"temp_max": 286.05,
"pressure": 1014,
"sea_level": 1014,
"grnd_level": 995,
"humidity": 84,
"temp_kf": 0
},
"weather": [
{
"id": 500,
"main": "Rain",
"description": "light rain",
"icon": "10d"
}
],
"clouds": {
"all": 100
},
"wind": {
"speed": 7.28,
"deg": 358,
"gust": 11.9
},
"visibility": 10000,
"pop": 0.88,
"rain": {
"3h": 0.81
},
"sys": {
"pod": "d"
},
"dt_txt": "2022-11-11 21:00:00"
},
{
"dt": 1668211200,
"main": {
"temp": 283.94,
"feels_like": 283.16,
"temp_min": 283.94,
"temp_max": 283.94,
"pressure": 1016,
"sea_level": 1016,
"grnd_level": 997,
"humidity": 80,
"temp_kf": 0
},
"weather": [
{
"id": 500,
"main": "Rain",
"description": "light rain",
"icon": "10n"
}
],
"clouds": {
"all": 100
},
"wind": {
"speed": 7.49,
"deg": 3,
"gust": 13.72
},
"visibility": 10000,
"pop": 0.92,
"rain": {
"3h": 0.73
},
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-12 00:00:00"
},
{
"dt": 1668222000,
"main": {
"temp": 283.69,
"feels_like": 282.5,
"temp_min": 283.69,
"temp_max": 283.69,
"pressure": 1019,
"sea_level": 1019,
"grnd_level": 1000,
"humidity": 65,
"temp_kf": 0
},
"weather": [
{
"id": 500,
"main": "Rain",
"description": "light rain",
"icon": "10n"
}
],
"clouds": {
"all": 71
},
"wind": {
"speed": 6.46,
"deg": 5,
"gust": 13.74
},
"visibility": 10000,
"pop": 0.71,
"rain": {
"3h": 0.65
},
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-12 03:00:00"
},
{
"dt": 1668232800,
"main": {
"temp": 283.22,
"feels_like": 281.64,
"temp_min": 283.22,
"temp_max": 283.22,
"pressure": 1020,
"sea_level": 1020,
"grnd_level": 1001,
"humidity": 52,
"temp_kf": 0
},
"weather": [
{
"id": 804,
"main": "Clouds",
"description": "overcast clouds",
"icon": "04n"
}
],
"clouds": {
"all": 85
},
"wind": {
"speed": 6.68,
"deg": 2,
"gust": 12.62
},
"visibility": 10000,
"pop": 0.59,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-12 06:00:00"
},
{
"dt": 1668243600,
"main": {
"temp": 281.29,
"feels_like": 277.81,
"temp_min": 281.29,
"temp_max": 281.29,
"pressure": 1021,
"sea_level": 1021,
"grnd_level": 1002,
"humidity": 48,
"temp_kf": 0
},
"weather": [
{
"id": 804,
"main": "Clouds",
"description": "overcast clouds",
"icon": "04n"
}
],
"clouds": {
"all": 100
},
"wind": {
"speed": 6.66,
"deg": 3,
"gust": 13.6
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-12 09:00:00"
},
{
"dt": 1668254400,
"main": {
"temp": 280.17,
"feels_like": 276.4,
"temp_min": 280.17,
"temp_max": 280.17,
"pressure": 1023,
"sea_level": 1023,
"grnd_level": 1004,
"humidity": 46,
"temp_kf": 0
},
"weather": [
{
"id": 804,
"main": "Clouds",
"description": "overcast clouds",
"icon": "04n"
}
],
"clouds": {
"all": 96
},
"wind": {
"speed": 6.58,
"deg": 1,
"gust": 13.59
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-12 12:00:00"
},
{
"dt": 1668265200,
"main": {
"temp": 281.38,
"feels_like": 277.67,
"temp_min": 281.38,
"temp_max": 281.38,
"pressure": 1025,
"sea_level": 1025,
"grnd_level": 1006,
"humidity": 39,
"temp_kf": 0
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03d"
}
],
"clouds": {
"all": 37
},
"wind": {
"speed": 7.47,
"deg": 10,
"gust": 12.33
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "d"
},
"dt_txt": "2022-11-12 15:00:00"
},
{
"dt": 1668276000,
"main": {
"temp": 285.61,
"feels_like": 283.72,
"temp_min": 285.61,
"temp_max": 285.61,
"pressure": 1025,
"sea_level": 1025,
"grnd_level": 1006,
"humidity": 31,
"temp_kf": 0
},
"weather": [
{
"id": 802,
"main": "Clouds",
"description": "scattered clouds",
"icon": "03d"
}
],
"clouds": {
"all": 28
},
"wind": {
"speed": 6.74,
"deg": 17,
"gust": 9.1
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "d"
},
"dt_txt": "2022-11-12 18:00:00"
},
{
"dt": 1668286800,
"main": {
"temp": 287.32,
"feels_like": 285.58,
"temp_min": 287.32,
"temp_max": 287.32,
"pressure": 1023,
"sea_level": 1023,
"grnd_level": 1004,
"humidity": 30,
"temp_kf": 0
},
"weather": [
{
"id": 801,
"main": "Clouds",
"description": "few clouds",
"icon": "02d"
}
],
"clouds": {
"all": 22
},
"wind": {
"speed": 6.24,
"deg": 15,
"gust": 7.89
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "d"
},
"dt_txt": "2022-11-12 21:00:00"
},
{
"dt": 1668297600,
"main": {
"temp": 284.46,
"feels_like": 282.59,
"temp_min": 284.46,
"temp_max": 284.46,
"pressure": 1025,
"sea_level": 1025,
"grnd_level": 1006,
"humidity": 36,
"temp_kf": 0
},
"weather": [
{
"id": 801,
"main": "Clouds",
"description": "few clouds",
"icon": "02n"
}
],
"clouds": {
"all": 12
},
"wind": {
"speed": 4.75,
"deg": 23,
"gust": 8.41
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-13 00:00:00"
},
{
"dt": 1668308400,
"main": {
"temp": 282.38,
"feels_like": 280.27,
"temp_min": 282.38,
"temp_max": 282.38,
"pressure": 1027,
"sea_level": 1027,
"grnd_level": 1008,
"humidity": 38,
"temp_kf": 0
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01n"
}
],
"clouds": {
"all": 8
},
"wind": {
"speed": 3.86,
"deg": 30,
"gust": 8.28
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-13 03:00:00"
},
{
"dt": 1668319200,
"main": {
"temp": 280.71,
"feels_like": 278.47,
"temp_min": 280.71,
"temp_max": 280.71,
"pressure": 1027,
"sea_level": 1027,
"grnd_level": 1007,
"humidity": 40,
"temp_kf": 0
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01n"
}
],
"clouds": {
"all": 5
},
"wind": {
"speed": 3.43,
"deg": 33,
"gust": 7.28
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-13 06:00:00"
},
{
"dt": 1668330000,
"main": {
"temp": 279.51,
"feels_like": 277.08,
"temp_min": 279.51,
"temp_max": 279.51,
"pressure": 1027,
"sea_level": 1027,
"grnd_level": 1008,
"humidity": 42,
"temp_kf": 0
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01n"
}
],
"clouds": {
"all": 4
},
"wind": {
"speed": 3.32,
"deg": 33,
"gust": 6.89
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-13 09:00:00"
},
{
"dt": 1668340800,
"main": {
"temp": 278.54,
"feels_like": 276.24,
"temp_min": 278.54,
"temp_max": 278.54,
"pressure": 1027,
"sea_level": 1027,
"grnd_level": 1008,
"humidity": 44,
"temp_kf": 0
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01n"
}
],
"clouds": {
"all": 2
},
"wind": {
"speed": 2.84,
"deg": 43,
"gust": 5.05
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "n"
},
"dt_txt": "2022-11-13 12:00:00"
},
{
"dt": 1668351600,
"main": {
"temp": 280.9,
"feels_like": 278.78,
"temp_min": 280.9,
"temp_max": 280.9,
"pressure": 1028,
"sea_level": 1028,
"grnd_level": 1009,
"humidity": 34,
"temp_kf": 0
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
],
"clouds": {
"all": 3
},
"wind": {
"speed": 3.28,
"deg": 65,
"gust": 5.23
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "d"
},
"dt_txt": "2022-11-13 15:00:00"
},
{
"dt": 1668362400,
"main": {
"temp": 286.19,
"feels_like": 284.2,
"temp_min": 286.19,
"temp_max": 286.19,
"pressure": 1026,
"sea_level": 1026,
"grnd_level": 1007,
"humidity": 25,
"temp_kf": 0
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
],
"clouds": {
"all": 5
},
"wind": {
"speed": 3.27,
"deg": 95,
"gust": 4.35
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "d"
},
"dt_txt": "2022-11-13 18:00:00"
},
{
"dt": 1668373200,
"main": {
"temp": 288.59,
"feels_like": 286.82,
"temp_min": 288.59,
"temp_max": 288.59,
"pressure": 1022,
"sea_level": 1022,
"grnd_level": 1003,
"humidity": 24,
"temp_kf": 0
},
"weather": [
{
"id": 800,
"main": "Clear",
"description": "clear sky",
"icon": "01d"
}
],
"clouds": {
"all": 7
},
"wind": {
"speed": 3.83,
"deg": 116,
"gust": 4.64
},
"visibility": 10000,
"pop": 0,
"sys": {
"pod": "d"
},
"dt_txt": "2022-11-13 21:00:00"
},
{
"dt": 1668384000,
"main": {
"temp": 285.82,
"feels_like": 284.08,
"temp_min": 285.82,
"temp_max": 285.82,
"pressure": 1021,
"sea_level": 1021,
"grnd_level": 1002,
"humidity": 36,
"temp_kf": 0
},
"weather": [
{
"id": 801,
"main": "Clouds",
"description": "few clouds",
"icon": "02n"
}
],
"clouds": {
"all": 21
},
"wind": {
  "speed": 3.3,
  "deg": 122,
  "gust": 5.43
},
"visibility": 10000,
"pop": 0,
"sys": {
  "pod": "n"
},
"dt_txt": "2022-11-14 00:00:00"
},
{
"dt": 1668394800,
"main": {
  "temp": 284.47,
  "feels_like": 282.68,
  "temp_min": 284.47,
  "temp_max": 284.47,
  "pressure": 1022,
  "sea_level": 1022,
  "grnd_level": 1003,
  "humidity": 39,
  "temp_kf": 0
},
"weather": [
  {
    "id": 804,
    "main": "Clouds",
    "description": "overcast clouds",
    "icon": "04n"
  }
],
"clouds": {
  "all": 98
},
"wind": {
  "speed": 2.81,
  "deg": 132,
  "gust": 6.22
},
"visibility": 10000,
"pop": 0,
"sys": {
  "pod": "n"
},
"dt_txt": "2022-11-14 03:00:00"
}
],
"city": {
  "id": 4671654,
  "name": "Austin",
  "coord": {
    "lat": 30.2711,
    "lon": -97.7437
  },
  "country": "US",
  "population": 790390,
  "timezone": -21600,
  "sunrise": 1667911851,
  "sunset": 1667950720
  }
}
```
