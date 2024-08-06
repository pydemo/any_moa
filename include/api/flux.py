import requests
import tempfile
from PIL import Image
from os.path import basename, join, dirname, exists
import fal_client
import os
import subprocess
import platform
import time

prompt = """



the head of putin in a suit has fire on it, in the style of layered imagery , creative commons attribution, diana f+, haunting figuratism,


"""

model = 'fal-ai/flux/schnell'


def download_image(img_url):
    r = requests.get(img_url)
    desktop_path = join(os.path.expanduser('~'), 'Desktop')
    os.makedirs(desktop_path, exist_ok=True)
    fn = join(desktop_path, f'generated_image_{basename(tempfile.mktemp())}.png')
    with open(fn, 'wb') as f:
        f.write(r.content)
    return fn

def generate_images(prompt):
    handler = fal_client.submit(
        "fal-ai/flux/dev",
        arguments={
            "prompt": prompt,
            "image_size": "portrait_16_9",
            "num_images": 1,
            "enable_safety_checker": False,
            "num_inference_steps": 28,
            "guidance_scale": 3.5,
        },
    )
    result = handler.get()
    return result

import subprocess
import platform
import time
import pyperclip

def open_image(file_path):
    if not exists(file_path):
        print(f"Error: File not found at {file_path}")
        return False

    system = platform.system()
    try:
        if system == 'Windows':
            # Copy the file path to clipboard
            original_clipboard = pyperclip.paste()

            pyperclip.copy(file_path)
            
            # Open a new command prompt
            subprocess.Popen('start cmd', shell=True)
            
            # Wait for the command prompt to open
            time.sleep(.5)
            
            # Simulate pressing Ctrl+V (paste) and Enter
            from pywinauto.keyboard import send_keys
            send_keys('^v{ENTER}')
            pyperclip.copy(original_clipboard)
        else:
            print(f"Unsupported operating system: {system}")
            return False
        
        return True
    except Exception as e:
        print(f"Error opening image: {e}")
        return False

if __name__ == "__main__":
    result = generate_images(prompt)
    
    for img in result['images']:
        img_url = img['url']
        fn = download_image(img_url)
        
        print(f"Image saved at: {fn}")
        
        if open_image(fn):
            print("Image opened successfully. Please check your image viewer.")
            if 0:
                # Wait for user confirmation
                input("Press Enter to continue...")
                
 
        else:
            print("Failed to open the image. Please check the saved location and try to open it manually.")

    