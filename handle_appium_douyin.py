import time
from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


cap = {
  "platformName": "Android",
  "platformVersion": "7.1.1",
  "deviceName": "913eea43",
  "appPackage": "io.va.exposed",
  "appActivity": "io.virtualapp.splash.SplashActivity",
  "noReset": True,
    "unicodekeyboard":True,
    "resetkeyboard":True,
}

driver = webdriver.Remote("http://localhost:4723/wd/hub",cap)

def get_size():
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return(x,y)

element = driver.find_element_by_xpath("//android.widget.TextView[@content-desc='设置']")
ActionChains(driver).click_and_hold(on_element=element).perform()
ActionChains(driver).move_to_element_with_offset(to_element=element,xoffset=0,yoffset=5).perform()
time.sleep(0.5)
driver.find_element_by_class_name("android.widget.TextView").click()
time.sleep(8)

def handle_douyin(driver):
    #点击放大镜
    driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.ss.android.ugc.aweme:id/aft']").click()
    driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/jt']").click()
    time.sleep(0.1)
    #定位搜索框
    driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/jt']").send_keys('lwnx1208')
    time.sleep(0.1)
    #点击搜索
    driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/a8w']").click()
    #点击用户标签
    driver.find_element_by_xpath("//android.widget.TextView[@text='用户']").click()
    #点击头像
    driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView[@resource-id='com.ss.android.ugc.aweme:id/kh']/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/android.widget.ImageView[1]").click()
    #点击粉丝按钮
    driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/a6a']").click()

    l = get_size(driver)
    x1 = int(l[0]*0.5)
    y1 = int(l[1]*0.75)
    y2 = int(l[1]*0.25)
    while True:
        if '没有更多了' in driver.page_source:
            break
        driver.swipe(x1,y1,x1,y2)
        time.sleep(0.5)

if __name__ == '__main__':
    handle_douyin(driver)