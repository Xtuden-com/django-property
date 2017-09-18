Django Property
===============

Django base website for estate agents using Django, PostGis, Postgres etc

This will be a continuing open sourced project (see license below) that I use
to learn more Django

To install download and place inside virtualenv running Python 2.7

Config
----

Depends on environment variables as follows:

* DATABASE_URL
* DJANGO_SETTINGS_MODULE
* SECRET_KEY
* AWS_STORAGE_BUCKET_NAME
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* GOOGLE_MAPS_API_KEY
* EMAIL_HOST
* EMAIL_HOST_USER
* EMAIL_HOST_PASSWORD
* EMAIL_PORT
* DEFAULT_FROM_EMAIL
* DO_NOT_REPLY_EMAIL
* RECAPTCHA_SITE_KEY
* RECAPTCHA_SECRET_KEY
* RECAPTCHA_VERIFICATION_URL

Of the above DJANGO_SETTINGS_MODULE needs to be set to whichever
settings file you are using for the site e.g. config.settings.local
for local development, config.settings.production for production. 
They all inherit from config.settings.base

DATABASE_URL would be in the form of postgres://[user]:[pass]@[host]:[port]/[database]

GOOGLE_MAPS_API_KEY you need to register with Google and give permission
for Geocoder API as well as Javascript Maps

The AWS_* settings need to map to a bucket IAM user to upload
images etc as the site uses remote hosting for these

The EMAIL_* settings relate to sending email 

The DEFAULT_FROM_EMAIL is the default email address used if you don't provide another in Django

The DO_NOT_REPLY_EMAIL is and address used for for emails you don't want
people to reply to.

The RECAPTCHA_* keys relate to site and secret keys and verification URL from Recaptcha and are 
used to protect contact forms

Styles etc
-----

All stylesheets and templates are in the homes_themes_default
app. System uses NPM / Yarn for package management.

Styles are VERY basic atm in this default theme. Uses Bootstrap 4.0.0 beta
Idea of theming just copy the homes_themes_default app and hack away at
the templates / styles etc.

To run the build process for styles / js etc check the package.json file.
There are 5 scripts therein...

**npm run build**
Full rebuild (JS/CSS etc) and runs collect static and uploads to S3
bucket

**npm run static**
Runs django collect static command and sends to S3 bucket

**npm run styles**
Runs rebuild of CSS and uploads to S3 bucket

**npm run server**
Runs the Django server

**npm run test**
Runs tests against the JS components using jest

Currently there are tests against some of the JS components using Jest.

Getting it running
----

To install git clone repo into your virtualenv and when downloaded and all environment
variables set you can run pip install -r requirements.txt to install
the required Python modules

Once this succeeds then you can run ./manage.py migrate to install
the database tables etc

Once this is complete just ./manage.py runserver and visit 127.0.0.1:8000 and it should be running.

Fixtures
----
There is some fixtures data to populate site initially in the fixtures directories inside each app. Load
using the ./manage.py loaddata --app=[app name] [fixture path]

Tests
----
Django tests can be run using ./manage.py test
There are currently 103 tests 

What next
----
As said, work in progress. The following are next...

* Additional tests for JS components already built
* Tests for notification emailer and alert emailer
* Add pages for estate agent / branches listing property
* Add some captcha and additional protection on contact form
* +++

License
----
MIT License

Copyright (c) 2017 Robert Coster

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.