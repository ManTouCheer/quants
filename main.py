from PltHelper import draw_xy
from funds.fund import get_open_fund_website, get_single_fund_websites, get_daily_data
from utils.web_helper import get_driver

# 获取开放基金的网址
open_fund_website = get_open_fund_website()
# 获取全部基金的网址
all_fund_websites = get_single_fund_websites(open_fund_website)
driver = get_driver()
for fund_name, website in all_fund_websites:
    data_x, data_y = get_daily_data(website, driver)
    draw_xy(data_x, data_y, fund_name)

driver.close()



