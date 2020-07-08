# Ecommerce-Django
This is an Ecommerce website created in Django 3. 

1.	Create a new directory.

2.	Do a git clone for this project.

3.  Create a virtual environment by typing the below two commands,

    >	 pip install virtualenv

    >	virtualenv venv  
4.  Run the requirements.txt file as follows,
  
    >  pip install -r requirements.txt

5.	Once all the modules are installed. Create a random secret Key and add the secret key in a secrets.py file which should be  
    in the same directory as setting.py
    Example:
    KEY="ABC123"

6.	Apply all the migrations by running the below command,
 
    > python manage.py migrate


7.	Run the server by entering below command,
 
    > python manage.py runserver

6. The above command will run a local webserver on port 8000. Open your browser and type
localhost:8000
