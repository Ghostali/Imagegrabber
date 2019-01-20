from selenium import webdriver
import time
from selenium.common import exceptions

links = []


# scrawls website for images in a <img> tag
def website(site, option):
    del links[:]
    driver = webdriver.PhantomJS()
    driver.maximize_window()
    driver.get(site)
    for _ in range(int(option)):
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("Scrolling")
            time.sleep(2)
        except exceptions.StaleElementReferenceException:
            pass
    images = driver.find_elements_by_xpath('//img[@src]')
    for image in images:
        links.append(image.get_attribute('src'))
    driver.quit()
    return set(links)
