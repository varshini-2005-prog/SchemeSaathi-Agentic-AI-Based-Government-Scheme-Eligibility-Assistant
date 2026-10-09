import React from 'react';
import { Landmark, ShieldCheck, Languages, ChevronDown } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  language: string;
  setLanguage: (lang: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  language,
  setLanguage,
}) => {
  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur border-b border-slate-200 shadow-sm">
      {/* Official Government Disclaimer Banner */}
      <div className="bg-slate-900 text-slate-200 text-xs px-4 py-1.5 flex items-center justify-between">
        <div className="max-w-7xl mx-auto w-full flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <ShieldCheck className="w-3.5 h-3.5 text-teal-400" />
            <span>Tamil Nadu & Central Government Scheme Eligibility Guidance Portal</span>
          </div>
          <div className="hidden sm:flex items-center space-x-4 text-slate-400">
            <span>Verified Sources</span>
            <span>•</span>
            <span>Deterministic Rule Engine</span>
          </div>
        </div>
      </div>

      {/* Main Header Navigation */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Brand */}
          <div 
            className="flex items-center space-x-3 cursor-pointer"
            onClick={() => setActiveTab('home')}
          >
            <div className="w-10 h-10 rounded-lg bg-teal-700 flex items-center justify-center text-white shadow-md">
              <Landmark className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-xl text-slate-900 tracking-tight">SchemeSaathi</span>
                <span className="text-xs bg-teal-50 text-teal-800 border border-teal-200 font-semibold px-2 py-0.5 rounded">திட்டம் சாதி</span>
              </div>
              <p className="text-xs text-slate-500 hidden sm:block">Agentic Government Eligibility Assistant</p>
            </div>
          </div>

          {/* Nav Items */}
          <nav className="hidden md:flex items-center space-x-8">
            <button
              onClick={() => setActiveTab('home')}
              className={`text-sm font-medium transition-colors ${
                activeTab === 'home' ? 'text-teal-700 font-semibold' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Home
            </button>
            <button
              onClick={() => setActiveTab('schemes')}
              className={`text-sm font-medium transition-colors ${
                activeTab === 'schemes' ? 'text-teal-700 font-semibold' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Explore Schemes
            </button>
            <button
              onClick={() => setActiveTab('checker')}
              className={`text-sm font-medium transition-colors ${
                activeTab === 'checker' ? 'text-teal-700 font-semibold' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Check Eligibility
            </button>

            <button
              onClick={() => setActiveTab('simulator')}
              className={`text-sm font-medium transition-colors ${
                activeTab === 'simulator' ? 'text-teal-700 font-semibold' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              What-if Simulator
            </button>
          </nav>

          {/* Language Selector & CTA */}
          <div className="flex items-center space-x-4">
            <div className="relative flex items-center bg-slate-100 rounded-lg px-2.5 py-1.5 border border-slate-200">
              <Languages className="w-4 h-4 text-slate-500 mr-1.5" />
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="bg-transparent text-xs font-medium text-slate-700 focus:outline-none cursor-pointer pr-1"
              >
                <option value="en">English</option>
                <option value="ta">தமிழ் (Tamil)</option>
                <option value="ta-en">Tanglish</option>
              </select>
            </div>

            <button
              onClick={() => setActiveTab('checker')}
              className="bg-teal-700 hover:bg-teal-800 text-white text-sm font-medium px-4 py-2 rounded-lg shadow-sm transition-all focus:ring-2 focus:ring-teal-500 focus:ring-offset-2"
            >
              Check Eligibility
            </button>
          </div>

        </div>
      </div>
    </header>
  );
};
