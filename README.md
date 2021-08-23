# django-notebook

Based off of Christos Stathakis' tutorial "Create a Notebook with Django"
https://christosstath10.medium.com/create-a-notebook-with-django-f25c28db2643

Added more/different features to mimic Microsoft OneNote.

Running example on Python Anywhere:
http://tmanwarren.pythonanywhere.com/

## Installation

Create a folder on your computer then clone this repo with this command:

```bash
git clone https://github.com/TysonManwarren/django-notebook.git
#Next
cd django-notebook
```
I used pipenv to create a virtual environment, so you install pipenv globally on your computer:
```bash
pip install pipenv
```

Create a new virtual environment:
```bash
pipenv shell
```

Next, install required packages stored in the ``Pipfile.lock`` file using the ``sync`` command.
```bash
pipenv sync
```

After that, you run your migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

Finally, run the app
```bash
python manage.py runserver
```