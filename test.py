from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 设置 Chrome 选项（可选）
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
# chrome_options.add_argument("--headless")  # 启动无头模式

# 使用 webdriver_manager 自动管理驱动版本
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
# 打开网页
url = 'https://main.m.taobao.com/order/index.html?skuId=5320306445942&quantity=1&itemId=714273870642'
driver.get(url)
element = driver.find_element(By.LINK_TEXT, "提交订单")
element.click()
# 输出网页标题

# 保持浏览器窗口打开，直到用户手动关闭
# 注释掉或移除 driver.quit() 行
# driver.quit()

# 如果需要在脚本结束后保持浏览器打开，也可以使用 input() 函数等待输入
input("按 Enter 键关闭浏览器...")
driver.quit()