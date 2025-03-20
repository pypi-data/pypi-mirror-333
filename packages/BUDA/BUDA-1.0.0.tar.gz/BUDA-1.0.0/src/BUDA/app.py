from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def main(verbosity="INFO", host="127.0.0.1", port:int=9875):

    # Create the Flask app
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize the database
    db.init_app(app)

    # Resets all narratives on app startup.
    from .models.narrative import Narrative
    with app.app_context():
        db.create_all()
        db.session.query(Narrative).update({Narrative.is_running: False})
        db.session.commit()

    # Register Blueprints
    from .routes.root import root_bp
    app.register_blueprint(root_bp, url_prefix='/')

    from .routes.context import context_bp
    app.register_blueprint(context_bp, url_prefix='/context')

    from .routes.narratives import narratives_bp
    app.register_blueprint(narratives_bp, url_prefix='/narratives')
    
    from .routes.user_profiles import user_profiles_bp
    app.register_blueprint(user_profiles_bp, url_prefix='/user_profiles')

    from .routes.activities import activities_bp
    app.register_blueprint(activities_bp, url_prefix='/activities')

    from .routes.narrative_review import narrative_review_bp
    app.register_blueprint(narrative_review_bp, url_prefix='/narrative_review')

    from .routes.statistics import statistics_bp
    app.register_blueprint(statistics_bp, url_prefix='/statistics')
    
    from .routes.ai_integration import ai_bp
    app.register_blueprint(ai_bp, url_prefix='/ai')

    from .routes.settings import settings_bp
    app.register_blueprint(settings_bp, url_prefix='/settings')
    
    return app

