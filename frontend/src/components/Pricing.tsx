import { useAuth } from '../contexts/AuthContext';

interface PricingProps {
  onNavigate: (section: 'translate' | 'pricing' | 'dashboard') => void;
}

export default function Pricing({ onNavigate }: PricingProps) {
  const { user } = useAuth();

  const plans = [
    {
      name: 'Free',
      price: '£0',
      period: '/month',
      features: [
        { text: '10,000 characters/month', included: true },
        { text: '50+ languages', included: true },
        { text: 'Basic translation', included: true },
        { text: 'Language detection', included: true },
        { text: 'Priority support', included: false },
        { text: 'API access', included: false },
      ],
      buttonText: user?.plan === 'free' ? 'Current Plan' : 'Get Started',
      buttonClass: 'btn-outline',
      featured: false,
    },
    {
      name: 'Pro',
      price: '£7.99',
      period: '/month',
      features: [
        { text: '1,000,000 characters/month', included: true },
        { text: '100+ languages', included: true },
        { text: 'Advanced translation', included: true },
        { text: 'Language detection', included: true },
        { text: 'Priority support', included: true },
        { text: 'API access', included: true },
      ],
      buttonText: user?.plan === 'pro' ? 'Current Plan' : 'Upgrade to Pro',
      buttonClass: 'btn-primary',
      featured: true,
    },
    {
      name: 'Enterprise',
      price: '£39.99',
      period: '/month',
      features: [
        { text: 'Unlimited characters', included: true },
        { text: '100+ languages', included: true },
        { text: 'Advanced translation', included: true },
        { text: 'Language detection', included: true },
        { text: '24/7 support', included: true },
        { text: 'Custom API limits', included: true },
      ],
      buttonText: user?.plan === 'enterprise' ? 'Current Plan' : 'Contact Sales',
      buttonClass: 'btn-outline',
      featured: false,
    },
  ];

  return (
    <section className="pricing-section">
      <h2 className="section-title">Choose Your Plan</h2>

      <div className="pricing-grid">
        {plans.map((plan) => (
          <div
            key={plan.name}
            className={`pricing-card ${plan.featured ? 'featured' : ''}`}
          >
            {plan.featured && <div className="plan-badge-top">Most Popular</div>}

            <div className="plan-header">
              <h3>{plan.name}</h3>
              <div className="plan-price">
                <span className="price">{plan.price}</span>
                <span className="period">{plan.period}</span>
              </div>
            </div>

            <ul className="plan-features">
              {plan.features.map((feature, index) => (
                <li key={index}>
                  <i
                    className={`fas fa-${feature.included ? 'check' : 'times'}`}
                  ></i>{' '}
                  {feature.text}
                </li>
              ))}
            </ul>

            <button
              className={`btn ${plan.buttonClass}`}
              disabled={user?.plan === plan.name.toLowerCase()}
              onClick={() => {
                if (plan.name === 'Free') {
                  onNavigate('translate');
                } else {
                  onNavigate('dashboard');
                }
              }}
            >
              {plan.buttonText}
            </button>
          </div>
        ))}
      </div>
    </section>
  );
}
