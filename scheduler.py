# scheduler.py
from extensions import db, scheduler
from models import Job
from datetime import datetime, timedelta

def delete_old_rows():
    thirty_days_ago = datetime.now(datetime.timezone.utc) - timedelta(days=30)
    Job.query.filter(Job.created_at < thirty_days_ago).delete()
    db.session.commit()

@scheduler.task('interval', id='delete_old_rows', hours=24)
def scheduled_task():
    from app import create_app  # Import the app to access the app context
    app = create_app()
    with app.app_context():
        delete_old_rows()
