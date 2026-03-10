import json
import math
import datetime
from playwright.sync_api import sync_playwright

# 载入现有的 JSON 数据
def load_local_prices():
    with open('prices.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 保存更新后的 JSON 数据
def save_local_prices(data):
    data['config']['last_updated'] = datetime.datetime.utcnow().isoformat() + "Z"
    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_prices():
    data = load_local_prices()
    
    with sync_playwright() as p:
        # 启动无头浏览器
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # 示例 1：抓取即梦图像生成价格 (https://www.volcengine.com/docs/85621/1544714?lang=zh)
            print("正在抓取即梦定价...")
            page.goto("https://www.volcengine.com/docs/85621/1544714?lang=zh", timeout=60000)
            page.wait_for_selector("table") # 等待表格渲染完成
            
            # 注意：这里的选择器需要你通过浏览器 F12 审查元素来精确获取
            # 假设我们获取到了 "即梦AI-文生图3.0" 的价格文本 "0.2"
            # fetched_price = page.locator("xpath=//table/.../td").inner_text()
            
            # 更新逻辑示例
            # for model in data['models']:
            #     if model['official_id'] == 'jimeng-img-3.0':
            #         model['price'] = float(fetched_price)

            # 示例 2：处理 Vidu 积分换算 (1积分 = 0.03125元)
            # 抓取到积分后，如果需要在后端直接转换为 RMB，执行严格的向上取整逻辑
            raw_vidu_points = 32 # 假设抓取到了 32 积分
            rmb_converted = raw_vidu_points * 0.03125
            final_rmb_price = math.ceil(rmb_converted * 100) / 100
            print(f"Vidu 1080p 换算后人民币单价: {final_rmb_price}")

        except Exception as e:
            print(f"抓取过程中发生错误: {e}")
            print("将保留旧版价格数据，防止前端崩溃。")
            
        finally:
            browser.close()
            
    save_local_prices(data)

if __name__ == "__main__":
    update_prices()
