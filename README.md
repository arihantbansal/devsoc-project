# Scheddy - Your Scheduling ally!

Scheddy helps you schedule meetings without the back-and-forth emails.

### *Schedule time with anyone.* 

-   Get clear visibility.
-   Quickly discover who’s available
-   Skip the email games. No more back-and-forth emails.
-   Stay in control. With Scheddy, you invite people to choose one of your proposed times.
### Getting started

1.  Clone this repo:  `git clone git@github.com:arihantbansal/devsoc-project.git`
2.  Change to the repo directory:  `cd devsoc-project`
3. Make a virtual environment for your project as 
`mkvirtualenv venv`. If you have already made a virtual environment, then activate it using `workon venv` 
4. Install dependencies with pip:  `pip install -r requirements.txt`
5. Specify the Flask application by: `export FLASK_APP=application.py` (on Unix) or `set FLASK_APP=application.py` (on Windows)
6. Finally run the application by: `python -m flask run` or simply `flask run`

### Features

The landing page of the website gives a brief introduction about our team and the features of our website.

New users have to click on “Register” and enter their username and password that they wish to use in the website.

Once registered, the users can simply “Log In” to the website using their username and password. 

After logging in, the page displays whether the user already has a meeting time slot scheduled. 

The users have to then enter their preferred time slot.

The “Start Time” must be earlier than the “End Time”, else an error message pops up. 

Once you have set your time slot, you are good to go.

Now enter the username of the person who want to have a meeting with. The website will automatically find the common time when both of the users are free. Now feel free to start a GMeet and chat with your friends.

An error message will pop in case the username you enter does not exist. So, ask your friends to login with their real names
