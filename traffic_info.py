#!/usr/bin/env python3
"""
查询南阳到深圳的交通信息
"""
import re
from datetime import datetime, timedelta

def get_general_route_info():
    """获取南阳到深圳的一般路线信息"""
    # 路线信息
    routes = {
        "高铁/动车": {
            "distance": "约 1200-1400 公里",
            "duration": "4.5-6 小时",
            "stops": ["南阳东", "驻马店西", "武汉", "长沙南", "广州南", "深圳北"],
            "advantages": ["时间短", "舒适", "准时", "不受堵车影响"],
            "disadvantages": ["票价较高", "需要到站乘车"]
        },
        "自驾": {
            "distance": "约 1200-1400 公里",
            "duration": "12-15 小时（正常路况）",
            "highways": ["二广高速", "京港澳高速", "许广高速"],
            "major_cities": ["郑州", "武汉", "长沙", "衡阳", "广州"],
            "advantages": ["时间灵活", "可以带更多行李", "目的地交通便利"],
            "disadvantages": ["疲劳驾驶", "油费过路费", "受堵车影响"]
        },
        "飞机": {
            "duration": "约 2-3 小时（不含中转）",
            "distance": "约 1200-1400 公里",
            "stops": ["南阳姜营机场", "武汉/郑州中转", "深圳宝安机场"],
            "advantages": ["最快", "最安全", "最舒适"],
            "disadvantages": ["价格较高", "受天气影响大", "需要提前到达机场"]
        }
    }

    return routes

def get_congestion_forecast():
    """获取堵车预测"""
    current_hour = datetime.now().hour

    # 堵车时段
    rush_hours = {
        "早高峰": (7, 9),  # 7:00-9:00
        "晚高峰": (17, 19),  # 17:00-19:00
        "周末全天": None  # 周末全天都较堵
    }

    # 易堵车路段
    congestion_points = [
        "武汉周边（二广高速）",
        "长沙周边（京港澳高速）",
        "衡阳、郴州段（二广高速）",
        "广州周边（虎门大桥、环城高速）",
        "深圳周边（机荷高速、广深高速）"
    ]

    # 节假日建议
    holiday_suggestions = {
        "春节": "建议提前 3-5 天出发，避开腊月二十八、二十九和除夕",
        "国庆": "建议提前 2-3 天出发，避开 10 月 1 日和 10 月 6-7 日",
        "清明节": "建议提前 1-2 天出发",
        "劳动节": "建议提前 2-3 天出发"
    }

    return {
        "rush_hours": rush_hours,
        "congestion_points": congestion_points,
        "holiday_suggestions": holiday_suggestions
    }

def get_departure_recommendation():
    """获取出发时间建议"""
    info = get_congestion_forecast()
    current_hour = datetime.now().hour
    current_weekday = datetime.now().strftime("%A")

    # 今天是星期几
    weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = weekday_names[datetime.now().weekday()]

    # 建议出发时间
    recommendations = {}

    if today in ["Saturday", "Sunday"]:
        # 周末
        if current_hour < 6:
            recommendations["自驾"] = "建议现在出发（早鸟，避免早高峰）"
            recommendations["高铁"] = "可以稍晚出发，避开早高峰"
        elif current_hour < 12:
            recommendations["自驾"] = "建议等到 14:00 后出发，避开中午时段"
            recommendations["高铁"] = "可以随时出发，但建议提前购票"
        else:
            recommendations["自驾"] = "建议明天早上 5:00-6:00 出发"
            recommendations["高铁"] = "可以随时出发，但建议提前购票"
    else:
        # 工作日
        if current_hour < 5:
            recommendations["自驾"] = "建议现在出发（早鸟）"
            recommendations["高铁"] = "可以稍晚出发，避开早高峰"
        elif current_hour < 10:
            recommendations["自驾"] = "建议等到 22:00 后出发（夜猫模式）"
            recommendations["高铁"] = "可以随时出发，但建议提前购票"
        elif current_hour < 17:
            recommendations["自驾"] = "建议等到 22:00 后出发（夜猫模式）"
            recommendations["高铁"] = "可以随时出发，但建议提前购票"
        else:
            recommendations["自驾"] = "建议现在出发（晚高峰已过）"
            recommendations["高铁"] = "可以随时出发，但建议提前购票"

    # 总体建议
    if today in ["Friday", "Saturday", "Sunday"]:
        recommendations["general"] = "🔴 注意：今天是周五/周六/周日，堵车风险较高"
    else:
        recommendations["general"] = "🟢 今天是工作日，路况相对较好"

    return recommendations

def format_report():
    """格式化报告"""
    print("="*60)
    print("南阳 → 深圳交通信息查询")
    print("="*60)
    print(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 路线信息
    print("📍 路线信息:")
    print("-"*60)
    routes = get_general_route_info()
    for transport, info in routes.items():
        print(f"\n{transport}:")
        print(f"  距离: {info['distance']}")
        print(f"  预计时长: {info['duration']}")
        if 'stops' in info:
            print(f"  主要站点: {' → '.join(info['stops'])}")
        if 'highways' in info:
            print(f"  主要高速: {' → '.join(info['highways'])}")
        print(f"  优势: {', '.join(info['advantages'][:3])}...")
        print(f"  劣势: {', '.join(info['disadvantages'][:3])}...")

    # 堵车情况
    print("\n\n🚗 堵车预测:")
    print("-"*60)
    forecast = get_congestion_forecast()
    print(f"当前时段: {current_hour}:00")
    print(f"易堵车路段: {', '.join(forecast['congestion_points'][:3])}...")

    # 出发建议
    print("\n\n⏰ 出发时间建议:")
    print("-"*60)
    recommendations = get_departure_recommendation()
    print(f"总体情况: {recommendations['general']}")

    for transport, advice in recommendations.items():
        if transport != "general":
            print(f"\n{transport}:")
            print(f"  {advice}")

    # 额外提示
    print("\n\n💡 温馨提示:")
    print("-"*60)
    tips = [
        "建议使用高德地图或百度地图实时查询路况",
        "出发前检查车辆状况（如果是自驾）",
        "准备充足的食物和水",
        "规划好休息站点（自驾每 3-4 小时休息一次）",
        "关注沿途天气预报，避免恶劣天气出行",
        "如果是春节、国庆等假期，建议提前 3-5 天出发",
        "准备好备选路线，遇到堵车时及时调整"
    ]

    for tip in tips:
        print(f"  • {tip}")

    print("\n" + "="*60)
    print("祝您一路平安！🚗")
    print("="*60)

def main():
    format_report()

if __name__ == "__main__":
    main()
