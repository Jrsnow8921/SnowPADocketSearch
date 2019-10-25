from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import selenium.common.exceptions as slex
import os
import requests
import subprocess
import time
import PyPDF2 
import substring
import urllib3, shutil



class SnowDocketScrMJ:

  def __init__(self, driver = None):
    self.driver = webdriver.Chrome()

  def run(self):
    self.driver.set_window_position(-10000,0)
    self.driver.implicitly_wait(20)
    self.driver.get("https://ujsportal.pacourts.us/DocketSheets/MDJ.aspx")

    ignored_exceptions=(slex.NoSuchElementException,slex.StaleElementReferenceException) 
    element_wait = WebDriverWait(self.driver, 10,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.ID, "ctl00_ctl00_ctl00_cphMain_cphDynamicContent_ddlSearchType")))
    element = self.driver.find_element_by_xpath("//select[@id='ctl00_ctl00_ctl00_cphMain_cphDynamicContent_ddlSearchType']")
    all_options = element.find_elements_by_tag_name("option")
    options_list = list()
    for option in all_options:
      options_list.append(option.get_attribute("value"))


    dropdown = Select(element) 
    element.click()
    dropdown_select = dropdown.select_by_value("ParticipantName")
    time.sleep(1)


    county_element = self.driver.find_element_by_xpath("//select[@id='ctl00_ctl00_ctl00_cphMain_cphDynamicContent_cphSearchControls_udsParticipantName_ddlCounty']")


    all_options = county_element.find_elements_by_tag_name("option")
    options_list = list()
    for option in all_options:
      options_list.append(option.get_attribute("value"))


    dropdown_county = Select(county_element)
    county_element.click()
    print options_list
    dropdown_county_select = dropdown_county.select_by_value(str(raw_input("Enter A Valid County From The List Above: ")))

    last_name = self.driver.find_element_by_xpath("//input[@id='ctl00_ctl00_ctl00_cphMain_cphDynamicContent_cphSearchControls_udsParticipantName_txtLastName']")
    last_name.send_keys(str(raw_input("Enter Last Name: ")))

    first_name = self.driver.find_element_by_xpath("//input[@id='ctl00_ctl00_ctl00_cphMain_cphDynamicContent_cphSearchControls_udsParticipantName_txtFirstName']")
    first_name.send_keys(str(raw_input("Enter First Name: ")))

    self.driver.find_element_by_id("ctl00_ctl00_ctl00_cphMain_cphDynamicContent_btnSearch").send_keys(Keys.ENTER)
    time.sleep(2)

    b = self.driver.find_element_by_id("ctl00_ctl00_ctl00_cphMain_cphDynamicContent_cphResults_gvDocket")

    links = self.driver.find_elements_by_css_selector("tr a")

    f = []
    mj = []
    for link in links:
      if "https://ujsportal.pacourts.us/DocketSheets/MDJReport.ashx?docketNumber=MJ" in link.get_attribute("href"):
        mj.append(link.get_attribute("href")[71:95])

        f.append(link.get_attribute("href")) 

    #for row in b.find_elements_by_css_selector('tr'):
    #   for cell in row.find_elements_by_tag_name('td'):
    #      if "MJ-" in cell.text:
    #        mj.append(cell.text)
    #print(f)
    #print(mj) 



    for xy, xr in zip(f, mj):
      #print len(xy)
      if not len(xy) >= 131:
        self.downloadFile(xy, xr)
        self.getPDFData(xr + '.pdf')
      else:
        self.downloadFile(xy, 'civil_case')
        self.getPDFData('civil_case' + '.pdf')

  def getPDFData(self, ff):
    pdfFileObj = open(ff, 'rb')

    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    #print(pdfReader.numPages)

    pageObj = pdfReader.getPage(0)

    #print(pageObj.extractText())
    data = pageObj.extractText()
    pdfFileObj.close()

    xj = data[data.find('Name:') + 5:data.find('Sex:')].replace(",", "").replace(" ", "_")
    if len(xj) <= 80:
      if not os.path.exists(xj):
        os.mkdir(xj)
      print ff 
      subprocess.call("mv %s %s" % (ff, xj + "/" + ff), shell=True)
    else:
      xj = 'civil_case'
      if not os.path.exists(xj):
        os.mkdir(xj)
      print ff 
      subprocess.call("mv %s %s" % (ff, xj + "/" + ff), shell=True)



  def downloadFile(self, xy, mj):
    url = xy
    #print(url)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    c = urllib3.PoolManager()
    filename = mj + '.pdf'
    with c.request('GET',url, preload_content=False) as resp, open(filename, 'wb') as out_file:
      shutil.copyfileobj(resp, out_file)
    resp.release_conn()

  def driverClose(self):
    self.driver.close()
    os.system("killall -9 'Google Chrome'")


