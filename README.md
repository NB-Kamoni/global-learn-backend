# Global Learn School Management System - Backend Server

Welcome to the backend server repository for the Global Learn school management system. This server handles database operations and provides endpoints for managing student, teacher, course, and enrollment data.

## Setup and contribution Instructions

### 1. Clone the repo 

```
git clone git@github.com:NB-Kamoni/global-learn-backend.git

cd global-learn-backend

```


### 2. Add upstream remote

```
git remote add upstream git@github.com:NB-Kamoni/global-learn-backend.git

```

### 3. Create new branch


```
git checkout -b <branch-name>

```

### 4. Install Dependencies and Activate Virtual Env

Make sure you have Python and `pipenv` installed. Use `pipenv` to install dependencies.

```
pipenv install
pipenv shell

```

### 5. Set Set Flask Environment Variables

```
cd server
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555

```


### 6. Database Setup and seeding

```
flask db init
flask db migrate -m "Initial migrate"
flask db upgrade head
python seed.py

```

### 7. Run server


```
flask run

```
### 8. stage and commit changes


```
git add .
git commit -m ""

```

### 9. push changes to your branch


```
git push --set-upstream origin <branch name>

```

### 10. After you update the code, create a pull request

Go to the original repository on GitHub. Switch to the branch you just pushed (your branch). Create a pull request with your changes. Select Kelvin as the reviewer

You are done :)

