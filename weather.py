from selenium import webdriver

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobar")
    options.add_argument("start-maximized")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("no-sandbox")
    options.add_experimental_option("excludeSwitches", ["Enable-automation"])
    options.add_argument("disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://duckduckgo.com/?q=weather&va=o&t=hx&ia=weather")
    return driver

def find_weather_element():
    driver = get_driver()
    element = driver.find_element(by='xpath', value="/html/body/div[2]/div[6]/div[4]/div/div/div/div/section[1]/ol/li[1]/div/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[3]")
    return element.text