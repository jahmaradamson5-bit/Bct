import React, { useState, useEffect, useRef } from 'react';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { Activity, LineChart, Wallet, Settings, Zap } from 'lucide-react';
import { Tabs, TabsList, TabsTrigger } from '../components/ui/tabs';
import Dashboard from './Dashboard';
import WalletTracker from './WalletTracker';
import Trading from './Trading';
import SettingsPage from './SettingsPage';

export default function MainLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  const [activeTab, setActiveTab] = useState('dashboard');

  useEffect(() => {
    const path = location.pathname.substring(1) || 'dashboard';
    setActiveTab(path);
  }, [location]);

  const handleTabChange = (value) => {
    setActiveTab(value);
    navigate(`/${value === 'dashboard' ? '' : value}`);
  };

  return (
    <div className="min-h-screen bg-[#FAFAFA]">
      {/* Header with Navigation */}
      <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-[#E4E4E7]">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-black rounded-sm flex items-center justify-center">
                <Activity className="w-5 h-5 text-white" />
              </div>
              <h1 className="text-xl font-['Manrope'] font-extrabold tracking-tight">Polymarket Trading Bot</h1>
            </div>
            <div className="flex items-center gap-2 text-xs font-mono text-gray-500">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
              LIVE
            </div>
          </div>
          
          {/* Navigation Tabs */}
          <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full">
            <TabsList className="grid w-full grid-cols-4 bg-gray-100 rounded-sm p-1">
              <TabsTrigger 
                value="dashboard" 
                className="data-[state=active]:bg-white data-[state=active]:text-black rounded-sm font-semibold text-sm"
                data-testid="tab-dashboard"
              >
                <LineChart className="w-4 h-4 mr-2" />
                Dashboard
              </TabsTrigger>
              <TabsTrigger 
                value="wallets"
                className="data-[state=active]:bg-white data-[state=active]:text-black rounded-sm font-semibold text-sm"
                data-testid="tab-wallets"
              >
                <Wallet className="w-4 h-4 mr-2" />
                Wallet Tracker
              </TabsTrigger>
              <TabsTrigger 
                value="trading"
                className="data-[state=active]:bg-white data-[state=active]:text-black rounded-sm font-semibold text-sm"
                data-testid="tab-trading"
              >
                <Zap className="w-4 h-4 mr-2" />
                Auto Trading
              </TabsTrigger>
              <TabsTrigger 
                value="settings"
                className="data-[state=active]:bg-white data-[state=active]:text-black rounded-sm font-semibold text-sm"
                data-testid="tab-settings"
              >
                <Settings className="w-4 h-4 mr-2" />
                Settings
              </TabsTrigger>
            </TabsList>
          </Tabs>
        </div>
      </header>

      {/* Page Content */}
      <main>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/wallets" element={<WalletTracker />} />
          <Route path="/trading" element={<Trading />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </main>
    </div>
  );
}