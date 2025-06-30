import { useAuth } from "@/contexts/AuthContext";
import React from "react";

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Main content */}
      <div className="relative z-10 min-h-screen">
        {/* Header */}
        <header className="bg-black/20 backdrop-blur-md border-b border-white/10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-400 to-purple-500 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">O</span>
                </div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                  Orbitah
                </h1>
              </div>

              <div className="flex items-center space-x-4">
                <div className="text-white/80">
                  Welcome,{" "}
                  <span className="font-semibold text-white">
                    {user?.email}
                  </span>
                </div>
                <button
                  onClick={logout}
                  className="px-4 py-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 border border-red-500/30 rounded-lg transition-all duration-200 backdrop-blur-sm"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Dashboard content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Focus Session Card */}
            <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all duration-300 group">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">
                  Focus Session
                </h3>
                <div className="w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center group-hover:bg-blue-500/30 transition-colors">
                  <span className="text-blue-400">🎯</span>
                </div>
              </div>
              <p className="text-white/70 mb-4">
                Start a new focus session to track your productivity
              </p>
              <button className="w-full bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 border border-blue-500/30 rounded-lg py-2 transition-all duration-200">
                Start Session
              </button>
            </div>

            {/* Goals Card */}
            <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all duration-300 group">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">Goals</h3>
                <div className="w-8 h-8 bg-green-500/20 rounded-lg flex items-center justify-center group-hover:bg-green-500/30 transition-colors">
                  <span className="text-green-400">🎯</span>
                </div>
              </div>
              <p className="text-white/70 mb-4">
                Track your progress towards your goals
              </p>
              <button className="w-full bg-green-600/20 hover:bg-green-600/30 text-green-400 border border-green-500/30 rounded-lg py-2 transition-all duration-200">
                View Goals
              </button>
            </div>

            {/* Achievements Card */}
            <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all duration-300 group">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">
                  Achievements
                </h3>
                <div className="w-8 h-8 bg-yellow-500/20 rounded-lg flex items-center justify-center group-hover:bg-yellow-500/30 transition-colors">
                  <span className="text-yellow-400">🏆</span>
                </div>
              </div>
              <p className="text-white/70 mb-4">
                Unlock achievements and track your milestones
              </p>
              <button className="w-full bg-yellow-600/20 hover:bg-yellow-600/30 text-yellow-400 border border-yellow-500/30 rounded-lg py-2 transition-all duration-200">
                View Achievements
              </button>
            </div>

            {/* Exploration Card */}
            <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all duration-300 group">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">
                  Exploration
                </h3>
                <div className="w-8 h-8 bg-purple-500/20 rounded-lg flex items-center justify-center group-hover:bg-purple-500/30 transition-colors">
                  <span className="text-purple-400">🚀</span>
                </div>
              </div>
              <p className="text-white/70 mb-4">
                Discover new features and capabilities
              </p>
              <button className="w-full bg-purple-600/20 hover:bg-purple-600/30 text-purple-400 border border-purple-500/30 rounded-lg py-2 transition-all duration-200">
                Explore
              </button>
            </div>

            {/* Groups Card */}
            <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all duration-300 group">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">Groups</h3>
                <div className="w-8 h-8 bg-indigo-500/20 rounded-lg flex items-center justify-center group-hover:bg-indigo-500/30 transition-colors">
                  <span className="text-indigo-400">👥</span>
                </div>
              </div>
              <p className="text-white/70 mb-4">Join or create study groups</p>
              <button className="w-full bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-400 border border-indigo-500/30 rounded-lg py-2 transition-all duration-200">
                View Groups
              </button>
            </div>

            {/* Stats Card */}
            <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all duration-300 group">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">Statistics</h3>
                <div className="w-8 h-8 bg-pink-500/20 rounded-lg flex items-center justify-center group-hover:bg-pink-500/30 transition-colors">
                  <span className="text-pink-400">📊</span>
                </div>
              </div>
              <p className="text-white/70 mb-4">
                View your productivity statistics
              </p>
              <button className="w-full bg-pink-600/20 hover:bg-pink-600/30 text-pink-400 border border-pink-500/30 rounded-lg py-2 transition-all duration-200">
                View Stats
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
