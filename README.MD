# Project Description 
This team project teaches us how to setup Pycharm with Docker, Flask, and MySQL using csv data.
Once our data was setup, we developed the following two features:
1. Add a chart from chart.js to incorporate our api data from the json endpoints. 
2. Create a login and registration process that includes email verification from SendGrid. 

Installation Instructions for Using the App with Docker:
1. Make sure you have docker desktop installed in your computer. 

Setting Up Code & Running it: 
Add a .env file under App directory after downloading the repository. 
The .env file will need one variable called SENDGRID_API in order for flask app to function. 


EMail Login/Registration Process: 
Registration - Indicate your email and password. 
Once a username and password are entered, then you will be redirected to the homepage. 
You will also receive an email to the registered address indicating registration is complete. 
Login - Using the same email and password, - login to the account. 
Once logged in, you will be redirected to the homepage. 
During Registration and Login process, the server will validate your input and send back error messages if information is incorrect. 
Please observe network tab in your browser for any error messages. 
