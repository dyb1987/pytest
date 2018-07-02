import pytesseract
from PIL import Image #导入 python image 库

image_file = r"d:\os\2.png"
img_steam = Image.open(image_file)

img_data = pytesseract.image_to_string(img_steam,lang="chi_sim")
print(img_data.replace("\ ",""))
