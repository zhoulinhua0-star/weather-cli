import sys
import requests

def get_current_weather(city_name, api_key):
    """专门负责获取并打印当前实时天气"""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric",
        "lang": "zh_cn"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        description = data['weather'][0]['description']

        print(f"\n🌍 【{city_name}】 当前实时天气")
        print(f"🌡️  当前温度: {temp}°C (体感: {feels_like}°C) | ☁️  状况: {description}")
        return True  # 返回 True 表示查询成功

    except requests.exceptions.HTTPError:
        print(f"\n❌ 获取失败: 请检查城市 '{city_name}' 拼写或 API Key 是否正确。")
        return False  # 失败返回 False，阻止后续执行
    except Exception as e:
        print(f"\n❌ 获取实时天气时发生错误: {e}")
        return False


def get_5_day_forecast(city_name, api_key):
    """专门负责获取并打印未来 5 天预报"""
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric",
        "lang": "zh_cn"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()

        forecast_list = weather_data['list']

        print(f"\n📅 【{city_name}】 未来 5 天预报概览:")
        print("-" * 55)

        for daily_data in forecast_list[::8]:
            time_str = daily_data['dt_txt']
            temp = daily_data['main']['temp']
            description = daily_data['weather'][0]['description']
            date_only = time_str.split(" ")[0]

            print(f"🗓️ 日期: {date_only} | 🌡️ 温度: {temp:5.1f}°C | ☁️ 状况: {description}")

        print("-" * 55, "\n")

    except Exception as e:
        # 主要捕获网络异常
        print(f"\n❌ 获取预报数据时发生错误: {e}")


if __name__ == "__main__":
    API_KEY = "your_api_key"

    if len(sys.argv) < 2:
        print("\n❌ 错误: 缺少参数！")
        print("💡 用法: python main.py <城市名称>")
        print("💡 示例: python main.py Tokyo")
        sys.exit(1)

    city = sys.argv[1]

    # 业务逻辑编排 (Orchestration)：
    # 只有当成功获取当前天气时 (返回 True)，才去请求未来 5 天的预报
    # 这样避免了如果城市输错了，程序连续报错两次的尴尬
    is_success = get_current_weather(city, API_KEY)
    if is_success:
        get_5_day_forecast(city, API_KEY)