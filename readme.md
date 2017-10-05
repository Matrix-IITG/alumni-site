# Alumni-site
I have made the accounts feature but still edit_profile needs to be added, some more fields and a better UI.

## Setting up and running
- Install django, preferably 1.10.4.
- Clone the repo using `$ git clone https://github.com/Matrix-IITG/alumni-site.git`
- run `$ python manage.py migrate`
- `$ python manage.py createsuperuser {{any_name}}` //optional, will help in seeing database
- `$ python manage.py runserver`
- Goto https://localhost:8000
- Register a new user.
- Goto https://localhost:8000/admin and login with superuser credentials that you made above in terminal and check users to find the new entry.
