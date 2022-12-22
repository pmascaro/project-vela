# project-vela

Named after the Vela constellation, this app aims to provide users with detailed travel information tailored to the user needs harnessing state-of-the-art technology. Let's make our journeys as smooth and enjoyable as possible.

TODO - visualise journey in a map
TODO - create user interaction and solve issue with token
TODO - deploy via web app

### Creating the project

##### Creating venv

This sections is based on the following youtube tutorial: 
https://www.youtube.com/watch?v=brJR5Qjp4SM

and https://bobbyhadz.com/blog/source-is-not-recognized-as-internal-or-external-command

In the terminal, use: python -m venv venv

This creates the virtual environment and now we need to activate it. To do so, use:

if you use windows use the following: venv\Scripts\activate.bat

Aside note: remember that 'chdir' command prints the path in the terminal

To deactivate it, simply type: deactivate

Note: To check for interpreter, use 'python'

Now it's time to install all your required libraries, which you can do as you require them. Also, you can check (here)[https://towardsdatascience.com/how-to-use-bash-to-automate-the-boring-stuff-for-data-science-d447cd23fffe] if you want to install them in one go

At the end of the process, use this in the terminal:

pip freeze > requirements.txt

You can always create another virtual environment, you can always copy all the requirements from the requirements.txt file:

pip install -r requirements.txt