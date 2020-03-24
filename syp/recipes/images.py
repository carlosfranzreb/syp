""" Function to delete, rename and store images. """


from os import path, remove, rename
from string import Template
from PIL import Image
from flask import current_app


def change_image(image, new_url, old_url):
    """ Save new image. If an old URL is given, the images named
    after that URL must be deleted. If the image is None, old images
    must be renamed. If the new URL is None, images must be replaced. """
    if image is not None:  # new image has been uploaded
        if new_url is None:  # replace images
            store_image(image, old_url)
        else:  # remove images with old name and create ones with new name.
            store_image(image, new_url)
            delete_image(old_url)
    else:  # rename images
        rename_image(old_url, new_url)


def store_image(image, name):
    mark = Image.open(
        path.join(current_app.root_path, 'static/images/icons/syp_circle.png')
    )
    mark.thumbnail((250, 250))
    img = Image.open(image)
    img.paste(mark, (30, 30), mark)
    img = img.convert('RGB')
    for folder in ('large', '600', '300'):
        img.save(
            path.join(
                current_app.root_path,
                f'static/images/recipes/{folder}/{name}.jpg'
            ), optimize=True, progressive=True
        )


def delete_image(name):
    for folder in ['large', '600', '300']:
        remove(path.join(
            current_app.root_path,
            f'static/images/recipes/{folder}/{name}.jpg'
        ))


def rename_image(src, dst):
    common_path = Template(path.join(
        current_app.root_path, 'static/images/recipes/$dir'
    ))
    for folder in ['large', '600', '300']:
        rename(
            common_path.substitute(dir=f'{folder}/{src}.jpg'),
            common_path.substitute(dir=f'{folder}/{dst}.jpg')
        )
