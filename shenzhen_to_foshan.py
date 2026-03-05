#!/usr/bin/env python3
"""
深圳到佛山旅游攻略
"""
from datetime import datetime

def get_cities_info():
    """获取深圳和佛山的主要景点和美食"""
    cities = {
        "深圳": {
            "districts": ["南山区", "福田区", "罗湖区", "宝安区", "龙岗区", "盐田区", "龙华区", "坪山区", "光明区"],
            "attractions": {
                "南山/福田": ["深圳湾", "欢乐港湾", "世界之窗", "锦绣中华民俗村", "欢乐谷"],
                "罗湖": ["东门老街", "地王大厦", "万象城"],
                "宝安": ["海上田园", "凤凰山", "深圳机场"],
                "大梅沙": ["大梅沙海滨公园", "杨梅坑"]
            },
            "food": ["深圳早茶", "潮汕牛肉火锅", "广东煲仔饭", "肠粉", "猪脚饭", "潮汕卤鹅", "沙井鲜蚝"],
            "shopping": ["华强北电子市场", "万象城", "东门步行街", "KK MALL", "COCO Park", "海岸城"]
        },
        "佛山": {
            "districts": ["禅城区", "南海区", "顺德区", "三水区", "高明区"],
            "attractions": {
                "禅城区": ["祖庙", "岭南天地", "梁园", "南风古灶", "佛山创意产业园"],
                "南海区": ["西樵山", "千灯湖", "南海影视城", "南国桃园", "梦里水乡"],
                "顺德区": ["清晖园", "顺德博物馆", "长鹿农庄", "碧江金楼", "逢简水乡"],
                "三水区": ["三水荷花世界", "三水森林公园", "三水温泉"],
                "高明区": ["皂幕山", "盈香生态园", "泰康山"]
            },
            "food": ["顺德鱼生", "双皮奶", "佛山盲公饼", "佛山扎蹄", "均安蒸猪", "伦教糕", "柱侯鸡", "石湾鱼皮", "佛山烧鹅"],
            "specialties": ["佛山陶瓷", "佛山剪纸", "佛山醒狮", "粤剧", "功夫文化"]
        }
    }

    return cities

def get_transport_info():
    """获取交通信息"""
    transport = {
        "高铁": {
            "duration": "约 30 分钟",
            "stations": ["深圳北", "佛山新城/佛山"],
            "advantages": ["时间短", "舒适", "准时"],
            "cost": "约 60-100 元"
        },
        "地铁": {
            "lines": ["深圳地铁3号线/5号线 → 广佛线", "深圳地铁11号线"],
            "duration": "约 1-1.5 小时",
            "advantages": ["便宜", "方便", "不受堵车影响"],
            "cost": "约 10-20 元"
        },
        "自驾": {
            "distance": "约 60-80 公里",
            "duration": "约 1-1.5 小时（正常路况）",
            "highways": ["广深沿江高速", "广深高速", "珠三角环线高速"],
            "advantages": ["时间灵活", "可以带更多行李"],
            "cost": "油费约 50-80 元 + 过路费约 30-50 元"
        },
        "大巴": {
            "duration": "约 1.5-2 小时",
            "stations": ["深圳汽车站", "福田汽车站", "宝安汽车站"],
            "advantages": ["便宜", "班次多"],
            "cost": "约 30-50 元"
        }
    }

    return transport

def get_itinerary(days):
    """获取行程安排"""
    if days == 1:
        return {
            "上午": ["深圳出发（8:00）", "抵达佛山（9:30）", "游览祖庙（10:00-12:00）"],
            "中午": ["品尝顺德美食（12:00-13:30）"],
            "下午": ["游览西樵山（14:00-17:00）", "返回深圳（18:00）"]
        }
    elif days == 2:
        return {
            "第一天": {
                "上午": ["深圳出发（8:00）", "抵达佛山（9:30）", "游览祖庙、梁园（10:00-12:00）"],
                "中午": ["品尝顺德美食（12:00-13:30）"],
                "下午": ["游览南风古灶（14:00-17:00）"],
                "晚上": ["入住酒店（18:00）", "品尝佛山夜宵（19:00-21:00）"]
            },
            "第二天": {
                "上午": ["游览西樵山（9:00-12:00）", "参观佛山陶瓷博物馆（12:00-13:00）"],
                "中午": ["品尝双皮奶、佛山盲公饼（13:00-14:00）"],
                "下午": ["游览顺德清晖园、长鹿农庄（14:00-17:00）"],
                "晚上": ["返回深圳（18:00）"]
            }
        }
    else:
        return {
            "第一天": "深圳 → 佛山，游览祖庙、岭南天地",
            "第二天": "游览西樵山、千灯湖",
            "第三天": "顺德美食之旅，游览清晖园、碧江金楼、逢简水乡",
            "第四天": "禅城文化之旅，参观南风古灶、佛山创意产业园",
            "第五天": "返回深圳，购买特产（佛山陶瓷、双皮奶等）"
        }

def format_report():
    """格式化报告"""
    print("="*70)
    print("深圳 → 佛山旅游攻略")
    print("="*70)
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 城市信息
    cities = get_cities_info()

    print("🏙️ 城市信息")
    print("-"*70)
    print("\n📍 深圳:")
    print(f"  主要区域: {', '.join(cities['深圳']['districts'][:6])}...")
    print(f"  代表景点: {', '.join(cities['深圳']['attractions']['南山/福田'][:3])}...")
    print(f"  特色美食: {', '.join(cities['深圳']['food'][:5])}...")
    print(f"  购物场所: {', '.join(cities['深圳']['shopping'][:3])}...")

    print("\n\n📍 佛山:")
    print(f"  主要区域: {', '.join(cities['佛山']['districts'])}")
    print(f"  顺德特色: 清晖园、长鹿农庄、碧江金楼、逢简水乡")
    print(f"  南海特色: 西樵山、千灯湖、南国桃园")
    print(f"  特色美食: {', '.join(cities['佛山']['food'][:5])}...")
    print(f"  文化特色: {', '.join(cities['佛山']['specialties'])}")

    # 交通信息
    print("\n\n🚗 交通方式")
    print("-"*70)
    transport = get_transport_info()

    print("\n✈️ 高铁:")
    print(f"  时长: {transport['高铁']['duration']}")
    print(f"  车次: {' → '.join(transport['高铁']['stations'])}")
    print(f"  票价: {transport['高铁']['cost']}")
    print(f"  优势: {', '.join(transport['高铁']['advantages'])}")

    print("\n🚇 地铁:")
    print(f"  时长: {transport['地铁']['duration']}")
    print(f"  线路: {', '.join(transport['地铁']['lines'])}")
    print(f"  票价: {transport['地铁']['cost']}")
    print(f"  优势: {', '.join(transport['地铁']['advantages'])}")

    print("\n🚗 自驾:")
    print(f"  距离: {transport['自驾']['distance']}")
    print(f"  时长: {transport['自驾']['duration']}")
    print(f"  高速: {', '.join(transport['自驾']['highways'])}")
    print(f"  费用: {transport['自驾']['cost']}")
    print(f"  优势: {', '.join(transport['自驾']['advantages'])}")

    print("\n🚌 大巴:")
    print(f"  时长: {transport['大巴']['duration']}")
    print(f"  车站: {', '.join(transport['大巴']['stations'])}")
    print(f"  票价: {transport['大巴']['cost']}")
    print(f"  优势: {', '.join(transport['大巴']['advantages'])}")

    # 行程安排
    print("\n\n📅 行程安排")
    print("-"*70)
    print("\n📆 1日游:")
    itinerary_1day = get_itinerary(1)
    for period, activities in itinerary_1day.items():
        print(f"  {period}: {', '.join(activities)}")

    print("\n\n📆 2日游:")
    itinerary_2day = get_itinerary(2)
    for day, schedule in itinerary_2day.items():
        print(f"  {day}:")
        for period, activities in schedule.items():
            print(f"    {period}: {', '.join(activities)}")

    print("\n\n📆 3-5日游:")
    itinerary_3to5 = get_itinerary(5)
    for day, plan in itinerary_3to5.items():
        print(f"  {day}: {plan}")

    # 温馨提示
    print("\n\n💡 旅游小贴士")
    print("-"*70)
    tips = [
        "顺德美食是必尝的，特别是顺德鱼生、双皮奶、伦教糕",
        "佛山陶瓷和剪纸是很好的伴手礼",
        "西樵山建议坐缆车，可以节省体力",
        "清晖园和梁园可以一起游览，距离很近",
        "如果时间充裕，建议去顺德吃一顿正宗的顺德宴",
        "佛山祖庙可以感受岭南文化，很有历史感",
        "南风古灶是世界文化遗产，非常壮观",
        "岭南天地有很多特色小店，可以买到纪念品",
        "佛山的高铁站和地铁站都很方便，交通便利",
        "建议提前预订酒店，特别是节假日期间"
    ]

    for i, tip in enumerate(tips, 1):
        print(f"  {i}. {tip}")

    print("\n" + "="*70)
    print("祝您佛山之旅愉快！🎉")
    print("="*70)

if __name__ == "__main__":
    format_report()
