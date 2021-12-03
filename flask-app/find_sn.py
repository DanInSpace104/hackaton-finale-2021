
import cv2
import re
import pytesseract

def scan_img(image):
	config = r'--oem 3 --psm 6'
	return pytesseract.image_to_string(image, config=config)

def get_digit(s):
    sn_list = list()
    while s.find("69")>-1:
        i = s.find("69")
        num = s[i:i+8]
        sn_list.append(num)
        s = s[i+8:len(s)]  
    return sn_list

def get_sn_carriage(image):
    return get_digit(scan_img(image))

if __name__=='__main__':
    img = cv2.imread('text.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print(get_sn_carriage(img))