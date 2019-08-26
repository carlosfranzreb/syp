"""
Posts photo of recipe and intro in Instagram
"""


from InstagramAPI import InstagramAPI as api


def post_photo(photo, caption):
    path = '/home/charlo/docs/code/www/flask-syp/extras/images/instagram'
    photo_path = f'{path}/{photo}'

    ig = api("saludypimienta", "w$41opM7")
    ig.login()
    ig.uploadPhoto(photo_path, caption=caption)


def delete_last():
    ig = api("saludypimienta", "w$41opM7")
    ig.login()
    ig.getSelfUserFeed()
    media = ig.LastJson['items'][-1]
    if ig.deleteMedia(media['id']):
        print("Media has been deleted")
    else:
        print("Media has not been deleted. Fuck off.")
