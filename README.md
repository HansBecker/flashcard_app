# Flashcard app
Simple flashcard app for practicing flashcards. The application is written in Django. The main application code is located 
in the `main` directory. The unit tests can be found in `main/tests/test_views.py`.

## Setup a Python environment
I use `pipenv` for creating a virtual environment. This application 
is written for Python 3.9 

1. Check if `pipenv` is installed by running `pipenv --version`, if it returns a
version number, great! Otherwise install by running `pip install pipenv`
2. Navigate the terminal to the top level `ShortURL` directory containing `manage.py`
3. Start a pipenv with `pipenv shell`
4. Install the requirements with `pipenv install -r requirements.txt`
5. You can exit or close the newly created virtual environment with `exit`. 

## Starting the application
To start the application

1. Start the virtual environment with `pipenv shell`
2. Create the database with `python manage.py migrate`
3. Start the application with `python manage.py runserver`

## Creating a superuser
1. Start the virtual environment with `pipenv shell`
2. Run `python manage.py createsuperuser`
3. Follow the prompts to create a new superuser

## Running the tests
The tests
1. Start the virtual environment with `pipenv shell`
   1. Sometimes the virtual environment needs to be restarted to make
    sure pytest can recognize all installed packages. The virtual 
   environment can be exited with `exit` while in the virtual environment.
2. Run the tests with `pytest`