# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from filters import first_letter ,thisisthat_worldwide ,thisisthat_remote , time_since ,check_compensation
# from .scheduler import scheduler  # Import the scheduler setup

# db = SQLAlchemy()


# def create_app():
#     app = Flask(__name__ ,template_folder='templates')
#     app.jinja_env.filters['first_letter'] = first_letter
#     app.jinja_env.filters['thisisthat_worldwide'] = thisisthat_worldwide
#     app.jinja_env.filters['thisisthat_remote'] = thisisthat_remote   
#     app.jinja_env.filters['time_since'] = time_since   
#     app.jinja_env.filters['check_compensation'] = check_compensation   
#     # print(first_word("Test Company Name"))  # Should print "Test"
#     # print(app.jinja_env.filters)  # Should include 'first_word'
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./jobboard.db' 
#     db.init_app(app)
    
#     from routes import register_routes
#     register_routes(app,db)

#     migrate = Migrate(app,db)
#     return app
# app.py
from flask import Flask
from flask_migrate import Migrate
from filters import first_letter, thisisthat_worldwide, thisisthat_remote, time_since, check_compensation
from extensions import db, scheduler  # Import from extensions
from scheduler import delete_old_rows  # Import the delete function if needed in the scheduler

def create_app():
    app = Flask(__name__, template_folder='templates')

    # Add custom Jinja filters
    app.jinja_env.filters['first_letter'] = first_letter
    app.jinja_env.filters['thisisthat_worldwide'] = thisisthat_worldwide
    app.jinja_env.filters['thisisthat_remote'] = thisisthat_remote   
    app.jinja_env.filters['time_since'] = time_since   
    app.jinja_env.filters['check_compensation'] = check_compensation   

    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./jobboard.db'
    db.init_app(app)
    
    # Register routes
    from routes import register_routes
    register_routes(app, db)

    # Initialize migration
    migrate = Migrate(app, db)

    # Initialize and start the scheduler
    scheduler.init_app(app)
    scheduler.start()

    return app
