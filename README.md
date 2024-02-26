# CAPTCHA Solver
This Python script is designed to solve CAPTCHAs using image processing techniques and OCR (Optical Character Recognition). It provides a method to preprocess CAPTCHA images, align letters for better OCR accuracy, and extract text from CAPTCHA images.
It scrape data from thewebsite using Selenium. It automates the process of solving CAPTCHA, entering company details, and downloading the payment details Excel file.


## Functionality
The CAPTCHA solver script performs the following tasks:
1. Preprocesses CAPTCHA images to enhance readability.
2. Aligns letters in CAPTCHA images to improve OCR accuracy.
3. Extracts text from preprocessed CAPTCHA images using OCR.
4. Provides a method to integrate with Selenium for solving CAPTCHAs in web automation tasks.


## Requirements
- Python 3.11 or higher
- Chrome driver
- `requirements.txt` file should be verified before running the code

## Usage
1. Clone the repository.
2. Install the required dependencies from `requirements.txt`.
3. Run the `main.py` file.

## Functionality
The script performs the following tasks:
1. Solves the CAPTCHA automatically using image processing techniques.
   1. Preprocesses CAPTCHA images to enhance readability.
   2. Aligns letters in CAPTCHA images to improve OCR accuracy.
   3. Extracts text from preprocessed CAPTCHA images using OCR.
2. Enters the company name and solves the CAPTCHA on the EPFO website.
3. Navigates to the payment details page and downloads the Excel file containing payment details.

## File Structure
- `main.py`: Main Python script to initiate the scraping process.
- `requirements.txt`: File containing the required Python packages.
- `data/`: Directory where the downloaded Excel file is stored.
- `utils.py`: Helper functions for image processing and CAPTCHA solving.

## How to Run
1. Install the required dependencies using `pip install -r requirements.txt`.
2. Execute `python main.py`.
3. Follow the on-screen instructions.

## Testing
Unit tests are provided to verify the correctness of the scraped data. Run the `test_scrape_data()` function after scraping to ensure data integrity.

## Note
This CAPTCHA solver is designed for learning purposes and should not be used for any illegal or unethical activities. Respect the terms of service of websites and APIs when using CAPTCHA solving techniques.


