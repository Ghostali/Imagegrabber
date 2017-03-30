from selenium import webdriver
import time

links = []


# scrawls website for images in a <img> tag
def website(site,option):
    del links[:]
    # open firefox and go to the looking glass website
    driver = webdriver.PhantomJS()
    driver.maximize_window()
    driver.get(site)
    for _ in range(int(option)):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("Scrolling")
        time.sleep(2)
    images = driver.find_elements_by_xpath('//img[@src]')
    for image in images:
        print(image.get_attribute('src'))
        links.append(image.get_attribute('src'))
    driver.quit()
    print(links)
    return links
