# Shoppingcart backend
This is a simple backend made with Flask framework, Python and Postgres database. The purpose of this backend is to serve REST API service to frontend made with React. There are six different endpoints i.e for getting all products from db. With Postman set headers content/type:application/json and use `GET` method.
> http://127.0.0.1:5000/api/allproducts

To edit certain product by id use `PUT` method. Content body can be as follows:

```
{
    "product_name": "Soldering iron",
    "description": "Solder whatever you want. Warning: Soldering head may be hot.",
    "price": 9999,
    "availability": "In stock",
    "image_link": "https://cdn.pixabay.com/photo/2015/11/11/12/24/soldering-iron-1038540_960_720.jpg",
    "condition": "New",
    "brand": "Beepboop"
}
```
The endpoint is as follows:
> http://127.0.0.1:5000/api/edit/id

To delete product by id from store use `DELETE` method:
> http://127.0.0.1:5000/api/deleteproduct/id

To add product in the store, use `POST` method:
> http://127.0.0.1:5000/api/add

example body:

```
{
    "product_name": "Soldering iron",
    "description": "Solder whatever you want. Warning: Soldering head may be hot.",
    "price": 23.50,
    "availability": "In stock",
    "image_link": "https://cdn.pixabay.com/photo/2015/11/11/12/24/soldering-iron-1038540_960_720.jpg",
    "condition": "New",
    "brand": "Torcher"
}
```

To get current shoppingcart, use `GET` method:
> http://127.0.0.1:5000/api/shoppingcart

In order to add product in the shoppingcart use `POST` method:
> http://127.0.0.1:5000/api/shoppingcart

To test this you can post the following in the above address with Postman:

```
{
    "id": 7,
    "count": 1
}
```

In order to get a single product by id, use `GET` methon:
> http://127.0.0.1:5000/api/getproduct/id

## Update Python and install Pip, Venv
In order to update Python on your Linux machine open terminal and enter the following lines into Linux terminal window.

To update your local package index:
> sudo apt-get update

To upgrade the packages installed on your machine:
> sudo apt-get -y upgrade

To check your installed Python version:
> python3 -V

To install Pip (Python package manager):
> sudo apt-get install -y python3-pip

Install Venv with this command:
> sudo apt install -y python3-venv

# Create Python virtual environment 
Now that all the previous has been done make new virtual environment. Open terminal and go to documents folder or where you want to set up the virtual environment.
> cd Documents

Create new folder for the environment
>mkdir foldername

>cd foldername

In the folder enter the following:
>python3 -m venv environment_name_here

# Install and run Flask, SQLAlchemy & Psycopg2 in virtual environment
After creating the virtual environment, activate the environment by entering the following command:
>source my_environment/bin/activate

After activation install Flask, SQLAlchemy and Psycopg2
>pip install Flask

>pip install SQLAlchemy

>pip install psycopg2


In the terminal find folder src and in the folder app.py file. You can run the app.py by entering the following command in terminal:
>python3 app.py

or

>flask run

After you don't need venv anymore deactivate it by typing the following in terminal:
>deactivate