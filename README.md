![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![PyCharm](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)

# eStore

 :placard: Vitrine.Dev |     |
| -------------  | --- |
| :sparkles: Nome        | eStore
| :label: Tecnologias | python, django, postgresql
| :rocket: URL         | 

![Django-Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Django_logo.svg/2560px-Django_logo.svg.png#vitrinedev)

E-Commerce Django Project !

Buy and Sell in your custom made shop !

## **Store View**

![Store-View](https://i.imgur.com/0l4NlvN.png)

## **Product View**

![Django-Product-View](https://i.imgur.com/YLhV0qx.png)

![Other-Product-View](https://i.imgur.com/FKg0gIv.png)

![Shipping](https://i.imgur.com/R8tZ5gG.png)

## **Cart View**
![Cart-View](https://i.imgur.com/UbyUvls.png)

## **Checkout View**
![Checkout-View](https://i.imgur.com/CT6uuRG.png)

# Config
<hr>

- Create an `.env` file in the same folder where `migrate.py` is.
- In your terminal with venv, execute `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` generating a new secret key
- Insert the new secret key in `.env` file like this: `SECRET_KEY = oahsdodjifodjfodjfpadjpajsdpojsd` .
- Insert the database URL in the `.env` file like this: `DATABASE_URL = your_db://your_db:password@localhost/my_db`.
- Run `python manage.py migrate` and create the tables

# Run
<hr>

```sh
python manage.py runserver
```

Server is running in http://127.0.0.1:8000/, access your browser !
 
    



# To-Dos Done:
- Products
- Cart
- Payment
- Checkout