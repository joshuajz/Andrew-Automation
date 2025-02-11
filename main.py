import requests
from PIL import Image
from io import BytesIO
import json
import os
import shutil

def get_favicon(url, size=256):
    finalURL = f"https://www.google.com/s2/favicons?sz={size}&domain={url}"

    try:
        response = requests.get(finalURL, stream=True, timeout=5)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return False
    return response

def resize_image(image: Image, size, output_file):
    # Open image (Google API should return PNG format)
    

    # Ensure it's resized correctly (only if needed)
    if image.size != size:
        image = image.resize(size, Image.LANCZOS)  # Use LANCZOS for high quality
    
    # Save image
    image.save(output_file, format="PNG")
    print(f"Favicon saved as {output_file}")


def main():
    preURL = input("Website URL: ")
    shortName = input("Short Name: ")
    name = input("Name: ")

    os.makedirs(shortName)

    response = get_favicon(preURL)
    if response == False:
        imageLocation = input("Image Location (Favicon Not Found): ")
        image = Image.open(imageLocation)
    else:
        image = Image.open(BytesIO(response.content))

    resize_image(image, [192, 192], f'{shortName}/logo192.png')
    resize_image(image, [512, 512], f'{shortName}/logo512.png')

    image.save(f'{shortName}/favicon.ico')

    print("Favicons Generated")

    # Load JSON file
    with open("template/manifest.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    # Modify the data (example: add a new key-value pair)
    data['short_name'] = shortName
    data['name'] = name

    print("Data generated:", data)

    # Save modified data to a new file
    with open(f"{shortName}/manifest.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    print("JSON file modified and saved as 'manifest.json'")

    shutil.copyfile(f"template/index.html", f"{shortName}/index.html")
    shutil.copyfile(f"template/robots.txt", f"{shortName}/robots.txt")

    shutil.make_archive(f"{shortName}", "zip", f"{shortName}/")

    print("Created zip file")

    shutil.rmtree(f"{shortName}/")

    print("Deleted working directory")

    print("Finished")




# # Example Usage
# website_url = "https://www.engsoc.queensu.ca/"
# download_and_save_favicon(website_url, "favicon.png")
main()
