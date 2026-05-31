import os
import sys
import time  # 💡 新增：用于在重试之间稍微等待一下
import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

# 初始化 rich 终端控制台
console = Console()

# 自动从 .env 文件中加载环境变量
load_dotenv()


def get_current_weather(city_name, api_key):
    """获取实时天气，并使用 rich Panel 渲染"""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric",
        "lang": "zh_cn"
    }

    try:
        # 增加 timeout 防止死等
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        description = data['weather'][0]['description']

        content = (
            f"[bold cyan]🌡️ 当前温度:[/bold cyan] {temp}°C [dim](体感: {feels_like}°C)[/dim]\n"
            f"[bold cyan]☁️ 天气状况:[/bold cyan] {description}"
        )

        panel = Panel(
            content,
            title=f"🌍 [bold yellow]【{city_name}】 当前实时天气[/bold yellow]",
            border_style="blue",
            expand=False
        )
        console.print()
        console.print(panel)
        return True

    except requests.exceptions.HTTPError:
        console.print(f"\n[bold red]❌ 获取失败:[/bold red] 请检查城市 '{city_name}' 拼写或 API Key 是否正确。")
        return False
    except Exception as e:
        console.print(f"\n[bold red]❌ 获取实时天气时发生错误: {e}[/bold red]")
        return False


def get_5_day_forecast(city_name, api_key):
    """获取预报，带有自动重试机制防网络截断"""
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric",
        "lang": "zh_cn"
    }

    max_retries = 3  # 💡 自动重试 3 次
    weather_data = None

    for attempt in range(max_retries):
        try:
            # timeout=10 保证不会无限卡住
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()

            # 尝试解析 JSON，如果网络截断这里会报错并触发 except
            weather_data = response.json()
            break  # 💡 如果成功解析，直接跳出重试循环！

        except Exception as e:
            if attempt < max_retries - 1:
                console.print(f"[yellow]⚠️ 网络波动导致数据残缺，正在进行第 {attempt + 2} 次重试...[/yellow]")
                time.sleep(1)  # 等待 1 秒后再试
            else:
                console.print(f"\n[bold red]❌ 连续 {max_retries} 次获取预报数据失败，请检查网络环境。[/bold red]")
                return

    # 如果三次都失败了，weather_data 会是 None，直接结束
    if not weather_data:
        return

    try:
        forecast_list = weather_data['list']

        daily_data = {}
        for item in forecast_list:
            date_only, time_only = item['dt_txt'].split(" ")
            temp = item['main']['temp']
            description = item['weather'][0]['description']

            if date_only not in daily_data:
                daily_data[date_only] = {'temps': [], 'midday_desc': description}

            daily_data[date_only]['temps'].append(temp)
            if time_only == "12:00:00":
                daily_data[date_only]['midday_desc'] = description

        dates = list(daily_data.keys())
        today_date = dates[0]
        future_dates = dates[1:]

        today_min = min(daily_data[today_date]['temps'])
        today_max = max(daily_data[today_date]['temps'])
        today_desc = daily_data[today_date]['midday_desc']

        today_content = (
            f"[bold]🗓️ 日期:[/bold] {today_date}\n"
            f"[bold blue]📉 最低温度:[/bold blue] {today_min:5.1f}°C  |  [bold red]📈 最高温度:[/bold red] {today_max:5.1f}°C\n"
            f"[bold]☁️ 总体状况:[/bold] {today_desc}"
        )
        today_panel = Panel(
            today_content,
            title="[bold green]▶ 今日综合预报[/bold green]",
            border_style="green",
            expand=False
        )
        console.print(today_panel)

        table = Table(
            title="📅 [bold magenta]未来预报概览 (明日起)[/bold magenta]",
            box=box.ROUNDED,
            header_style="bold cyan"
        )

        table.add_column("🗓️ 日期", justify="center")
        table.add_column("📉 最低温", justify="right", style="blue")
        table.add_column("📈 最高温", justify="right", style="red")
        table.add_column("☁️ 状况", justify="center", style="white")

        for d in future_dates:
            t_min = min(daily_data[d]['temps'])
            t_max = max(daily_data[d]['temps'])
            desc = daily_data[d]['midday_desc']
            table.add_row(
                d,
                f"{t_min:.1f}°C",
                f"{t_max:.1f}°C",
                desc
            )

        console.print(table)
        console.print()

    except Exception as e:
        console.print(f"\n[bold red]❌ 渲染预报数据时发生错误: {e}[/bold red]")


if __name__ == "__main__":
    API_KEY = os.getenv("API_KEY")

    if not API_KEY:
        console.print("\n[bold red]❌ 错误: 未能在环境变量或 .env 文件中找到 'API_KEY'！[/bold red]")
        console.print("[yellow]💡 请检查项目根目录下是否存在 .env 文件，且内容为: API_KEY=你的真实Key[/yellow]\n")
        sys.exit(1)

    if len(sys.argv) < 2:
        console.print("\n[bold red]❌ 错误: 缺少参数！[/bold red]")
        console.print("[yellow]💡 用法: python main.py <城市名称>[/yellow]")
        console.print("[yellow]💡 示例: python main.py New York[/yellow]\n")
        sys.exit(1)

    # 💡 已经包含了之前拼接带空格城市名（如 New York）的逻辑
    city = " ".join(sys.argv[1:])

    is_success = get_current_weather(city, API_KEY)
    if is_success:
        get_5_day_forecast(city, API_KEY)