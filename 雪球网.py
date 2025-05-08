import requests
import time
import json
import random
from functools import wraps

XUEQIU_COOKIE = "cookiesu=921746689754896; device_id=69e401b835a3e05149c017321b247d53; smidV2=20250508153557c8e80c940954dba374697560d056fbd300a4c9f8edb179400; s=bt19mimbn6; remember=1; xq_a_token=6f4faac43b5f74ff1a41c963f363762d8571f0cc; xqat=6f4faac43b5f74ff1a41c963f363762d8571f0cc; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjk1MDYzODc2MTYsImlzcyI6InVjIiwiZXhwIjoxNzQ5Mjg0ODY2LCJjdG0iOjE3NDY2OTI4NjY5MDMsImNpZCI6ImQ5ZDBuNEFadXAifQ.OCnTAUZ05GBa_tYGTEbedYJTVVMt90pbtVvM87iTT1N11GztH8S02L6W2GS2lSYUWG0S2okyHRoaMrX4tfviQKx1leZ5EG3el2HHXv9zpSjUeLeS5AQWCmLXgfE-kJFqqokMGK-D8-aCq4WASE5Vlh8JdIMtkPOs1LHc8ocP64Mh2_aR20qf7bLYD3NkXRY2me3h1IQCY4kOnGuTlYtVI64ShdNcpjntjEriI07noMzIW8LbMIsoDFu6GU9gxaP0AhuoZpthLa9rAcCuEbNOa0Vr59jyfXFmDqSk2BDcO5XvNJ4JeR_CXZDVlqfVKTEyicQyzek5FpblXA8knTOkyQ; xq_r_token=46d564513531d4a1b2c41b1e7b64f7daa0bfedb4; xq_is_login=1; u=9506387616; acw_tc=0a27a99b17466999837552342e005dd66e7e379e02d729de37eddf8f4d1322; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=vD3HEROPQCWFksXTeaA6IFgpipEt/IgohLipy4iBf7soJ2HGccnQNG+yW1ThasIh/UqDo9NAfe46ciaoLaqD/g%3D%3D; ssxmod_itna=YuDQ0KYKGKDv=1DhpDgQxpxYknDumDWqGHDyhxYK0C8DLxnRDGdzRq8woDyjCAHm70XKPlmdm2eDBTnYDSxD6HDK4GTwzgAitsP4p04ThabQRGqI+KmUYu4qtAjGCpvkmtn+rKxCPGnD0=NKGLrDYAfDBYD74G+DDeDi2iD84D+DGp5LnR5xi3onDqDzq0YxG33xYp5TeDgmDDBGRNDKTPodDDl3AHGtAhe7cbVCPw8xGtNjej5x0taDBLi+UG5wa8fdiTdHKQaa32r5PGuDG=QzeGmDjFOmmTa=khSnkLtKoeIDEh3FAAqA5NjGznGiiD4t+sCDhDv4AvRe2rjPDDatDbt3wzG0xKhB35SFHMm2Y8GOli1nhtfwbn28Y2H30NmO4UvtRxNSRtSr=hOPU04CgxvAOfGDD; ssxmod_itna2=YuDQ0KYKGKDv=1DhpDgQxpxYknDumDWqGHDyhxYK0C8DLxnRDGdzRq8woDyjCAHm70XKPlmdmrDi=3WmCo8nD03qtebfYNhKDGX7Wp4+kxjhqg1iB0=lIiS+058VFfcgEctyuk9myXALX9dNV4kh2DwiclB0XCTrBlAXPdD2Z4r5eTkh3nl6eIu=54Pddil2uenid=uTYiQRuYdRqoMflzl6q1M2QV+jqtAuHb0=+suy3mb03sgDEluqXGuXKTMB13G=1FUBaTGQ+LId0H/FEdvOUz9Ngbd8U9MBz+XM0Da/5LCNVS+8/BRM8cczeAY77fmDqrp45C4rfjGgI+5mudmnRf0wj9uzxbFP2BIPwpHUbQiP+Y9G8I23v54mRzhRRq2I42n7DVrOF04/xqBRW7i7mF8ex4NculGnYTeOe80R67Y1ewklqAW9BWKzSbg+n/GIrTqzlPW0bHogI9Teliv3v5kS8su6twtURx0wCDvRn2=d9ze9fn2u4xbNwFAReNuamLTvaG9rO8fPP7mdFopOfYDQ2WLAoQkGQkF5fOsVAiKZwT38432CM4Lev/mikTxGwPX+P0mH8DhgjhEP845hrT/ifcYYzGBcBIFKrqQ0xzbEtDCKiPAUxYybPrF6tF3G9Y5XKG5F/ypRqrv9wRknIWfir4sE/lvYwx7Mb50I=0WzNAlFinX9kDQpRE7BxqrW8+QgV9x82=KX3EDOGAO3SEBL7FD3m3C48MDzGEwC8DiEYfGWq3bGr7xKh47P5xhY5BxsDY+r0he7rFeSGU4iDD"  # 必须更新有效Cookie
EXCHANGE_API_KEY = "c6c86684e45f49e445994cc9"


def get_exchange_rate():
    """获取实时美元兑人民币汇率"""
    try:
        response = requests.get(
            f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/USD",
            timeout=10
        )
        data = response.json()
        return data["conversion_rates"]["CNY"]
    except Exception as e:
        print(f"汇率获取失败，使用默认汇率7.25 | 错误: {str(e)}")
        return 7.25  # 默认值


def retry(max_retries=3, delay=5):
    """请求重试装饰器"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"第{attempt + 1}次重试，错误: {str(e)}")
                        time.sleep(delay * (attempt + 1))
                    else:
                        raise
            return None

        return wrapper

    return decorator


@retry(max_retries=3, delay=5)
def get_xueqiu_stock_info(symbol, exchange_rate):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Cookie": XUEQIU_COOKIE,
        "X-Requested-With": "XMLHttpRequest"
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        # 前置访问获取有效Cookie
        session.get("https://xueqiu.com/", timeout=10)
        time.sleep(random.uniform(1, 3))  # 随机延迟

        # 请求股票数据
        api_url = "https://stock.xueqiu.com/v5/stock/quote.json"
        response = session.get(
            api_url,
            params={"symbol": symbol.upper(), "extend": "detail"},
            timeout=20
        )
        response.encoding = "utf-8"

        # 验证响应内容
        try:
            data = response.json()
        except json.JSONDecodeError:
            print(f"响应异常，状态码: {response.status_code}")
            print(f"响应内容: {response.text[:200]}...")
            return None

        # 处理接口错误
        if data.get("error_code", 0) != 0:
            print(f"接口错误: {data.get('error_description', '未知错误')}")
            return None

        # 解析股票数据
        stock_data = data.get("data", {}).get("quote", {})
        if not stock_data:
            print("未找到有效股票数据")
            return None

        # 获取基础信息
        currency = stock_data.get("currency", "CNY")
        current = stock_data.get("current", 0)
        market_cap = stock_data.get("market_capital", 0)  # 单位：人民币分

        # 转换为人民币单位
        if currency == "USD":
            current_cny = current * exchange_rate
            market_cap_cny = (market_cap / 1e8) * 100  # 分 -> 元 -> 亿元
        else:  # CNY/HKD
            current_cny = current
            market_cap_cny = market_cap / 1e8  # 分 -> 亿元

        return {
            "symbol": symbol,
            "name": stock_data.get("name", "N/A"),
            "currency": "CNY",
            "price": round(current_cny, 2),
            "market_cap": round(market_cap_cny, 2)
        }

    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {str(e)}")
        return None
    except Exception as e:
        print(f"未处理异常: {str(e)}")
        return None


if __name__ == "__main__":
    exchange_rate = get_exchange_rate()
    print(f"当前汇率: 1 USD = {exchange_rate} CNY")

    stock_list = [
        ("TSLA", "特斯拉"),
        ("AAPL", "苹果"),
        ("00700.HK", "腾讯"),
        ("SH600519", "贵州茅台"),
        ("AMZN", "亚马逊")
    ]

    for symbol, name in stock_list:
        print(f"\n【{name}】数据获取中...")
        stock_info = get_xueqiu_stock_info(symbol, exchange_rate)

        if stock_info:
            print(f"股票名称: {stock_info['name']}")
            print(f"当前价格: {stock_info['price']} {stock_info['currency']}")
            print(f"公司市值: {stock_info['market_cap']}亿 {stock_info['currency']}")
        else:
            print("数据获取失败，请检查网络或股票代码")

        time.sleep(random.uniform(3, 6))  # 请求间隔

    print("\n数据更新完成，汇率更新时间:", time.strftime("%Y-%m-%d %H:%M:%S"))