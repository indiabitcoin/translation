import { useAuth } from '../contexts/AuthContext';

interface DashboardProps {
  onNavigate: (section: 'translate' | 'pricing' | 'dashboard') => void;
}

export default function Dashboard({ onNavigate }: DashboardProps) {
  const { user, usage } = useAuth();

  if (!user) {
    return (
      <section className="dashboard-section">
        <div className="empty-state">
          <i className="fas fa-sign-in-alt"></i>
          <h3>Please sign in to view your dashboard</h3>
        </div>
      </section>
    );
  }

  const usagePercentage = (usage.used / usage.limit) * 100;

  return (
    <section className="dashboard-section">
      <h2 className="section-title">Dashboard</h2>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>Usage This Month</h3>
          <div className="stat-value">{usage.used.toLocaleString()}</div>
          <div className="stat-label">
            of {usage.limit === Infinity ? 'unlimited' : usage.limit.toLocaleString()} characters
          </div>
          <div className="usage-bar-large">
            <div
              className="usage-progress-large"
              style={{ width: `${Math.min(usagePercentage, 100)}%` }}
            />
          </div>
        </div>

        <div className="dashboard-card">
          <h3>Current Plan</h3>
          <div className="plan-display">
            {user.plan.charAt(0).toUpperCase() + user.plan.slice(1)}
          </div>
          <button
            className="btn btn-primary"
            onClick={() => onNavigate('pricing')}
          >
            {user.plan === 'free' ? 'Upgrade Plan' : 'Manage Plan'}
          </button>
        </div>

        <div className="dashboard-card">
          <h3>Account</h3>
          <div className="account-info">
            <p>
              <strong>Email:</strong> {user.email}
            </p>
            <p>
              <strong>Name:</strong> {user.name}
            </p>
            {user.apiKey && (
              <p className="api-key">
                <strong>API Key:</strong>
                <code>{user.apiKey.substring(0, 20)}...</code>
              </p>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
