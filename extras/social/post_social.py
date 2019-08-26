"""
Posts a recipe in Facebook and Instagram.
3 Posts per recipe:
    1. Image with Intro
    2. Video (as long as possible)
    3. Pepper icon with health paragraph
"""

from fb import post_facebook
from insta import post_photo, delete_last


def get_text(name, intro, link):
    return f"¡Tenemos una nueva receta! {name} \n\n{intro} \n\n{link}"


def post_both(text, img):
    post_facebook(text, img)
    # post_photo(text, img)


if __name__ == '__main__':
    name = "Ñoquis de batata con pesto de tomate"
    intro = "Estos ñoquis son más sabrosos y saludables que los \
             tradicionales de patata. Si os gustan los ñoquis del \
             super, ¡esta receta casera os va a saber mucho mejor!"
    link = "https://www.saludypimienta.com"
    img = "noquis_de_batata_con_pesto_de_tomate_opt.jpg"
    text = get_text(name, intro, link)
    post_both(text, img)
