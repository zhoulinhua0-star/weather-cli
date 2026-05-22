import os
import sys
import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

# 初始化 rich 终端控制台
console = Console()

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
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        description = data['weather'][0]['description']

        # 使用富文本拼接内容
        content = (
            f"[bold cyan]🌡️ 当前温度:[/bold cyan] {temp}°C [dim](体感: {feels_like}°C)[/dim]\n"
            f"[bold cyan]☁️ 天气状况:[/bold cyan] {description}"
        )

        # 渲染卡片面板
        panel = Panel(
            content,
            title=f"🌍 [bold yellow]【{city_name}】 当前实时天气[/bold yellow]",
            border_style="blue",
            expand=False  # 根据内容自适应宽度
        )
        console.print()  # 打印空行留白
        console.print(panel)
        return True

    except requests.exceptions.HTTPError:
        console.print(f"\n[bold red]❌ 获取失败:[/bold red] 请检查城市 '{city_name}' 拼写或 API Key 是否正确。")
        return False
    except Exception as e:
        console.print(f"\n[bold red]❌ 获取实时天气时发生错误: {e}[/bold red]")
        return False


def get_5_day_forecast(city_name, api_key):
    """获取预报，拆分今日与未来，并使用 rich Table 渲染"""
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

        # 1. 按日期分组处理数据
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

        # 2. 提取今天和未来的日期
        dates = list(daily_data.keys())
        today_date = dates[0]
        future_dates = dates[1:]

        # --- 渲染今日综合预报面板 ---
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

        # --- 渲染未来几天预报的表格 ---
        table = Table(
            title="📅 [bold magenta]未来预报概览 (明日起)[/bold magenta]",
            box=box.ROUNDED,  # 圆角边框
            header_style="bold cyan"
        )

        # 添加表头
        table.add_column("🗓️ 日期", justify="center")
        table.add_column("📉 最低温", justify="right", style="blue")
        table.add_column("📈 最高温", justify="right", style="red")
        table.add_column("☁️ 状况", justify="center", style="white")

        # 填充表格数据
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
        console.print(f"\n[bold red]❌ 获取预报数据时发生错误: {e}[/bold red]")


if __name__ == "__main__":
    API_KEY = os.getenv("API_KEY")

    if len(sys.argv) < 2:
        console.print("\n[bold red]❌ 错误: 缺少参数！[/bold red]")
        console.print("[yellow]💡 用法: python main.py <城市名称>[/yellow]")
        console.print("[yellow]💡 示例: python main.py Tokyo[/yellow]\n")
        sys.exit(1)

    city = sys.argv[1]

    # 业务逻辑编排
    is_success = get_current_weather(city, API_KEY)
    if is_success:
        get_5_day_forecast(city, API_KEY)