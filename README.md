# Introduction
In this project, we have picked iPhoneX as our product for the analysis. We have gathered user’s tweets since February and have performed Sentiment Analysis and Summarization on them. This project covers user’s feedback about the new features and price of the iPhone X.

**Note: The application is hosted on a cloud server and can be accessed with the URL http://82x.rahulb.me**

# System Requirements
 - System with Windows, Linux or Mac (preferably a cloud machine)
 - Anaconda 5.0 or later (downloadable from https://www.anaconda.com/download/#macos)
 - Python packages:
    - NLTK (https://www.nltk.org/)
    - Django (https://www.djangoproject.com/)
    - Pymongo (https://api.mongodb.com/python/current/)
    - Djongo (not the same as Django) (https://github.com/nesdis/djongo)
    - Twython (https://twython.readthedocs.io/en/latest/)
    - Pandas (https://pandas.pydata.org/)
    - Requests (http://docs.python-requests.org/en/master/)

# Setup Instructions
- Setup the cloud machine with Linux
- Install Anaconda - See following webpages for the installation instruction
    - Windows (https://docs.anaconda.com/anaconda/install/windows)
    - MacOS (https://docs.anaconda.com/anaconda/install/mac-os)
    - Linux (https://docs.anaconda.com/anaconda/install/linux.html)
- Create a conda environment `conda create --name eight2x`
- Activate the conda environment `conda activate eight2x`
- Install the required Python packages in the conda environment
    `
    conda install -c anaconda nltk 
    conda install -c anaconda django 
    conda install -c anaconda pandas 
    conda install -c anaconda requests 
    conda install -c anaconda pymongo 
    conda install -c conda-forge twython 
    pip install djongo
    `
- Install and Setup MongoDB. See following webpages for the installation instruction
    - Linux (https://docs.mongodb.com/manual/administration/install-on-linux/)
    - MacOS (https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
    - Windows (https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)
- Run following command to import the database of tweets
    `mongorestore -d 82x database`
- Extract the project folder in at a particular location
- Modify the database configuration
- To run the application in the developer mode `python manage.py runserver`

# Jobs to read Tweets
There are several jobs that can be configured (but not mandatory to run only once) to read tweets and run models. The command to setup those jobs on a Linux or Mac system are
- Read Tweet Stream - `nohup python manage.py twitter_stream &`
- Estimate Tweet Country - `nohup python manage.py predict_country &`
- Sentiment Analysis - `nohup python manage.py predict_sentiment &`
- Predict Labels - `nohup python manage.py predict_label &`

# Project Structure
- eight2x: Project level configuration of the Django app
    - settings.py: consists of global settings like the API key used by all apps inside this project
    - urls.py: defines the routes of this projects. The default path leads to eight2x_app application
    - wsgi.py: defines the config to run application with Apache HTTP mod_wsgi (reference: https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/modwsgi/)

- eight2x_app: Main application
    - dataset: contains model training dataset. Only for sentiment classification, external dataset has been used, for other models manually labeled data is prepared in the database
    - lib: supporting classes and functions used by the application
    - management: contains the command line commands which can be executed as `python manage.py <command file name without .py>`
    - migrations: migrations to create the database structure
    - templates: defines the UI templates
    - admin.py: not used by the application
    - apps.py: Application specific configuration
    - models.py: models defined in the application
    - urls.py: routing URLs of this application
    - views.py: controllers defined in the application
- static: folder for the static files