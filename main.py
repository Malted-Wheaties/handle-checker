# Generate random word > Navigate to twitter page -> Screenshot -> Detect "profile not found" text in screenshot -> if valid username add to txt file

"""
TODO
Re-evauluate variable naming
Rewrite some comments for clarity & consistency
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from random_word import RandomWords
import os
import time
import cv2
import pytesseract


options = Options()
options.binary_location = "C:/Program Files/Firefox Developer Edition/firefox.exe"
driver = webdriver.Firefox(options=options)

r = RandomWords()

# The installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"


def CheckWord():
    # Return a single random word
    random_word = r.get_random_word()

    # Uses the current firefox instance to navigate to the twitter profile
    driver.get("http://twitter.com/" + random_word)

    # Wait for page to load
    time.sleep(5)
        
    # Screenshot page
    file_path = str(time.time()) + ".png" # A dedicated folder isn't necessary as the image is getting deleted immidiately
    driver.get_screenshot_as_file(file_path)


    # Read image from which text needs to be extracted
    img = cv2.imread(file_path)

    # Delete the image from the fs
    os.remove(file_path)

    # Preprocessing the image starts
  
    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    """
    Specify structure shape and kernel size. 
    Kernel size increases or decreases the area of the rectangle to be detected.
    A smaller value like (10, 10) will detect each word instead of a sentence.
    """
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
  
    # Appplying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
  
    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, 
                                                 cv2.CHAIN_APPROX_NONE)
    # Creating a copy of image
    im2 = img.copy()
  
    """
    Looping through the identified contours
    Then rectangular part is cropped and passed on to pytesseract for extracting text from it
    """
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
      
        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
      
        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]
      
        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)

        if text is None or text == "":
            print("Detected text was null or empty >:(")
            return

        if "This account doesn" in text:
            print("Available: " + random_word)
            f = open("valid handles.txt", "a+")
            f.write(random_word + "\n")
            f.close()
        else:
            print("Taken: " + random_word)


while True:
    CheckWord()
        
