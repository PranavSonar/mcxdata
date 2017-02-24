"""
Created on Feb 22, 2017
@author: Souvik
@Program Function: Download MCX bhavcopy data


"""

import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import dates

location = 'C:/Users/Souvik/OneDrive/Python/mcxdata/data' # Laptop
# location = 'C:/Users/SVK/OneDrive/Python/mcxdata/data' # Desktop

url = 'https://www.mcxindia.com/market-data/bhavcopy'
chromedriver = 'C:\Program Files (x86)/chromedriver_win32/chromedriver.exe'
logfile = 'log.txt'


os.chdir(location)

#date_range = dates.dates('2017-02-17', '2017-02-20')
date_range = dates.dates('2008-02-19')

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
prefs = {"download.default_directory" : location}
options.add_experimental_option("prefs",prefs)
#options.add_argument(location)

browser = webdriver.Chrome(chromedriver, chrome_options=options)
browser.get(url)

select_year_xpath = "//div[@class='datepick-month-header']/select[@title='Change the year']"
select_month_xpath = "//div[@class='datepick-month-header']/select[@title='Change the month']"
no_data_xpath = "//*[@id='tblBhavCopy']/tbody/tr/td[text()='Data not available.']"

for date in date_range:
    # print('###', df['Dates'][i], df['Clicks'][i], df['Downloaded'][i], i)
    #print(len(date), date, date[:4], dates.months(date[5:7]), int(date[8:10]))

    time.sleep(1)
    datepick = browser.find_element_by_id('txtDate')
    datepick.click()
    time.sleep(0.3)

    select_year = Select(browser.find_element_by_xpath(select_year_xpath))
    year, month = date[:4], dates.months(date[5:7])

    date_xpath = "//div[@class='datepick-month']/table/tbody/tr/td/a[text()='{}']".format(str(int(date[8:10])))
    select_year.select_by_visible_text(year)
    select_month = Select(browser.find_element_by_xpath(select_month_xpath))
    select_month.select_by_visible_text(month)
    select_date = browser.find_element_by_xpath(date_xpath)
    select_date.click()

    show = browser.find_element_by_id('btnShowDatewise')
    show.click()
    time.sleep(2)

    try:
        no_data = browser.find_element_by_xpath(no_data_xpath)
        print('No data for {}'.format(date))
    except selenium.common.exceptions.NoSuchElementException:
        download = browser.find_element_by_id('cph_InnerContainerRight_C001_lnkExpToCSV')
        download.click()
        print('Downloading data for {}'.format(date))


print('Download complete')

time.sleep(2)

browser.quit()



