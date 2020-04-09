""" Function to delete, rename and store images. """


from os import path, remove, rename
from string import Template
from PIL import Image
from flask import current_app


def change_image(image, folder, new_url, old_url):
    """ Save new image. If an old URL is given, the images named
    after that URL must be deleted. If the image is None, old images
    must be renamed. If the new URL is None, images must be replaced. """
    if image is not None:  # new image has been uploaded
        if new_url is None:  # replace images
            store_image(image, folder, old_url)
        else:  # remove images with old name and create ones with new name.
            store_image(image, folder, new_url)
            delete_image(folder, old_url)
    else:  # rename images
        rename_image(folder, old_url, new_url)


def store_image(image, folder, name):
    """ Stores images in the filesystem, optionally in
    different sizes. """
    folders = dict()  # image location and thumbnail size
    img = Image.open(image)
    if folder == 'recipes':
        folders = {  
            'recipes/large': None,
            'recipes/600': (600, 600),
            'recipes/300': (300, 300)
        }
        mark = Image.open(path.join(
            current_app.root_path, 'static/images/icons/syp_circle.png'
        ))
        mark.thumbnail((250, 250))
        img.paste(mark, (30, 30), mark)
        img = img.convert('RGB')
    elif folder == 'users':
        folders = {'users': None}
    for key in folders:
        if folders[key] is not None:
            img.thumbnail(folders[key])
        img.save(
            path.join(
                current_app.root_path,
                f'static/images/{key}/{name}.jpg'
            ), optimize=True, progressive=True
        )


def delete_image(name, folder):
    folders = list()  # image location
    if folder == 'recipes':
        folders = ['recipes/large', 'recipes/600', 'recipes/300']
    elif folder == 'users':
        folders = ['users']
    for f in folders:
        try:
            remove(path.join(
                current_app.root_path, f'static/images/{f}/{name}.jpg'
            ))
        except FileNotFoundError:
            continue


def rename_image(folder, src, dst):
    folders = list()  # image location
    if folder == 'recipes':
        folders = ['recipes/large', 'recipes/600', 'recipes/300']
    elif folder == 'users':
        folders = ['users']
    common_path = Template(path.join(
        current_app.root_path, 'static/images/$dir'
    ))
    for f in folders:
        rename(
            common_path.substitute(dir=f'{f}/{src}.jpg'),
            common_path.substitute(dir=f'{f}/{dst}.jpg')
        )
