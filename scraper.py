import time
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pandas import DataFrame

PATH = "C:/Program Files (x86)/chromedriver.exe"
signed = False

def get_jobs(keyword, num_jobs, verbose):
    url = f"https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&typedLocation=&locT=&locId=&jobType=&context=Jobs&sc.keyword={keyword}"

    jobs = []
    driver = webdriver.Chrome(PATH)
    driver.get(url)

    def removeSignIn():
        global signed

        if not signed:
            driver.implicitly_wait(5)
            try:
                driver.find_element(By.CLASS_NAME, "modal_closeIcon").click()
                signed = True
            except NoSuchElementException:
                pass
        
        removeSurvey()
        
    def removeSurvey():
        try:
            driver.find_element(By.CLASS_NAME, "delighted-web-survey-close-btn").click()
            signed = True
        except NoSuchElementException:
            pass
        
    def getValue(name):
        value = ""
        try:
            value = driver.find_element(By.CLASS_NAME, name).text
        except NoSuchElementException:
            pass
        except StaleElementReferenceException:
            pass

        return value

    def nextPage():
        try:
            driver.find_element(By.CLASS_NAME, "css-1yshuyv").find_element(By.CLASS_NAME, "SVGInline").click()
            time.sleep(5)
        except NoSuchElementException:
            print(f"Scraping terminated before reaching target number of jobs. Needed {num_jobs}, got {len(jobs)}.")

    while len(jobs) < num_jobs:
        removeSignIn()

        page_jobs = driver.find_elements_by_class_name("react-job-listing")
        print(len(page_jobs))

        for j in page_jobs:
            print(f"Progress: {str(len(jobs)+1)} / {str(num_jobs)}")

            if(len(jobs) >= num_jobs):
                break

            removeSignIn()
            j.click()
            time.sleep(1)

            data = {}
            data["company name"] = getValue("css-87uc0g").split('\n')[0]
            data["job title"] = getValue("css-1vg6q84")
            data["location"] = getValue("css-56kyx5")
            data["salary"] = getValue("css-16kxj2j")

            try:
                for c in driver.find_elements(By.CLASS_NAME, "css-rmzuhb"):
                    text = c.text
                    # data[c.text.split('\n')[0]] = c.text.split('\n')[1]           
            except NoSuchElementException:
                pass

            jobs.append(data)
            if verbose:
                print(data)

        nextPage()

    driver.quit()
    return DataFrame(jobs)