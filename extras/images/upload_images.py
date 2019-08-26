"""
This script gets the images of the 'images' folder and resizes them into three
    sizes, all optimized and saved as progressive .jpg in different folders:
        Original, 600px, 300px
It also puts a watermark on the upper left corner before it begins to shrink
    the images.
These images can then be sent to the EC2 server hosting the website, and saved
    in their respective folders with the shell script 'upload_photos.sh',
    which is located in the 'ec2' folder.
The folders will be deleted and created again before saving new images, so
    that no duplicates are saved.

** Bug: folders have to be re-created manually.
"""

from PIL import Image
import os
import shutil


def upload(rotate=False):

    print("Deleting and re-creating folders...")

    shutil.rmtree('large_opt')
    os.mkdir('large_opt')
    shutil.rmtree('600_opt')
    os.mkdir('600_opt')
    shutil.rmtree('300_opt')
    os.mkdir('300_opt')
    print('Folders re-created.')

    print("Optimizing images...")

    # Open watermark as thumbnail
    mark = Image.open('watermark.png')
    mark.thumbnail((250, 250))
    print("Watermark loaded.")

    # Iterate over images in 'images folder'
    for f in os.listdir('images'):
        print(f"Found image '{f}'.")
        f_name, f_ext = os.path.splitext(f)
        img = Image.open(f'images/{f}')
        if rotate:
            img = img.rotate(90, expand=True)

        img.paste(mark, (30, 30), mark)  # watermark (PNG image)
        img = img.convert('RGB')  # convert back to JPEG

        # save optimized and progressive image in original size with '_opt' end
        img.save(f'large_opt/{f_name}_opt.jpg', optimize=True,
                 progressive=True)

        # save optimized and progressive image in 600px size with '_opt' ending
        img.thumbnail((600, 600))
        img.save(f'600_opt/{f_name}_600_opt.jpg', optimize=True,
                 progressive=True)

        # save optimized and progressive image in 300px size with '_opt' ending
        img.thumbnail((300, 300))
        img.save(f'300_opt/{f_name}_300_opt.jpg', optimize=True,
                 progressive=True)

        print(f"Image {f} optimized and saved in three different sizes.")

    print("All images have been opimized and saved.")

    """
    print("Calling shell script to upload photos...")
    subprocess.call(['/home/charlo/docs/code/ec2/upload_photos.sh'])
    print("Script terminated. Bye!")
    """


if __name__ == "__main__":
    upload()
