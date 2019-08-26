class Config:
    SECRET_KEY = '5731628xx0b13ce0c696dfdefuwba945'
    mysql = 'mysql+pymysql://syp_admin:w$41opM7@localhost/db_syp'
    SQLALCHEMY_DATABASE_URI = mysql
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'carlosfranzreb@gmail.com'
    MAIL_PASSWORD = 'w$41opM7'
    RECAPTCHA_PUBLIC_KEY = '6LcEZo4UAAAAAEr4grJz9agEzBe7iIf4B-JPRItk'
    RECAPTCHA_PRIVATE_KEY = '6LcEZo4UAAAAANOn-mO-NbUwrT75zJ_gZ25CYwg5'
