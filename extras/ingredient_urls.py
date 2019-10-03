import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Ingredient(Base):
    __tablename__ = 't_ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    url = db.Column(db.String(100), nullable=False, unique=True)
    health = db.Column(db.Text, nullable=False)


    def __repr__(self):
        return f"Ingredient('{self.name}')"


def get_url(name):
    name = name.lower()
    name = name.replace(' ', '_')
    name = name.replace('ñ', 'n')
    name = name.replace('í', 'i')
    name = name.replace('ó', 'o')
    name = name.replace('é', 'e')
    name = name.replace('ú', 'u')
    name = name.replace('á', 'a')
    return name


if __name__ == '__main__':
    engine = db.create_engine(
        'mysql+pymysql://syp_admin:w$41opM7@localhost/db_syp'
    )
    Session = sessionmaker(bind=engine)
    session = Session()
    ingredients = session.query(Ingredient).all()
    for ing in ingredients:
        ing.url = get_url(ing.name)
    session.commit()
