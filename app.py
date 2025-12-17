import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# RPA Monitor - Setup
from rpa_monitor_client import setup_rpa_monitor, rpa_log

def init_rpa_monitor():
    """Inicializa o RPA Monitor com as configurações das secrets"""
    try:
        rpa_id = os.environ.get('RPA_MONITOR_ID', 'APP-GESTAO-INOVAILAB')
        host = os.environ.get('RPA_MONITOR_HOST', 'wss://app-in-sight.replit.app/ws')
        region = os.environ.get('RPA_MONITOR_REGION', 'Sudeste')
        transport = os.environ.get('RPA_MONITOR_TRANSPORT', 'ws')
        
        setup_rpa_monitor(
            rpa_id=rpa_id,
            host=host,
            port=None,
            region=region,
            transport=transport,
        )
        logging.info(f"RPA Monitor inicializado: {rpa_id} -> {host}")
        rpa_log.info(f"Sistema iniciado - RPA Monitor conectado", regiao="startup")
    except Exception as e:
        logging.warning(f"RPA Monitor não pôde ser inicializado: {e}")

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
mail = Mail()

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 280,
    "pool_pre_ping": True,
    "pool_size": 5,
    "max_overflow": 10,
    "pool_timeout": 30,
    "connect_args": {
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }
}

# configure file uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # Format JSON responses with indentation
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', 'txt', 'csv', 'mp4', 'mov', 'avi', 'mp3', 'wav', 'fig', 'sketch', 'psd', 'ai'}

# configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

# initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
mail.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()
    
    # Create default admin user if it doesn't exist
    from models import User
    from werkzeug.security import generate_password_hash
    
    admin = User.query.filter_by(email='admin@sistema.com').first()
    if not admin:
        admin_user = User(
            nome='Administrador',
            sobrenome='Sistema',
            email='admin@sistema.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created: admin@sistema.com / admin123")
    
    # Create default file categories if they don't exist
    from models import FileCategory
    default_categories = [
        {'nome': 'UX/Design', 'icone': 'fa-palette', 'cor': '#8b5cf6', 'ordem': 1},
        {'nome': 'Documentação', 'icone': 'fa-file-alt', 'cor': '#3b82f6', 'ordem': 2},
        {'nome': 'Desenvolvimento', 'icone': 'fa-code', 'cor': '#10b981', 'ordem': 3},
        {'nome': 'Imagens', 'icone': 'fa-image', 'cor': '#f59e0b', 'ordem': 4},
        {'nome': 'Vídeos', 'icone': 'fa-video', 'cor': '#ef4444', 'ordem': 5},
        {'nome': 'Outros', 'icone': 'fa-folder', 'cor': '#6b7280', 'ordem': 6},
    ]
    for cat_data in default_categories:
        existing = FileCategory.query.filter_by(nome=cat_data['nome']).first()
        if not existing:
            category = FileCategory(**cat_data)
            db.session.add(category)
    db.session.commit()

# Inicializar RPA Monitor
init_rpa_monitor()

# Import routes after app initialization
import routes

# Register API v1 Blueprint
from api_v1 import api_v1
app.register_blueprint(api_v1)
