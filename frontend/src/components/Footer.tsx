import React from 'react';
import { Landmark, ShieldCheck } from 'lucide-react';

interface FooterProps {
  setActiveTab: (tab: string) => void;
}

export const Footer: React.FC<FooterProps> = ({ setActiveTab }) => {
  return (
    <footer className="bg-slate-900 text-slate-300 pt-12 pb-8 border-t border-slate-800 text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          
          {/* Brand Info */}
          <div className="space-y-3 md:col-span-1">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 rounded-lg bg-teal-600 flex items-center justify-center text-white font-bold">
                <Landmark className="w-5 h-5" />
              </div>
              <span className="font-bold text-lg text-white tracking-tight">SchemeSaathi</span>
            </div>
            <p className="text-slate-400 leading-relaxed text-xs">
              Agentic AI Government Scheme Eligibility Assistant for Tamil Nadu & Central Government schemes.
            </p>
          </div>

          {/* Nav Links */}
          <div>
            <h4 className="font-bold text-white uppercase text-xs tracking-wider mb-3">Quick Links</h4>
            <ul className="space-y-2 text-slate-400">
              <li>
                <button onClick={() => setActiveTab('home')} className="hover:text-teal-400 transition-colors">
                  Home Portal
                </button>
              </li>
              <li>
                <button onClick={() => setActiveTab('schemes')} className="hover:text-teal-400 transition-colors">
                  Explore Schemes Catalog
                </button>
              </li>
              <li>
                <button onClick={() => setActiveTab('checker')} className="hover:text-teal-400 transition-colors">
                  Check Scheme Eligibility
                </button>
              </li>
              <li>
                <button onClick={() => setActiveTab('simulator')} className="hover:text-teal-400 transition-colors">
                  What-if Eligibility Simulator
                </button>
              </li>
            </ul>
          </div>

          {/* Languages */}
          <div>
            <h4 className="font-bold text-white uppercase text-xs tracking-wider mb-3">Language Support</h4>
            <ul className="space-y-2 text-slate-400">
              <li>English (Official Government Translation)</li>
              <li>தமிழ் (Tamil NLU Engine)</li>
              <li>Tanglish (Tamil-English Conversational Mix)</li>
            </ul>
          </div>

          {/* Disclaimer */}
          <div>
            <h4 className="font-bold text-white uppercase text-xs tracking-wider mb-3">Official Disclaimer</h4>
            <div className="bg-slate-800/80 p-3 rounded-xl border border-slate-700 text-[11px] text-slate-300 leading-relaxed space-y-1">
              <div className="flex items-center text-teal-400 font-semibold mb-1">
                <ShieldCheck className="w-3.5 h-3.5 mr-1" />
                <span>Informational Guidance Only</span>
              </div>
              <p>
                SchemeSaathi provides informational eligibility guidance based on published Government Orders (G.O.). Always verify the latest criteria directly with official government portals before submitting formal applications.
              </p>
            </div>
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="pt-6 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between text-slate-500 text-[11px]">
          <span>© 2026 SchemeSaathi (திட்டம் சாதி). All rights reserved.</span>
          <span>Deterministic Rule Engine • FAISS Multilingual RAG • LangGraph Agent</span>
        </div>

      </div>
    </footer>
  );
};
