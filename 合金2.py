import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

url = "https://www.atimaterials.com/specialtyrolledproducts/Pages/surcharge-history.aspx"

session = requests.Session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
}

try:
    # 步骤1：获取初始页面
    print("获取初始页面...")
    response = session.get(url)
    response.raise_for_status()

    with open("initial_page.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("已保存初始页面")

    soup = BeautifulSoup(response.text, 'html.parser')


    # 提取所有隐藏参数
    def extract_hidden_params(soup):
        params = {}
        for input_tag in soup.find_all('input', type='hidden'):
            if input_tag.has_attr('id') and input_tag.has_attr('value'):
                params[input_tag['id']] = input_tag['value']
        return params


    hidden_params = extract_hidden_params(soup)
    viewstate = hidden_params.get('__VIEWSTATE', '')
    viewstategenerator = hidden_params.get('__VIEWSTATEGENERATOR', '')
    requestdigest = hidden_params.get('__REQUESTDIGEST', '')
    eventvalidation = hidden_params.get('__EVENTVALIDATION', '')

    print(f"提取参数: VIEWSTATE={len(viewstate)} bytes, GENERATOR={viewstategenerator[:10]}...")

    # 步骤2：模拟选择下拉框和点击按钮
    print("模拟表单提交...")

    form_data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategenerator,
        '__REQUESTDIGEST': requestdigest,
        '__EVENTVALIDATION': eventvalidation,
        'ctl00$ctl39$g_13235907_38e2_4756_80cf_f4e5f1573dee$ctl00$alloyType': 'HTANickel',
        'ctl00$ctl39$g_13235907_38e2_4756_80cf_f4e5f1573dee$ctl00$yearsAvailable': '2025',
        'ctl00$ctl39$g_13235907_38e2_4756_80cf_f4e5f1573dee$ctl00$btnGo': 'Find Results',
        'MSOTlPn_View': '0',
        'MSOSPWebPartManager_DisplayModeName': 'Browse',
        # 添加其他可能的参数
        'MSOTlPn_ShowSettings': 'False',
        'MSOTlPn_Button': 'none',
        'MSOSPWebPartManager_OldDisplayModeName': 'Browse',
        'MSOSPWebPartManager_StartWebPartEditingName': 'false',
        'MSOSPWebPartManager_EndWebPartEditing': 'true',
        # 添加所有隐藏参数
        **hidden_params
    }

    # 发送表单请求
    response = session.post(url, data=form_data)
    response.raise_for_status()

    with open("final_page.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("已保存最终页面")

    # 解析表格（尝试多种定位方式）
    soup = BeautifulSoup(response.text, 'html.parser')

    # 方法1：使用原始ID定位
    table = soup.find('table', {'id': 'ctl00_ctl39_g_13235907_38e2_4756_80cf_f4e5f1573dee_ctl00_historyGrid'})

    # 方法2：使用模糊匹配（如果ID动态变化）
    if not table:
        print("方法1失败，尝试方法2...")
        table = soup.find('table', id=re.compile(r'historyGrid'))

    # 方法3：使用表格内容特征定位
    if not table:
        print("方法2失败，尝试方法3...")
        table = soup.find(lambda tag: tag.name == 'table' and 'Alloy' in tag.text and 'Effective Date' in tag.text)

    if table:
        print("找到目标表格！解析数据...")

        # 提取表头
        headers = []
        header_row = table.find('tr')
        if header_row:
            headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]

        # 提取数据行
        rows = []
        for row in table.find_all('tr')[1:]:
            cols = row.find_all(['td', 'th'])
            if cols:
                rows.append([col.get_text(strip=True) for col in cols])

        if headers and rows:
            df = pd.DataFrame(rows, columns=headers)
            print(f"解析成功：{len(df)} 行，{len(df.columns)} 列")
            print("数据示例：")
            print(df.head().to_string())
            df.to_csv('nickel_surcharge.csv', index=False, encoding='utf-8-sig')
            print("数据已保存到 nickel_surcharge.csv")
        else:
            print("表格内容为空")
    else:
        print("未找到目标表格！请检查 final_page.html")

        # 分析页面是否包含错误信息
        error_msg = soup.find(string=re.compile(r'error|not found|forbidden', re.IGNORECASE))
        if error_msg:
            print(f"页面包含错误信息：{error_msg.strip()[:200]}...")

        # 分析页面是否有验证码或登录提示
        captcha = soup.find(string=re.compile(r'captcha|verification', re.IGNORECASE))
        login = soup.find(string=re.compile(r'login|sign in', re.IGNORECASE))
        if captcha:
            print("页面需要验证码，可能触发了反爬机制")
        elif login:
            print("页面需要登录，可能需要身份验证")

except requests.exceptions.RequestException as e:
    print(f"请求错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")