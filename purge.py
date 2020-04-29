import time
import csv
import sys
from selenium import webdriver
from selenium.webdriver.support.select import Select

def purgeFunTest(arg):
    try:
        success = "Done Purging"
        return success
    except:
        error = "Something Went Wrong"
        return error
    finally:
        print("run onces")


def purgeFun(arg):
    try:
        #List
        LinkDict = {
            #Define List of ULR here
        }
        print(LinkDict.keys())
        print(arg)
        #which = input("Enter the Applicaion Name: ")
        test=LinkDict.get(arg)
        print(test[0],",",test[1])

        driver = webdriver.Chrome('chromedriver')
        driver.set_window_position(-10000,0)
        #Enter URL Here
        driver.get('URL')
        #Enter Credentials
        username=driver.find_element_by_id('Username')
        username.send_keys("email")
        password=driver.find_element_by_id('Password')
        password.send_keys("password")
        password.submit()
        #Redriect to Another page
        driver.get('Another Page for Purge')
        time.sleep(7)
        driver.get('Another Page for Purge')
        time.sleep(3)
        print("Now Purging")
        #Auto 1
        driver.find_element_by_partial_link_text('Bulk').click()
        bulk=driver.find_element_by_name('bulkPaths')
        #Enter the URL one by one
        bulk.send_keys(test[0])

        #To CLick
        driver.find_element_by_xpath('//*[@id="purgeFormBody"]/div/div/div[1]/cache-manager-form/div/div/div[5]/div[1]/ng-form/div/div[1]/a').click()

        time.sleep(3)

        #Auto 2
        #driver.find_element_by_partial_link_text('Bulk').click()
        bulk=driver.find_element_by_name('bulkPaths')
        bulk.send_keys(test[1])

        #To CLick
        driver.find_element_by_xpath('//*[@id="purgeFormBody"]/div/div/div[1]/cache-manager-form/div/div/div[5]/div[1]/ng-form/div/div[1]/a').click()
    
        print("Done Purging")
        success = "Done Purging"
        return success

    except:
        error = "Something Went Wrong"
        return error

    finally:
        print("run onces")