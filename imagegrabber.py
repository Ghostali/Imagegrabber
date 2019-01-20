from selenium import webdriver
import time

links = []


# scrawls website for images in a <img> tag
def website(site, option):
    del links[:]
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(site)
    for _ in range(int(option)):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("Scrolling")
        time.sleep(0.5)
    images = driver.find_elements_by_xpath('//img[@src]')
    for image in images:
        if 'http' not in image.get_attribute('src'):
            links.append(site + '/' + image.get_attribute('src'))
        else:
            links.append(image.get_attribute('src'))
    driver.quit()
    return set(links)
