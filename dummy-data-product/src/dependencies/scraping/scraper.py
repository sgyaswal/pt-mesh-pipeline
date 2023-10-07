
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import json
import os
import pandas as pd

class Scraper:
    def __init__(self):
        with open('./config.json') as file:
            data = json.load(file)
        self.driver_path = '/home/sagar/Downloads/project/pt-mesh-pipeline/build/chromedriver'
        self.headless = data['headless']
        self.inprivate = data['private']
        self.output_name = data['output_csv']
        self.start_ind = data['start_ind']
        self.end_ind = data['end_ind']
        self.clearFlag = False
        
    
    def __countList(self, lst1, lst2):
        result = [None]*(len(lst1)+len(lst2))
        result[::2] = lst1
        result[1::2] = lst2
        return result
    
    def __cell_finder(self, tab):
        return tab.find_elements(By.CSS_SELECTOR,'.td_caption'), tab.find_elements(By.CSS_SELECTOR,'.td_field')
    
    def __dir_maker(self):
        try:
            os.mkdir('../../data')
        except FileExistsError:
            pass
    
    def __clear_dir(self):
        try:
            if self.output_name.endswith('.csv'):
                try:
                    os.remove('../../data/' + self.output_name)
                except FileNotFoundError:
                    pass
                finally:
                    self.clearFlag = True
            else:
                self.output_name += '.csv'
                try:
                    os.remove('../../../data/' + self.output_name)
                except FileNotFoundError:
                    pass
                finally:
                    self.clearFlag = True
        except PermissionError:
            print('Unable to remove the file: ' + self.output_name)
            print('Remove this file to proceed')
    
    def crawler(self):
        self.__dir_maker()
        self.__clear_dir()
        if self.clearFlag:
            options = Options()
            if self.headless:
                options.add_argument("--headless=new")    # headless mode
            if self.inprivate:
                options.add_argument('inprivate')    # inprivate mode
                
            options.add_argument('--log-level=1')    # to remove Permission Policy Header Errors
            browser = webdriver.Chrome(executable_path=self.driver_path,options=options)    # using Microsoft Edge Webdriver

            browser.get('https://etenders.gov.in/eprocure/app')    # root URL of the website to be scraped

            next_page1 = browser.find_element(By.ID,"PageLink_0")    # navigating to the required webpage
            next_page1.click()

            containers1_even = browser.find_elements(By.CLASS_NAME, 'even')
            containers1_odd = browser.find_elements(By.CLASS_NAME, 'odd')
            org_elements = self.__countList(containers1_even,containers1_odd)    # all the organisation elements
            
            if self.end_ind > len(org_elements)-1:
                self.end_ind = len(org_elements)
            if self.start_ind > self.end_ind:
                print('Start Index should be less than End Index')
                return
            if self.start_ind > len(org_elements)-1:
                self.start_ind = len(org_elements)-1

            data_list = []

            # for j in range(len(org_elements)):
            for j in range(self.start_ind,self.end_ind):
                org_element = org_elements[j]    # current organisation element
                org_name = org_element.find_elements(By.TAG_NAME,'td')[1].text    # current organisation name
                tender_count = int(org_element.find_elements(By.TAG_NAME,'td')[-1].text)    # current organisation tenders

                current_org_link = org_element.find_element(By.CLASS_NAME,'link2').get_attribute('href')    # getting next link and opening it in new tab
                browser.execute_script("window.open('');")
                browser.switch_to.window(browser.window_handles[1])
                browser.get(current_org_link)

                containers2_even = browser.find_elements(By.CLASS_NAME, 'even')
                containers2_odd = browser.find_elements(By.CLASS_NAME, 'odd')
                tender_elements = self.__countList(containers2_even,containers2_odd)    # all the tender elements

                for i in tqdm(range(len(tender_elements)), desc=org_name):
                    row_dict = {'Organisation Name':org_name,'Number of Tenders':tender_count,

                                'Organisation Chain':None,'Tender Reference Number':None,'Tender ID':None,
                                'Withdrawal Allowed':None,'Tender Type':None,'Form Of Contract':None,
                                'General Technical Evaluation Allowed':None,'ItemWise Technical Evaluation Allowed':None,
                                'Payment Mode':None,'Is Multi Currency Allowed For BOQ':None,
                                'Is Multi Currency Allowed For Fee':None,'Allow Two Stage Bidding':None,'Tender Category':None,
                                'No. of Covers':None,

                                'Tender Fee in ₹':None,'Fee Payable To':None,'Fee Payable At':None,
                                'Tender Fee Exemption Allowed':None,

                                'EMD Amount in ₹':None,'EMD through BG/ST or EMD Exemption Allowed':None,
                                'EMD Fee Type':None,'EMD Percentage':None,'EMD Payable To':None,'EMD Payable At':None,

                                'Title':None,'Work Description':None,'NDA/Pre Qualification':None,'Independent External Monitor/Remarks':None,
                                'Tender Value in ₹':None,'Product Category':None,'Sub category':None,'Contract Type':None,
                                'Bid Validity(Days)':None,'Period Of Work(Days)':None,'Location':None,'Pincode':None,
                                'Pre Bid Meeting Place':None,'Pre Bid Meeting Address':None,'Pre Bid Meeting Date':None,
                                'Bid Opening Place':None,'Should Allow NDA Tender':None,'Allow Preferential Bidder':None,

                                'Published Date':None,'Bid Opening Date':None,'Document Download / Sale Start Date':None,
                                'Document Download / Sale End Date':None,'Clarification Start Date':None,
                                'Clarification End Date':None,'Bid Submission Start Date':None,'Bid Submission End Date':None,

                                'Name':None,'Address':None}    # data for one row

                    current_tender_link = tender_elements[i].find_element(By.TAG_NAME, 'a').get_attribute('href')    # getting next link and opening it in new tab
                    browser.execute_script("window.open('');")
                    browser.switch_to.window(browser.window_handles[-1])
                    browser.get(current_tender_link)

                    content = browser.find_elements(By.CLASS_NAME,'tablebg')    # whole content
                    for i in content:    # identifying required tables
                        if i.find_element(By.CSS_SELECTOR,'tbody>tr>td').text == 'Organisation Chain':
                            tab1 = i.find_element(By.CSS_SELECTOR,'tbody')
                        elif i.find_element(By.CSS_SELECTOR,'tbody>tr>td').text == 'Tender Fee in ₹':
                            tab4 = i.find_element(By.CSS_SELECTOR,'tbody')
                        elif i.find_element(By.CSS_SELECTOR,'tbody>tr>td').text == 'EMD Amount in ₹':
                            tab5 = i.find_element(By.CSS_SELECTOR,'tbody')
                        elif i.find_element(By.CSS_SELECTOR,'tbody>tr>td').text == 'Title':
                            tab6 = i.find_element(By.CSS_SELECTOR,'tbody')
                        elif i.find_element(By.CSS_SELECTOR,'tbody>tr>td').text == 'Published Date':
                            tab7 = i.find_element(By.CSS_SELECTOR,'tbody')
                        elif i.find_element(By.CSS_SELECTOR,'tbody>tr>td').text == 'Name':
                            tab9 = i.find_element(By.CSS_SELECTOR,'tbody')


                    cells_key_element,cells_val_element = self.__cell_finder(tab1)
                    for key,val in zip(cells_key_element,cells_val_element):
                        row_dict[key.text] = val.text

                    cells_key_element,cells_val_element = self.__cell_finder(tab4)
                    for key,val in zip(cells_key_element,cells_val_element):
                        row_dict[key.text] = val.text

                    cells_key_element,cells_val_element = self.__cell_finder(tab5)
                    for key,val in zip(cells_key_element,cells_val_element):
                        row_dict[key.text] = val.text

                    cells_key_element,cells_val_element = self.__cell_finder(tab6)
                    for key,val in zip(cells_key_element,cells_val_element):

                        row_dict[key.text] = val.text

                    cells_key_element,cells_val_element = self.__cell_finder(tab7)
                    for key,val in zip(cells_key_element,cells_val_element):
                        row_dict[key.text] = val.text

                    cells_key_element,cells_val_element = self.__cell_finder(tab9)
                    for key,val in zip(cells_key_element,cells_val_element):
                        row_dict[key.text] = val.text

                    data_list.append(row_dict)  # Append the data to the list

                    browser.close()    # closing the tender data tab
                    browser.switch_to.window(browser.window_handles[1])
                browser.close()    # closing the organisation data tab
                browser.switch_to.window(browser.window_handles[0])
            browser.quit()    # closing the scraper window

            # Create a pandas DataFrame from the data_list
            df = pd.DataFrame(data_list)

            # Save the DataFrame to a CSV file
            df.to_csv('../../data/' + self.output_name, sep='\t', index=False, encoding="utf-16")

