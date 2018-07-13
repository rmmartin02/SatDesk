import urllib.request
from PIL import Image
from datetime import datetime,timedelta
from time import sleep

...
# Download the file from `url` and save it locally under `file_name`:
imageDir = './images/'
goes16 = 'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/1808x1808.jpg'

lower_right = '01/001_001.png'
lower_left = '/01/001_000.png'
upper_left = '/01/000_000.png'
upper_right = '/01/000_001.png'
u10minsbefore = '20180712011000/01/001_001.png'
u16hoursbefore = '/imagery/20180711/himawari---full_disk/geocolor/20180711091000/01/001_001.png'

#2018 07 11
#UTC time -1 hour? 24 hour style
#updates every 10 minutes
#2018 07 12 01 10 00

utc = datetime.utcnow()
utc_str = str(utc)
date = utc_str[:10].replace('-','')
time = utc_str[11:15].replace(':','')+'000'
time = str(utc-timedelta(minutes=10))[11:15].replace(':','')+'000'
him = 'http://rammb-slider.cira.colostate.edu/data/imagery/{}/himawari---full_disk/geocolor/{}{}/'.format(date,date,time)

print(datetime.utcnow())
				
while True:
        try:
                response = urllib.request.urlretrieve(him+lower_right, imageDir+'him-8_lr.png')
                break
        except:
                utc = utc-timedelta(minutes=10)
                utc_str = str(utc)
                date = utc_str[:10].replace('-','')
                time = utc_str[11:15].replace(':','')+'000'
                time = str(utc-timedelta(minutes=10))[11:15].replace(':','')+'000'
                him = 'http://rammb-slider.cira.colostate.edu/data/imagery/{}/himawari---full_disk/geocolor/{}{}/'.format(date,date,time)
                print(time)
#print('downloading images')
urllib.request.urlretrieve(goes16, imageDir+'goes16.jpg')
urllib.request.urlretrieve(him+lower_right, imageDir+'him-8_lr.png')
urllib.request.urlretrieve(him+lower_left, imageDir+'him-8_ll.png')
urllib.request.urlretrieve(him+upper_left, imageDir+'him-8_ul.png')
urllib.request.urlretrieve(him+upper_right, imageDir+'him-8_ur.png')

#merge him8 images
image_ul = Image.open(imageDir+'him-8_ul.png')
image_ur = Image.open(imageDir+'him-8_ur.png')
image_ll = Image.open(imageDir+'him-8_ll.png')
image_lr = Image.open(imageDir+'him-8_lr.png')

(width, height) = image_ul.size

result_width = width*2
result_height = height*2

him8_image = Image.new('RGB', (result_width, result_height))
him8_image.paste(im=image_ul, box=(0, 0))
him8_image.paste(im=image_ur, box=(width, 0))
him8_image.paste(im=image_ll, box=(0, height))
him8_image.paste(im=image_lr, box=(width, height))
him8_image.save(imageDir+'him8.jpg')

#resize and merge him8 and goes16 images
image1 = Image.open(imageDir+'goes16.jpg')
image2 = Image.open(imageDir+'him8.jpg')

height = 1080
width = 1920

image1 = image1.resize((int(width/2),height),Image.NEAREST)
image2 = image2.resize((int(width/2),height),Image.NEAREST)

result = Image.new('RGB', (width, height))
result.paste(im=image1, box=(0, 0))
result.paste(im=image2, box=(int(width/2), 0))
result.save(imageDir+'final.bmp')

#change desktop
import ctypes

SPI_SETDESKWALLPAPER = 20
ctypes.windll.user32.SystemParametersInfoW(20, 0, imageDir+'final.bmp', 3)
