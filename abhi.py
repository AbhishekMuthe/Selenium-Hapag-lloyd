from selenium import webdriver
from time import sleep
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import json

# from bson import json_util
#input_date = now.strftime("%Y%m%d")
#now = datetime.now()

def get_schedule(driver, input_date, results=[], origin='INNSA', destination='BEANR'):
    sleep(2)
    accept = driver.find_element_by_id("accept-recommended-btn-handler")
    accept.click()
    sleep(2)
    driver.maximize_window()
    driver.execute_script("window.scrollTo(0, 1000)")
    start_input = driver.find_element_by_id("schedules_interactive_f:hl19")
    start_input.send_keys("INNSA")
    sleep(2)
    start_loc = driver.find_element_by_class_name("combo-name")
    start_loc.click()
    end_input = driver.find_element_by_id("schedules_interactive_f:hl62")
    end_input.send_keys("BEANR")
    sleep(2)
    end_loc = driver.find_element_by_id("ext-gen297")
    # end_loc = driver.find_element_by_class_name("combo-full-address")
    sleep(2)
    end_loc.click()
    sleep(2)
    dob = driver.find_element_by_id("schedules_interactive_f:hl29")
    dob.send_keys(input_date)
    find = driver.find_element_by_id('schedules_interactive_f:hl116')
    find.click()
    sleep(2)
    sel = Selector(text=driver.page_source)
    port_loading = sel.xpath('//tr/td[3]/span/text()').extract()
    port_discharge = sel.xpath('//tr/td[6]/span/text()').extract()
    transit_days = sel.xpath('//*[@id="schedules_interactive_f:hl135"]/tbody/tr/td[7]/span/text()').extract()
    count = 0
    for i in range(0, len(port_loading)-2, 2):
        yyyy, mm, dd = port_loading[i+1].split("-")
        yyyy1, mm1, dd1 = port_discharge[i+1].split("-")
        a = {"origin_port": port_loading[i],
              "destination_port": port_discharge[i],
              "etd": datetime(int(yyyy), int(mm), int(dd), 0, 0, 0, 0),
              "eta": datetime(int(yyyy1), int(mm1), int(dd1), 0, 0, 0, 0),
              "transit_days": transit_days[int(i/2)]}
        results.append(a)
        count+=1
    return results, count
def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__() 
    
def results_to_json(results, count):
    a = {"results": results,
        "total_results": count}
    return a
    
def main():
    driver = webdriver.Chrome('C:/users/HP/Desktop/chromedriver.exe')
    driver.get('https://www.hapag-lloyd.com/en/online-business/schedule/interactive-schedule/interactive-schedule-solution.html')
    now = datetime.now()
    date = now.strftime("%Y%m%d")
    results, count = get_schedule(driver=driver, input_date=date)
    json_data = results_to_json(results, count)
    with open("abhi.json", "w") as write_file:
        json.dump(json_data, write_file, default = myconverter)
    print("Done writing JSON data into .json file")
    
if(__name__ == '__main__'):
    main()

        
        