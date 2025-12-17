"""Authentication and user management."""
import hashlib
import secrets
import json
import os
from typing import Optional, Dict
from datetime import datetime, timedelta
import jwt

# Simple file-based user storage (in production, use a database)
USERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'users.json')
SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))

# Plan limits
PLAN_LIMITS = {
    'free': 10000,  # characters per month
    'pro': 1000000,
    'enterprise': float('inf')
}

def load_users() -> Dict:
    """Load users from file."""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users: Dict):
    """Save users to file."""
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password: str) -> str:
    """Hash a password."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password."""
    return hash_password(password) == hashed

def generate_api_key() -> str:
    """Generate a new API key."""
    return secrets.token_urlsafe(32)

def create_user(email: str, password: str, name: str) -> Dict:
    """Create a new user."""
    users = load_users()
    
    if email in users:
        raise ValueError("User already exists")
    
    user = {
        'email': email,
        'name': name,
        'password_hash': hash_password(password),
        'plan': 'free',
        'api_key': generate_api_key(),
        'created_at': datetime.now().isoformat(),
        'usage': {
            'used': 0,
            'reset_date': (datetime.now() + timedelta(days=30)).isoformat()
        }
    }
    
    users[email] = user
    save_users(users)
    return user

def authenticate_user(email: str, password: str) -> Optional[Dict]:
    """Authenticate a user."""
    users = load_users()
    
    if email not in users:
        return None
    
    user = users[email]
    if not verify_password(password, user['password_hash']):
        return None
    
    return user

def get_user(email: str) -> Optional[Dict]:
    """Get user by email."""
    users = load_users()
    return users.get(email)

def update_user_usage(email: str, characters: int):
    """Update user usage."""
    users = load_users()
    
    if email not in users:
        return
    
    user = users[email]
    usage = user['usage']
    
    # Reset if past reset date
    reset_date = datetime.fromisoformat(usage['reset_date'])
    if datetime.now() > reset_date:
        usage['used'] = 0
        usage['reset_date'] = (datetime.now() + timedelta(days=30)).isoformat()
    
    usage['used'] += characters
    save_users(users)

def check_usage_limit(email: str, characters: int) -> bool:
    """Check if user has enough usage limit."""
    users = load_users()
    
    if email not in users:
        return False
    
    user = users[email]
    plan = user.get('plan', 'free')
    limit = PLAN_LIMITS.get(plan, PLAN_LIMITS['free'])
    
    if limit == float('inf'):
        return True
    
    usage = user['usage']
    
    # Reset if past reset date
    reset_date = datetime.fromisoformat(usage['reset_date'])
    if datetime.now() > reset_date:
        usage['used'] = 0
        usage['reset_date'] = (datetime.now() + timedelta(days=30)).isoformat()
        save_users(users)
    
    return (usage['used'] + characters) <= limit

def get_user_usage(email: str) -> Dict:
    """Get user usage information."""
    users = load_users()
    
    if email not in users:
        return {'used': 0, 'limit': PLAN_LIMITS['free']}
    
    user = users[email]
    plan = user.get('plan', 'free')
    limit = PLAN_LIMITS.get(plan, PLAN_LIMITS['free'])
    usage = user['usage']
    
    # Reset if past reset date
    reset_date = datetime.fromisoformat(usage['reset_date'])
    if datetime.now() > reset_date:
        usage['used'] = 0
        usage['reset_date'] = (datetime.now() + timedelta(days=30)).isoformat()
        save_users(users)
    
    return {
        'used': usage['used'],
        'limit': limit if limit != float('inf') else 999999999
    }

def upgrade_user_plan(email: str, plan: str):
    """Upgrade user plan."""
    users = load_users()
    
    if email not in users:
        raise ValueError("User not found")
    
    if plan not in PLAN_LIMITS:
        raise ValueError("Invalid plan")
    
    users[email]['plan'] = plan
    save_users(users)

def generate_token(user: Dict) -> str:
    """Generate JWT token."""
    payload = {
        'email': user['email'],
        'exp': datetime.utcnow() + timedelta(days=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return email."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload.get('email')
    except:
        return None

def get_user_by_api_key(api_key: str) -> Optional[Dict]:
    """Get user by API key."""
    users = load_users()
    for user in users.values():
        if user.get('api_key') == api_key:
            return user
    return None

