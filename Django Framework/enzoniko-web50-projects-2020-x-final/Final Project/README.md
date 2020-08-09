# Final project

Web programming with Python and JavaScript

https://youtu.be/xc8pGjEtkg4

This project is a rental system for sports courts in django.
In addition to python, I used bootstrap 4 to better control all DOM elements.

index.hmlt login.html signin.html menu.html extends the layout.html file
models.py contains all data structures
urls.py contains routes to functions
views.py cotain main program and functions that renders html files

Also in the static folder, there are the pictures and styles.css files that contain additional html style, in addition to all the pre-created bootstrap and jquery css and js files.

The program automatically creates a superuser account at the first start (admin, adminadmin)

Basically, the program allows users to create an account and then it shows some information about the site (60% of the money received is destined for cancer hospitals, so by renting these sports courts, you are helping a good cause ).
The user can rent periods (from 8 am to 12 pm / 2 pm to 6 pm / 8 pm - 12 pm) in one of our sports courts, being able to choose the date he would like to schedule (the program only allows dates from the day after 1 month after the current date). If this is the user's first rental, the program will ask for your CPF (ID) and save it in the database for other rentals. The program also adds the possibility of writing other people's CPFs (in case the user who paid for it cannot go). After payment, the user will receive a QR code in the email he registered when logging in.
This QR code will act as a key to enter the rented area (but this project does not cover this) (we also assume that security guards will understand if one of the users is the owner of the CPFs written on the website). But if, for some reason, the user needs to cancel the rental, the program implements an easy-to-use cancellation mechanism, the user will only need to write the ID that appears in the QR code, the application will check if that ID matches the user's rental and then it will be deleted from the database.
The website is responsive to mobile devices, easy to use and beautiful.
The final idea is to use a QR code reader connected to a microcontroller that opens and closes the door so that everything is automated and more of the money received can be donated.

How to use:

-Download the project source file (Final Project folder);

-set your enviroment variables for security:
    (in linux)
    
    -nano ~/.bash_profile
    -export EMAIL_ADDRESS="THE EMAIL THAT WILL SEND THE QR CODES"
    -export EMAIL_PASS="PASSWORD OF THE EMAIL ABOVE"


-In the NEXT RENT APP folder:

    -pip3 install -r requirements.txt
    -python3 manage.py makemigrations
    -python3 manage.py migrate
    -python3 manage.py runserver
    
-In the RENT API folder:

    -cd agenda_me
    -pip3 install -r requirements.txt
    -python3 manage.py makemigrations
    -python3 manage.py migrate
    -python3 manage.py runserver 7000
    
-After that you should be able to enter my final project website with the link that django give in the terminal from the NEXT RENT APP folder.

    

    
