from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
import requests
import sqlite3
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask import g
import sys

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['JSON_SORT_KEYS'] = False

# Add RAG directory to path for imports
rag_path = os.path.join(os.path.dirname(__file__), 'RAG')
if rag_path not in sys.path:
    sys.path.insert(0, rag_path)

# Import RAG query function
try:
    from query import run_query as rag_run_query
    RAG_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import RAG module: {e}")
    RAG_AVAILABLE = False

# Database configuration
DB_PATH = os.getenv('DATABASE_PATH', 'startuplex_users.db')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_users_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password_hash TEXT,
            api_key TEXT,
            created_at TEXT
        )
        '''
    )
    conn.commit()
    conn.close()


def create_user(name, email, password):
    password_hash = generate_password_hash(password)
    api_key = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO users (name, email, password_hash, api_key, created_at) VALUES (?, ?, ?, ?, ?)',
            (name, email, password_hash, api_key, created_at)
        )
        conn.commit()
        user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return None
    conn.close()
    return {'id': user_id, 'name': name, 'email': email, 'api_key': api_key, 'created_at': created_at}


def get_user_by_email(email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE email = ?', (email,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_api_key(api_key):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE api_key = ?', (api_key,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def verify_password(stored_hash, password):
    return check_password_hash(stored_hash, password)

# Initialize DB table
create_users_table()

# Routes

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'active',
        'service': 'StartupLex Backend',
        'rag_available': RAG_AVAILABLE,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/query', methods=['POST'])
def handle_query():
    """
    Handle legal queries from the frontend using RAG model
    Expected JSON: { "question": "user question" }
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({'error': 'Missing required field: question'}), 400
        
        question = data.get('question')
        
        if not RAG_AVAILABLE:
            return jsonify({'error': 'RAG model not available. Check if RAG module is properly configured.'}), 503
        
        # Get response from RAG model
        answer = rag_run_query(question)
        
        response = {
            'status': 'success',
            'question': question,
            'answer': answer,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def _extract_api_key_from_header():
    auth = request.headers.get('Authorization', '')
    if not auth:
        return None
    parts = auth.split()
    if len(parts) == 2 and parts[0].lower() == 'bearer':
        return parts[1]
    return None


def auth_required(f):
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = _extract_api_key_from_header()
        if not api_key:
            return jsonify({'error': 'Missing Authorization header'}), 401
        user = get_user_by_api_key(api_key)
        if not user:
            return jsonify({'error': 'Invalid API token'}), 401
        g.current_user = user
        return f(*args, **kwargs)

    return decorated


@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json() or {}
        name = data.get('name') or ''
        email = (data.get('email') or '').strip().lower()
        password = data.get('password') or ''

        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400

        existing = get_user_by_email(email)
        if existing:
            return jsonify({'error': 'User with this email already exists'}), 409

        user = create_user(name, email, password)
        if not user:
            return jsonify({'error': 'Failed to create user'}), 500

        return jsonify({'status': 'success', 'user': {'id': user['id'], 'name': user['name'], 'email': user['email']}, 'api_key': user['api_key']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/signin', methods=['POST'])
def signin():
    try:
        data = request.get_json() or {}
        email = (data.get('email') or '').strip().lower()
        password = data.get('password') or ''

        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400

        user = get_user_by_email(email)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        if not verify_password(user['password_hash'], password):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Return existing API key
        return jsonify({'status': 'success', 'user': {'id': user['id'], 'name': user['name'], 'email': user['email']}, 'api_key': user['api_key']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/me', methods=['GET'])
@auth_required
def me():
    user = g.get('current_user')
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    safe_user = {'id': user['id'], 'name': user['name'], 'email': user['email'], 'created_at': user['created_at']}
    return jsonify({'status': 'success', 'user': safe_user}), 200




@app.route('/api/documents', methods=['GET'])
def get_documents():
    """Get available compliance documents"""
    documents = [
        {'id': 1, 'title': 'LLC Formation Guide', 'category': 'Formation'},
        {'id': 2, 'title': 'SAFE Agreements', 'category': 'Fundraising'},
        {'id': 3, 'title': 'Equity Split Guide', 'category': 'Cap Table'},
    ]
    return jsonify(documents), 200


@app.route('/api/documents/<int:doc_id>', methods=['GET'])
def get_document(doc_id):
    """Get a specific document"""
    # TODO: Fetch from database
    document = {
        'id': doc_id,
        'title': f'Document {doc_id}',
        'content': 'Document content here',
        'category': 'Legal'
    }
    return jsonify(document), 200


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle multi-turn conversations
    Expected JSON: { "messages": [{"role": "user", "content": "..."}], "session_id": "optional" }
    """
    try:
        data = request.get_json()
        
        if not data or 'messages' not in data:
            return jsonify({'error': 'Missing required field: messages'}), 400
        
        messages = data.get('messages')
        session_id = data.get('session_id')
        
        # TODO: Process with AI model and maintain conversation context
        response = {
            'status': 'success',
            'session_id': session_id or 'new_session',
            'reply': 'This is a placeholder response. Integrate your AI model here.',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=5000)
