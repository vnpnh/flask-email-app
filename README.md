# Flask Event API


## Requirements
- Python >= 3.10
- Flask >= 3.0.0
- Celery >= 5.2.0
- Redis >= 6.0.0
- Mysql >= 8.0.0

Import postman collection from `docs` folder to test the API.

## Installation

### 1. Clone the repository

```bash
git clone git@github.com:vnpnh/jublia-interview-task.git
```

### 2. Set up a Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the required packages
```bash
pip install -r requirements.txt
```

### 4. Set up the database
```bash
mysql -u root -p
```

```sql
CREATE DATABASE email_app_db;
``` 

### 5. Set up the environment variables
```bash
cp .env.example .env
```

### 6. Run the migrations
```bash
flask db init
flask db migrate
flask db upgrade
```

### 7. Run the application
```bash
flask run
```

### 8. Run celery worker
```bash
celery -A celery_worker worker --loglevel=info --pool=solo
```

### 9. Run celery beat
```bash
celery -A celery_worker.celery beat --loglevel=info
```

Docker
```bash
docker-compose build
docker-compose up
```
