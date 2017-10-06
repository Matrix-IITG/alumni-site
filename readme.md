# Alumni-site
Basic Info site is ready !!
Few Enhancements can be thought of:
- Share Experiences
- Facebook Authentication
- Once FB Oauth cleared take permission to see life events, share life events so everyone is connected.
## Setting up and running
- Install django, preferably 1.10.4.
- Clone the repo using `$ git clone https://github.com/Matrix-IITG/alumni-site.git`
- run `$ python manage.py migrate`
- `$ python manage.py createsuperuser {{any_name}}` //optional, will help in seeing database
- `$ python manage.py runserver`
- Goto https://localhost:8000
- Register a new user.
- Goto https://localhost:8000/admin and login with superuser credentials that you made above in terminal and check users to find the new entry.
