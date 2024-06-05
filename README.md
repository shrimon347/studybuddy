### This is the note sharing website which is build upon the django framework 

# Introduction

This is the project of my 8tth semester of my university. In this project we can share our note with my friends and other any part of the world here we include the room system and included real chat system with the payment system .
### Home page
![note_share website](https://github.com/shrimon347/studybuddy/blob/master/image/homepage.PNG?raw=true)
### Main features

* User friendly ui/ux

* Custom user model 

* Included the room and real time chat system

* User registration and logging 

* Upload the note and also updated the note

* Separated requirements files
 
* Blog write in blog here user comment and also like the blog
  
* stripe payment system
  
* authication using github and google
  
* SQLite by default if no env variable is set
  
* serching system and also admin approved included the blog and note which upload by the user


### Room page
![note_share website](https://github.com/shrimon347/studybuddy/blob/master/image/rooms.PNGraw=true)
### Blog page
![note_share website](https://github.com/shrimon347/studybuddy/blob/master/image/blogs.PNG?raw=true)
### blog Details page
![note_share website](https://github.com/shrimon347/studybuddy/blob/master/image/blog%20detail.PNG?raw=true)
### Login page
![note_share website](https://github.com/shrimon347/studybuddy/blob/master/image/login.PNG?raw=true)
### User profile page
![note_share website](https://github.com/shrimon347/studybuddy/blob/master/image/profilepage.PNG?raw=true)



# Usage

To use this template to start your own project:

### Existing virtualenv

If your project is already in an existing python3 virtualenv first install django by running

    $ pip install django
    
And then run the `django-admin.py` command to start the new project:

    $ django-admin.py studybudy \
      --template=https://github.com/shrimon347/share-me-note/tree/master
      --extension=py,md \
      <project_name>
      
### No virtualenv

This assumes that `python3` is linked to valid installation of python 3 and that `pip` is installed and `pip3`is valid
for installing python 3 packages.

Installing inside virtualenv is recommended, however you can start your project without virtualenv too.

If you don't have django installed for python 3 then run:

    $ pip install django
if you don't have a virtualenv then follow the steps

    $ pip install pipenv
 And then:
 
    $ pipenv install django
 And then activate the virtualenv as follows :
 
    $ pipenv shell
    
And then:

    $ python3 -m django studybudy \
      --template=https://github.com/shrimon347/share-me-note/tree/master \
      --extension=py,md \
      <project_name>
      
      
After that just install the local dependencies, run migrations, and start the server.


# {{ project_name|title }}

# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com/USERNAME/{{ project_name }}.git
    $ cd {{ project_name }}
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements/local.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver
    
🙏 If you find this repo helpful then don't forget to give a start ❇️ to this repository. :)
