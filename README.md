# Weather CLI App

A simple command-line weather application built with Python and the OpenWeatherMap API.

This project allows users to:

- Check the current weather of a city
- View a 5-day weather forecast
- Handle invalid city names and network errors gracefully
- Use command-line arguments to search cities quickly

---

# Features

- Real-time weather data
- 5-day forecast overview
- Chinese language weather descriptions
- Error handling with `try-except`
- Modular function-based structure
- Command-line interface (CLI)

---

# Technologies Used

- Python 3
- Requests library
- OpenWeatherMap API

---

# Installation

Clone the repository:

```bash
git clone git@github.com:zhoulinhua0-star/weather-cli.git
```

Move into the project folder:

```bash
cd weather-cli
```

Install dependencies:

```bash
pip3 install requests
```

---

# Usage

## macOS / Linux

```bash
python3 main.py Tokyo
```

## Windows

```bash
python main.py Tokyo
```

Example:

```bash
python3 main.py Beijing
```

---

# Example Output

```text
🌍 【Beijing】 当前实时天气
🌡️ 当前温度: 24°C (体感: 22°C) | ☁️ 状况: 多云

📅 【Beijing】 未来 5 天预报概览:
-------------------------------------------------------
🗓️ 日期: 2026-05-17 | 🌡️ 温度: 24.3°C | ☁️ 状况: 多云
🗓️ 日期: 2026-05-18 | 🌡️ 温度: 26.1°C | ☁️ 状况: 小雨
-------------------------------------------------------
```

---

# Project Structure

```text
weather-cli/
│
├── main.py
├── README.md
```

---

# API Setup

This project uses the OpenWeatherMap API.

Get your free API key here:

https://openweathermap.org/api

Then replace:

```python
API_KEY = "your_api_key"
```

with your own API key.

---

# What I Learned

Through this project, I practiced:

- Making API requests with Python
- Parsing JSON data
- Error handling
- Using command-line arguments (`sys.argv`)
- Organizing code into functions
- Building beginner-friendly CLI tools

---

# Future Improvements

Possible future upgrades:

- Add hourly forecasts
- Add weather icons
- Support multiple languages
- Use environment variables for API keys
- Create a GUI version
- Package the app with argparse

---

# Author

Created by Linhua Zhou
