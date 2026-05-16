import sys
import requests


def get_5_day_forecast(city_name, api_key):
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

        print(f"\n📅 {city_name} 的未来 5 天预报概览:")
        print("-" * 50, "\n")

        for daily_data in forecast_list[::8]:
            time_str = daily_data['dt_txt']
            temp = daily_data['main']['temp']
            description = daily_data['weather'][0]['description']
            date_only = time_str.split(" ")[0]

            print(f"🗓️ 日期: {date_only} | 🌡️ 温度: {temp:5.1f}°C | ☁️ 状况: {description}")

        print("-" * 50)

    except requests.exceptions.HTTPError:
        print(f"\n❌ 获取失败: 请检查城市名称拼写或 API Key 是否正确。")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")


if __name__ == "__main__":
    API_KEY = "14c80980f0e3904c7dab6d6591c42efd"

    # 如果 len(sys.argv) < 2，说明用户只输入了 python main.py，漏掉了城市名
    if len(sys.argv) < 2:
        print("\n❌ 错误: 缺少参数！")
        print("💡 用法: python main.py <城市名称>")
        print("💡 示例: python main.py Tokyo")
        sys.exit(1)  # 优雅退出程序，1 表示异常退出

    # 获取命令行传入的第一个参数作为城市名
    city = sys.argv[1]

    # 直接执行查询，查完程序就结束
    get_5_day_forecast(city, API_KEY)
