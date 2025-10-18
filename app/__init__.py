from flask import Flask, jsonify
from .extensions import db, migrate, login_manager, cors, socketio
from .config import get_config


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(get_config(config_name))

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    socketio.init_app(app, cors_allowed_origins="*")

    @login_manager.unauthorized_handler
    def _unauthorized():
        return jsonify({"error": "Unauthorized"}), 401

    # Register blueprints
    from .api.auth import bp as auth_bp
    from .api.users import bp as users_bp
    from .api.rooms import bp as rooms_bp
    from .api.gigs import bp as gigs_bp
    from .api.payments import bp as payments_bp
    from .api.integrations import bp as integrations_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(rooms_bp, url_prefix="/api/rooms")
    app.register_blueprint(gigs_bp, url_prefix="/api/gigs")
    app.register_blueprint(payments_bp, url_prefix="/api/payments")
    app.register_blueprint(integrations_bp, url_prefix="/api/integrations")

    # Socket events
    from .sockets import register_socket_events
    register_socket_events(socketio)

    # Simple health route
    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    # CLI
    from .cli import register_cli
    register_cli(app)

    return app
