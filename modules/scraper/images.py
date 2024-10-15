import requests
from bs4 import BeautifulSoup
import base64
from io import BytesIO
from PIL import Image
from bing_image_downloader import downloader
import os


def get_car_base64(car_name: str) -> str:
    output_dir = os.path.join('temp_img')
    
    downloader.download(car_name, limit=1, output_dir=output_dir, adult_filter_off=False, force_replace=False, timeout=10, verbose=True)
    
    output_dir = os.path.join('temp_img', car_name)
    # get first image from the folder
    first_image = os.listdir(output_dir)[0]

    # Open the image and convert to base64
    with open(os.path.join(output_dir, first_image), "rb") as image_file:
        img_base64 = base64.b64encode(image_file.read())
        
    def remove_all(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                remove_all(item_path)
        os.rmdir(directory)

    # Clean up - remove folder and all images inside
    remove_all(output_dir)
    
    return img_base64

if __name__ == "__main__":
    base64_img = get_car_base64("Tesla Model 3")
    # show the image
    img = Image.open(BytesIO(base64.b64decode(base64_img)))
    img.show()