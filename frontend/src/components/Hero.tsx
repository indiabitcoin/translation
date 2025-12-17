import { useAuth } from '../contexts/AuthContext';

export default function Hero() {
  const { user, isAuthenticated } = useAuth();

  return (
    <section className="hero">
      <div className="container">
        <h1 className="hero-title">Translate Anywhere, Anytime</h1>
        <p className="hero-subtitle">
          World-class translation powered by AI. Support for 100+ languages.
        </p>

        {isAuthenticated && user && (
          <div className="plan-badge">
            <i className="fas fa-crown"></i>
            <span>{user.plan.charAt(0).toUpperCase() + user.plan.slice(1)} Plan</span>
          </div>
        )}
      </div>
    </section>
  );
}
