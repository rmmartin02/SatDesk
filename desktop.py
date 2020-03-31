import urllib.request
from PIL import Image
from datetime import datetime, timedelta
import os

# Increate max pixel limit for PILLOW
Image.MAX_IMAGE_PIXELS = 117679104 + 1

# Download the file from `url` and save it locally under `file_name`:
imageDir = os.path.join('.', 'images')
finalImageDir = os.path.join('.', 'finalImages')
goes16 = 'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/10848x10848.jpg'
goes17 = 'https://cdn.star.nesdis.noaa.gov/GOES17/ABI/FD/GEOCOLOR/10848x10848.jpg'

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
time = str(utc-timedelta(minutes=10))[11:15].replace(':', '')+'000'
him = 'http://rammb-slider.cira.colostate.edu/data/imagery/{}/himawari---full_disk/geocolor/{}{}/'.format(date,date,time)

print(datetime.utcnow())
count = 0
while count < 100:
        try:
                response = urllib.request.urlretrieve(him+lower_right, os.path.join(imageDir, 'him-8_lr.png'))
                print("Found him8 image at ", him)
                break
        except:
                utc = utc-timedelta(minutes=10)
                utc_str = str(utc)
                date = utc_str[:10].replace('-','')
                time = utc_str[11:15].replace(':','')+'000'
                time = str(utc-timedelta(minutes=10))[11:15].replace(':','')+'000'
                him = 'http://rammb-slider.cira.colostate.edu/data/imagery/{}/himawari---full_disk/geocolor/{}{}/'.format(date,date,time)
                count += 1
print('Downloading GOES images')
urllib.request.urlretrieve(goes16, os.path.join(finalImageDir, 'goes16.png'))
urllib.request.urlretrieve(goes17, os.path.join(finalImageDir, 'goes17.png'))
# Already go lr earlier ^
print('Downloading HIM8 images')
urllib.request.urlretrieve(him+lower_left, os.path.join(imageDir, 'him-8_ll.png'))
urllib.request.urlretrieve(him+upper_left, os.path.join(imageDir, 'him-8_ul.png'))
urllib.request.urlretrieve(him+upper_right, os.path.join(imageDir, 'him-8_ur.png'))

print("Merging HIM8 images")
image_ul = Image.open(os.path.join(imageDir, 'him-8_ul.png'))
image_ur = Image.open(os.path.join(imageDir, 'him-8_ur.png'))
image_ll = Image.open(os.path.join(imageDir, 'him-8_ll.png'))
image_lr = Image.open(os.path.join(imageDir, 'him-8_lr.png'))

(width, height) = image_ul.size

result_width = width*2
result_height = height*2

him8_image = Image.new('RGB', (result_width, result_height))
him8_image.paste(im=image_ul, box=(0, 0))
him8_image.paste(im=image_ur, box=(width, 0))
him8_image.paste(im=image_ll, box=(0, height))
him8_image.paste(im=image_lr, box=(width, height))
him8_image.save(os.path.join(finalImageDir, 'him8.png'))

print("Resizing images")
image1 = Image.open(os.path.join(finalImageDir, 'goes16.png'))
image2 = Image.open(os.path.join(finalImageDir, 'him8.png'))
image3 = Image.open(os.path.join(finalImageDir, 'goes17.png'))

height = 2160
width = 3840

image1 = image1.resize((int(width/2), height), Image.NEAREST)
image2 = image2.resize((int(width/2), height), Image.NEAREST)
image3 = image3.resize((int(width/2), height), Image.NEAREST)

print("Creating him8_goes16")
result = Image.new('RGB', (width, height))
result.paste(im=image2, box=(0, 0))
result.paste(im=image1, box=(int(width/2), 0))
result.save(os.path.join(finalImageDir, 'him8_goes16.png'))

print("Creating goes16_goes17.png")
result = Image.new('RGB', (width, height))
result.paste(im=image3, box=(0, 0))
result.paste(im=image1, box=(int(width/2), 0))
result.save(os.path.join(finalImageDir, 'goes16_goes17.png'))
