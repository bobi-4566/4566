from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


def scrape_alloy_surcharges(url):

    service = Service('C:\\Users\\35289\\Desktop\\edgedriver_win64\\msedgedriver.exe')
    driver = webdriver.Edge(service=service)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # 点击下拉框以展开选项
        dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ctl39_g_13235907_38e2_4756_80cf_f4e5f1573dee_ctl00_alloyType"]')))
        dropdown.click()
        time.sleep(2)  # 等待下拉菜单展开

        # 在展开的下拉菜单中点击 "Nickel & Cobalt Alloys" 选项
        try:
            target_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//option[contains(text(), "Nickel & Cobalt Alloys")]')))
            target_option.click()
        except Exception as e:
            print(f"点击 'Nickel & Cobalt Alloys' 选项时出现错误: {e}")
            return []

        # 点击 "find results" 按钮
        try:
            find_results_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Find Results"]')))
            find_results_button.click()
            time.sleep(5)  # 等待结果加载
        except Exception as e:
            print(f"点击 'find results' 按钮时出现错误: {e}")
            return []

        # 获取页面源代码
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        tables = soup.find_all('table')
        target_table = None
        for table in tables:
            th_texts = [th.get_text(strip=True) for th in table.find_all('th')]
            if any(month in th_texts for month in ['Jan', 'Feb', 'Mar']):
                target_table = table
                break

        if not target_table:
            print("未找到包含月份数据的表格")
            return []

        # 提取表头和数据
        headers = [th.get_text(strip=True) for th in target_table.find_all('th') if th.get_text(strip=True) in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
        alloy_data = []

        for tr in target_table.find_all('tr'):
            td_tags = tr.find_all('td')
            if len(td_tags) >= len(headers):
                alloy = td_tags[0].get_text(strip=True)
                values = [td.get_text(strip=True) for td in td_tags[1:1 + len(headers)]]
                numeric_values = [float(val) if val else 0.0 for val in values]  # 处理空值
                alloy_data.append({
                    'alloy': alloy,
                   'surcharges': dict(zip(headers, numeric_values))
                })

        return alloy_data

    except Exception as e:
        print(f"爬取失败: {e}")
        return []
    finally:
        driver.quit()


if __name__ == "__main__":
    target_url = "https://www.atimaterials.com/specialtyrolledproducts/Pages/surcharge-history.aspx"
    data = scrape_alloy_surcharges(target_url)
    print(f"共抓取到 {len(data)} 种合金数据")
    # 打印前5条数据（可选）
    for item in data[:5]:
        print(f"合金名称: {item['alloy']}")
        print(f"附加费数据: {item['surcharges']}\n")