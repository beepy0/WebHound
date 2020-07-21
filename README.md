# WebHound

## Setup

### Install
- Libraries: `python -m pip install -r requirements.txt`

### Code Quality
- Test coverage: `run --source='WebHoundApp/' manage.py test WebHoundApp` then `coverage report`
- Run tests separately: `python manage.py test`
- Linter: `flake8 --statistics`

### Run
- Start server: `python manage.py runserver`
- Navigate to `https://127.0.0.1:8000/webhound/trace/`