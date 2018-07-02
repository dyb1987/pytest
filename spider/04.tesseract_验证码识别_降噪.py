import pytesseract
from PIL import Image #导入 python image 库

image_file = r"d:\os\bank_card.jpg"
new_img_file = r"d:\os\bank_card_new.jpg"
img_steam = Image.open(image_file)
