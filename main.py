from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from email.mime.text import MIMEText
import smtplib

class ArgosChecker:
    def __init__(self, productId):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options, executable_path=r'C:\Users\stewa\Documents\Executables\geckodriver.exe')
        self.browser.get(f'https://www.argos.co.uk/product/{productId}')

    def checkStock(self, locationToCheck):
        # self.browser.implicitly_wait(10) #possible cause of the error
        sleep(5)
        
    
        try: 
            self.browser.find_element_by_xpath("//*[@id='consent_prompt_submit']").click()
            print('Cookies accept clicked')
            pass
        except:
            print('there was an error 1')

        try:
            elementToRemove = self.browser.find_element_by_xpath("//div[@class='privacy-prompt-wrapper']") #when using headless browser there is a privacy pop up that causes an error, these two lines remove them
            self.browser.execute_script("arguments[0].style.visibility='hidden'", elementToRemove)
            print('this was attempted')
            pass
        except:
            print('there was an error 2')
        
        print('I made it here')
        locationBox = self.browser.find_element_by_xpath("//input[@placeholder='Postcode or town']")
        locationBox.click()
        locationBox.send_keys(locationToCheck)

        locationBoxSubmit = self.browser.find_element_by_xpath("//button[text()='Check']")
        locationBoxSubmit.click()
        self.browser.implicitly_wait(5)

        lengthOfList = len(self.browser.find_elements_by_xpath("//ol[@data-test='component-store-selector-stores-list']//li"))
        # print(lengthOfList)
        self.List_of_stores_and_stock = []
        for i in range(lengthOfList):
            inStockMessage = self.browser.find_elements_by_css_selector("p[class^='AvailabilityResultstyles__AvailabilityResultHeadingCollectTitle']")[i].text #gets a list of the stock status of each of the stores
            storeName = self.browser.find_elements_by_css_selector("p[class^='AvailabilityResultstyles__StoreDetailsParagraph']")[i].text # gets a list of 10 store names
            singleMessage = storeName +' : '+inStockMessage
            self.List_of_stores_and_stock.append(singleMessage)

        self.browser.quit()

    def notifyMe(self, from_email, from_password, to_email):
        subject="Argos Stock Check"
        
        message="Dear Sir/Madam, <br> Please see the results of the stock checker for the product requested, <br><br>" + ", <br> <br>".join(self.List_of_stores_and_stock) +"<br><br><br> Kind Regards, <br> You, Yourself and Me"

        msg=MIMEText(message, 'html')
        msg['Subject']=subject
        msg['To']=to_email
        msg['From']=from_email
    
        gmail=smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login(from_email, from_password)
        gmail.send_message(msg)

