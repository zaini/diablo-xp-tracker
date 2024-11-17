import cv2
import pyautogui
import numpy as np
import pytesseract
import keyboard
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class DialogDimensions:
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height


DIALOG_DIMENSIONS = DialogDimensions(1050, 1150, 400, 90)


class ExpTracker:
    def __init__(self) -> None:
        pass

    def start(self, exp):
        self.start_time = time.time() * 1000
        self.start_exp = exp

    def end(self, exp):
        self.end_time = time.time() * 1000
        self.end_exp = exp

    def __str__(self):
        if (self.end_time < self.start_time):
            return 'You must end your current tracker before you can get the current status. Press CTRL+2.'
        time_elapsed_in_ms = self.end_time - self.start_time
        exp_change = self.end_exp - self.start_exp
        exp_per_ms = exp_change / time_elapsed_in_ms
        exp_per_hour = exp_per_ms * 3600000
        return f'Start Exp: {self.start_exp:,}\nEnd Exp: {self.end_exp:,}\nTime Elapsed (hh:mm:ss): {convert_ms_to_hms(time_elapsed_in_ms)}\nExp Per Hour: {round(exp_per_hour):,}'


EXP_TRACKER = ExpTracker()


def convert_ms_to_hms(milliseconds):
    seconds = int((milliseconds / 1000) % 60)
    minutes = int((milliseconds / (1000 * 60)) % 60)
    hours = int((milliseconds / (1000 * 60 * 60)) % 24)

    time_format = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    return time_format


def take_screenshot(x, y, width, height):
    # Get the screen dimensions
    screen_width, screen_height = pyautogui.size()

    # Ensure the provided coordinates are within the screen bounds
    if x < 0 or y < 0 or width < 0 or height < 0:
        print("Invalid coordinates!")
        return

    if x + width > screen_width or y + height > screen_height:
        print("Coordinates out of screen bounds!")
        return

    # Capture the screen
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to a numpy array
    screenshot = np.array(screenshot)

    # Convert color space from RGB to BGR
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # Crop the screenshot to the specified region
    cropped_image = screenshot[y:y + height, x:x + width]
    return cropped_image


def extract_text_from_image(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply image preprocessing, if needed (e.g., thresholding, denoising)

    # Perform OCR using pytesseract
    extracted_text = pytesseract.image_to_string(gray_image)

    return extracted_text


def getCurrentExp():
    # Call the function to extract text from the image
    extracted_text = extract_text_from_image(take_screenshot(DIALOG_DIMENSIONS.x, DIALOG_DIMENSIONS.y, DIALOG_DIMENSIONS.width, DIALOG_DIMENSIONS.height)
                                             )
    try:
        return int(extracted_text.split(" ")[3].replace(",", ""))
    except:
        return 0


def on_start_count():
    exp = getCurrentExp()
    print(f'Start Exp: {exp:,}\n')
    EXP_TRACKER.start(exp)


def on_end_count():
    exp = getCurrentExp()
    print(f'End Exp: {exp:,}\n')
    EXP_TRACKER.end(exp)
    print(EXP_TRACKER)


def on_output_tracker():
    print(EXP_TRACKER)


def on_define_screen_size():
    # Capture the screen
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to a numpy array
    screenshot = np.array(screenshot)

    # Convert color space from RGB to BGR
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    roi = cv2.selectROI(
        "Select the region of the image with only the EXP popup dialog", screenshot)
    DIALOG_DIMENSIONS.x, DIALOG_DIMENSIONS.y, DIALOG_DIMENSIONS.width, DIALOG_DIMENSIONS.height = roi
    print("New region:", roi)
    cv2.imwrite("exp-region-screenshot.png", screenshot[DIALOG_DIMENSIONS.y:DIALOG_DIMENSIONS.y +
                DIALOG_DIMENSIONS.height, DIALOG_DIMENSIONS.x:DIALOG_DIMENSIONS.x + DIALOG_DIMENSIONS.width])
    cv2.destroyAllWindows()


if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+0", on_define_screen_size)

    keyboard.add_hotkey("ctrl+1", on_start_count)

    keyboard.add_hotkey("ctrl+2", on_end_count)

    keyboard.add_hotkey("ctrl+3", on_output_tracker)

    # Keep the script running until interrupted
    keyboard.wait()
