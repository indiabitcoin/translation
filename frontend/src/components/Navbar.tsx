import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import AuthModal from './AuthModal';

interface NavbarProps {
  activeSection: string;
  onNavigate: (section: 'translate' | 'pricing' | 'dashboard') => void;
}

export default function Navbar({ activeSection, onNavigate }: NavbarProps) {
  const { user, isAuthenticated, logout } = useAuth();
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'signup'>('login');
  const [showUserMenu, setShowUserMenu] = useState(false);

  const handleAuth = (mode: 'login' | 'signup') => {
    setAuthMode(mode);
    setShowAuthModal(true);
  };

  const handleLogout = async () => {
    await logout();
    setShowUserMenu(false);
    onNavigate('translate');
  };

  return (
    <>
      <nav className="navbar">
        <div className="container">
          <div className="nav-brand">
            <i className="fas fa-language"></i>
            <span>LibreTranslate</span>
          </div>

          <div className="nav-menu">
            <button
              className={`nav-link ${activeSection === 'translate' ? 'active' : ''}`}
              onClick={() => onNavigate('translate')}
            >
              Translate
            </button>

            <button
              className={`nav-link ${activeSection === 'pricing' ? 'active' : ''}`}
              onClick={() => onNavigate('pricing')}
            >
              Pricing
            </button>

            <button
              className="nav-link"
              onClick={() => {
                document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' });
              }}
            >
              Contact
            </button>

            {isAuthenticated && (
              <button
                className={`nav-link ${activeSection === 'dashboard' ? 'active' : ''}`}
                onClick={() => onNavigate('dashboard')}
              >
                Dashboard
              </button>
            )}

            {isAuthenticated && user ? (
              <div className="user-menu">
                <button
                  className="user-btn"
                  onClick={() => setShowUserMenu(!showUserMenu)}
                >
                  <i className="fas fa-user"></i>
                  <span>{user.email}</span>
                  <i className="fas fa-chevron-down"></i>
                </button>

                {showUserMenu && (
                  <div className="user-dropdown">
                    <button
                      className="dropdown-item"
                      onClick={() => {
                        onNavigate('dashboard');
                        setShowUserMenu(false);
                      }}
                    >
                      <i className="fas fa-chart-line"></i> Dashboard
                    </button>
                    <button className="dropdown-item" onClick={handleLogout}>
                      <i className="fas fa-sign-out-alt"></i> Logout
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <>
                <button
                  className="btn btn-outline"
                  onClick={() => handleAuth('login')}
                >
                  Sign In
                </button>
                <button
                  className="btn btn-primary"
                  onClick={() => handleAuth('signup')}
                >
                  Sign Up
                </button>
              </>
            )}
          </div>
        </div>
      </nav>

      {showAuthModal && (
        <AuthModal
          mode={authMode}
          onClose={() => setShowAuthModal(false)}
          onSwitchMode={() =>
            setAuthMode(authMode === 'login' ? 'signup' : 'login')
          }
        />
      )}
    </>
  );
}
