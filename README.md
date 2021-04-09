# Handle Checker
## A script to check the availability of random words as twitter handles without using Twitter's public API.


## Setup instructions
### Install the required PyPI packages;
`pip install selenium random-word opencv-python pytesseract`

---

### Download the webdriver

You must have the correct webdriver for your browser for selenium to work.

For example, I'm using firefox, so I'll need the Gecko webdriver.

Refer to the table [here](https://selenium-python.readthedocs.io/installation.html#drivers) for your browser of choice.

I found it was hit or miss adding the webdriver to `PATH`, so I recommend just sticking it in the same directory as `main.py`. It works just the same.
If you're on Windows, the webdriver should just be an `exe` file.

Next, change the `options.binary_location` line in `main.py` to reflect the path to your firefox executable. I'm using this to force selenium to run with the developer edition of firefox.

---

### Install Tesseract-OCR

For tesseract, refer to the documentation [here](https://tesseract-ocr.github.io/tessdoc/#binaries). For simplicity, I recommend using the pre-compiled binaries.

If you're on Windows, download the correct `exe` and go through the installation process. If you leave things as default, the path to your tesseract executable should be `C:\Program Files\Tesseract-OCR\tesseract.exe`.

It will be under `Program Files (x86)` if you chose to download the 32 bit (`x32`) file from the github page.
You'll also need to change the `pytesseract.pytesseract.tesseract_cmd` line in `main.py` accordingly if you've done so.

---

## Extra notes
If you have a particularly slow internet connection, you might find the page isn't fully loading before the screenshot is taken. In that case, just increse the wait time at the top of `CheckWord()`.

Likewise, you might be able to lower this number too. I designed this script to be left running overnight, and so I'd rather it take an extra second or two just to make sure it doesn't break if the network speed dips.

If you're really bothered, see [here](https://stackoverflow.com/a/26567563) and [here](https://selenium-python.readthedocs.io/waits.html), and use `By.CLASS_NAME` instead of `By.ID`, because as far as I know there aren't ID's on the divs in question on Twitter. Also, from my experience the class names are obfuscated, but don't change from session to session.
