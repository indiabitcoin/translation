import { useState } from 'react';
import { ToastProvider } from './contexts/ToastContext';
import { TranslationProvider } from './contexts/TranslationContext';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import TranslationCard from './components/TranslationCard';
import Pricing from './components/Pricing';
import Dashboard from './components/Dashboard';
import Toast from './components/Toast';
import Footer from './components/Footer';

type Section = 'translate' | 'pricing' | 'dashboard';

function App() {
  const [activeSection, setActiveSection] = useState<Section>('translate');

  return (
    <ToastProvider>
      <AuthProvider>
        <TranslationProvider>
          <div className="app">
            <Navbar 
              activeSection={activeSection} 
              onNavigate={setActiveSection} 
            />
            
            <Hero />

            <main className="main-content">
              <div className="container">
                {activeSection === 'translate' && <TranslationCard />}
                {activeSection === 'pricing' && <Pricing onNavigate={setActiveSection} />}
                {activeSection === 'dashboard' && <Dashboard onNavigate={setActiveSection} />}
              </div>
            </main>

            <Toast />
          <Footer />
          </div>
        </TranslationProvider>
      </AuthProvider>
    </ToastProvider>
  );
}

export default App;
