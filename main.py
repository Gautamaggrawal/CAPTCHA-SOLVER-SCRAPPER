'''
Use Python Selenium to scrape data from the EPFO website. Make sure to use the Chrome driver.
Make sure to verify your requirements.txt file before submitting your code. You can use Python 3.11>= for this coding challenge.

Fill out the sections where TODO is written.
Ideally your code should work simply by running the main.py file.

This is a sample file to get you started. Feel free to add any other functions, classes, etc. as you see fit.
This coding challenge is designed to test your ability to write python code and your familiarity with the Selenium library.
This coding challenge is designed to take 2-4 hours and is representative of the kind of work you will be doing at the company daily.
'''

# Importing the required libraries
import os
import pandas as pd
import time
import pytesseract
from PIL import Image
import requests
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cv2
import numpy as np
from selenium.common.exceptions import NoSuchElementException
import uuid
import time

DOWNLOAD_DIR = "data/"

from PIL import Image, ImageFilter
from pytesseract import image_to_string
import cv2
import numpy as np

def preprocess_image_using_pil(image_path):
    img = Image.open(image_path)
    img = img.convert("RGBA")
    pixdata = img.load()
    
    img = img.filter(ImageFilter.SHARPEN)
    img.save("input-black.gif")

    basewidth = 1000
    im_orig = Image.open('input-black.gif')
    # print(im_orig.size[0])
    wpercent = (basewidth / float(im_orig.size[0]))
    hsize = int((float(im_orig.size[1]) * float(wpercent)))
    # print(hsize,wpercent)
    big = im_orig.resize((basewidth, hsize), Image.HAMMING)  # Use Image.LANCZOS for antialiasing

    ext = ".tif"
    tif_file = "input-NEAREST.tif"
    big.save(tif_file)
    
    return tif_file


def align_letters(image_name):
    img = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
    ret, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY_INV)
    Contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    Contours = sorted(Contours, key=lambda x : cv2.boundingRect(x)[0])
    Contours.sort(key=lambda x : cv2.boundingRect(x)[0])
    newImg = np.zeros(img.shape, dtype=np.uint8)
    bb = cv2.boundingRect(Contours[0])
    newY = (bb[1] + bb[3])
    for Contour in Contours:
        [x, y, w, h] = cv2.boundingRect(Contour)

        newImg[newY-h+1:newY+1, x:x+w] = img[y:y+h, x:x+w].copy()
    print(f'aligned-{image_name}','align_letters')
    cv2.imwrite(f"aligned-{image_name}", newImg)

def get_captcha_text_from_captcha_image(captcha_path):
    
    tif_file = preprocess_image_using_pil(captcha_path)
    image = Image.open(tif_file)
    ocr_text = image_to_string(image, config='--psm 9 --oem 3 -c ''tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return(ocr_text)


def solve_captcha(driver, company_name):
    search_box = driver.find_element("id", "estName")
    search_box.clear()
    search_box.send_keys(company_name)
    captcha_img = driver.find_element("id","capImg")
    img_name = 'captcha'
    captcha_ss = driver.find_element("id","capImg").screenshot(f'{img_name}.png')
    align_letters(f'{img_name}.png')
    capcha_text = get_captcha_text_from_captcha_image(f"aligned-{img_name}.png")
    print(capcha_text)
    captcha_input = driver.find_element('xpath','//*[@id="captcha"]')
    captcha_input.send_keys(capcha_text)
    search_btn =  driver.find_element('xpath','//*[@id="searchEmployer"]')
    search_btn.click()

def scrape_data(company_name: str):
    '''
    Scrape data from the EPFO website
    '''
    
    # Create Selenium driver
    options = Options()
    # TODO: Add whatever options you might think are helpful
    prefs = {"download.default_directory" : os.path.join(os.getcwd(), DOWNLOAD_DIR)} # Set the download directory to the data folder
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    # Open the EPFO website
    driver.get('https://unifiedportal-epfo.epfindia.gov.in/publicPortal/no-auth/misReport/home/loadEstSearchHome')

    while True:
        try:
            solve_captcha(driver, company_name)
            time.sleep(2)
            # Check if CAPTCHA is successfully solved (add your own condition here)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(('xpath', '//*[@id="example"]/tbody/tr/td[5]/a[1]'))
            )
            print("CAPTCHA solved successfully!")
            break  # Exit the loop if CAPTCHA is solved
        except Exception as e:
            print("Failed to solve CAPTCHA, retrying...")
            driver.refresh()  # Refresh the page to get a new CAPTCHA

    time.sleep(5)

    # TODO: Fill out the code for the following steps
    # Step 2 - Refer to the sample_output/step_2.png for the screenshot of the page
    # Click on the "View Details" button - you should see an output similar to sample_output/step_2.png
    anchor_element = driver.find_element('xpath','//*[@id="example"]/tbody/tr/td[5]/a[1]')
    
    # Click on the anchor element
    anchor_element.click()
    

    # Click on the "View Payment Details" button that is displayed in sample_output/step_2.png - this opens a new tab
    # view_payment_element = driver.find_element('xpath','//*[@id="tablecontainer3"]/div/a')
    # Click on the anchor element
    view_payment_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(('xpath', '//*[@id="tablecontainer3"]/div/a'))
)
    view_payment_element.click()

    # TODO: Fill out the code for the following steps
    # Step 3 - Refer to the sample_output/step_3.png for the screenshot of the page - this is the new tab that opens up in Step 2
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)
    excel_btn = driver.find_element('xpath','//*[@id="table_pop_up_wrapper"]/div[1]/a')
    time.sleep(1) 
    # Click on the anchor element
    excel_btn.click()


    
    # Click on the "Excel" button - this downloads an excel file in the Downloads folder
    # This should be the final output of the function and should save the excel file in the data folder
    # It should look something like data/Payment Details.xlsx as used in the test_scrape_data() function


def test_scrape_data():
    '''
    Test the scraped data
    '''
    # Convert xlsx file to csv due to some issues with pandas
    from xlsx2csv import Xlsx2csv
    Xlsx2csv("data/Payment Details.xlsx", outputencoding="utf-8").convert("payment_details.csv")

    df = pd.read_csv("payment_details.csv")

    assert set(df.columns) == set(['TRRN', 'Date Of Credit', 'Amount', 'Wage Month', 'No. of Employee', 'ECR'])
    assert df['TRRN'].loc[0] == 3171702000767
    assert df['Date Of Credit'].loc[0] == '03-FEB-2017 14:35:15'
    assert df['Amount'].loc[0] == 334901
    assert df['Wage Month'].loc[0] == 'DEC-16'
    assert df['No. of Employee'].loc[0] == 83
    assert df['ECR'].loc[0] == 'YES'
    print("All tests passed!")

def main():
    print("Hello World!")

    scrape_data("MGH LOGISTICS PVT LTD")

    # TODO: Uncomment the following tests whenever scraping is completed.
    test_scrape_data()
    # TODO: Feel free to add any edge cases which you might think are helpful


if __name__ == "__main__":
    main()