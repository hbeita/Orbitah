import { LoginForm } from "@/components/auth/LoginForm";
import { RegisterForm } from "@/components/auth/RegisterForm";
import Dashboard from "@/components/dashboard/Dashboard";
import SpaceBackground from "@/components/SpaceBackground";
import { LanguageSwitcher } from "@/components/ui/language-switcher";
import { AuthProvider, useAuth } from "@/contexts/AuthContext";
import { LanguageProvider } from "@/contexts/LanguageContext";
import React, { useState } from "react";

const AppContent: React.FC = () => {
  const { user, loading, isAuthenticated } = useAuth();
  const [isLogin, setIsLogin] = useState(true);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center relative">
        <SpaceBackground />
        <div className="relative z-10 text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-400 mx-auto"></div>
          <p className="mt-4 text-white/80">Loading...</p>
          <div className="mt-6">
            <LanguageSwitcher />
          </div>
        </div>
      </div>
    );
  }

  if (isAuthenticated && user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative">
        <SpaceBackground />
        <Dashboard />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative">
      <SpaceBackground />
      <div className="relative z-10 min-h-screen flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          {isLogin ? (
            <LoginForm onSwitchToRegister={() => setIsLogin(false)} />
          ) : (
            <RegisterForm onSwitchToLogin={() => setIsLogin(true)} />
          )}
        </div>
      </div>
    </div>
  );
};

function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </LanguageProvider>
  );
}

export default App;
