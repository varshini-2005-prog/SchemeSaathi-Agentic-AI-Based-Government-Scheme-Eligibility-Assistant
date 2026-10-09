import React from 'react';
import { Search, ShieldCheck, ArrowRight, CheckCircle2, FileText, Sparkles } from 'lucide-react';

interface HeroProps {
  onStartChecker: () => void;
  onExploreSchemes: () => void;
}

export const Hero: React.FC<HeroProps> = ({ onStartChecker, onExploreSchemes }) => {
  return (
    <section className="relative bg-gradient-to-b from-slate-100 via-slate-50 to-white pt-12 pb-16 border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          {/* Left Column: Text Content */}
          <div className="lg:col-span-7 space-y-6">
            
            {/* Trust badge */}
            <div className="inline-flex items-center space-x-2 bg-teal-50 border border-teal-200 px-3 py-1.5 rounded-full text-xs font-semibold text-teal-800">
              <ShieldCheck className="w-4 h-4 text-teal-600" />
              <span>Verified against Official Government Orders (G.O.)</span>
            </div>

            {/* Headline */}
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight">
              Discover Government Schemes You Are <span className="text-teal-700">Eligible For</span>
            </h1>

            {/* Subheading */}
            <p className="text-base sm:text-lg text-slate-600 leading-relaxed max-w-2xl">
              SchemeSaathi adaptively checks your eligibility for Tamil Nadu and Central Government welfare programs—evaluating every rule deterministically without guessing or hallucinations.
            </p>

            {/* Primary & Secondary Buttons */}
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center space-y-3 sm:space-y-0 sm:space-x-4 pt-2">
              <button
                onClick={onStartChecker}
                className="inline-flex items-center justify-center bg-teal-700 hover:bg-teal-800 text-white font-medium text-base px-6 py-3.5 rounded-xl shadow-sm transition-all group"
              >
                <span>Find Schemes for Me</span>
                <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
              </button>
              
              <button
                onClick={onExploreSchemes}
                className="inline-flex items-center justify-center bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 font-medium text-base px-6 py-3.5 rounded-xl transition-all shadow-xs"
              >
                <Search className="w-4 h-4 mr-2 text-slate-500" />
                <span>Explore All Schemes</span>
              </button>
            </div>

            {/* Key Value Highlights */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-6 border-t border-slate-200">
              <div className="flex items-center space-x-2.5">
                <CheckCircle2 className="w-5 h-5 text-teal-600 shrink-0" />
                <span className="text-xs font-medium text-slate-700">Adaptive Questioning</span>
              </div>
              <div className="flex items-center space-x-2.5">
                <CheckCircle2 className="w-5 h-5 text-teal-600 shrink-0" />
                <span className="text-xs font-medium text-slate-700">3-Way PASS/FAIL Rules</span>
              </div>
              <div className="flex items-center space-x-2.5">
                <CheckCircle2 className="w-5 h-5 text-teal-600 shrink-0" />
                <span className="text-xs font-medium text-slate-700">Official Document Guidance</span>
              </div>
            </div>

          </div>

          {/* Right Column: Visual Scheme Discovery Portal Preview */}
          <div className="lg:col-span-5">
            <div className="bg-white rounded-2xl border border-slate-200 shadow-xl overflow-hidden">
              
              {/* Portal Header */}
              <div className="bg-slate-900 px-5 py-4 text-white flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 rounded-full bg-rose-500"></div>
                  <div className="w-3 h-3 rounded-full bg-amber-500"></div>
                  <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
                  <span className="text-xs font-mono text-slate-400 ml-2">schemesaathi.tn.gov.in</span>
                </div>
                <span className="text-xs bg-teal-800 text-teal-100 font-medium px-2 py-0.5 rounded">Live Engine</span>
              </div>

              {/* Card Content Sample */}
              <div className="p-6 space-y-4 bg-slate-50/50">
                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-teal-700 uppercase tracking-wide">Scholarship & Higher Ed</span>
                    <span className="text-xs bg-emerald-50 text-emerald-700 border border-emerald-200 font-semibold px-2 py-0.5 rounded">Eligible</span>
                  </div>
                  <h4 className="font-bold text-slate-900 text-sm">Pudhumai Penn Scheme</h4>
                  <p className="text-xs text-slate-600">₹1,000/month financial aid for female students from TN Govt Schools.</p>
                  <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                    <span>Source: G.O. (Ms) No. 18</span>
                    <span className="text-teal-700 font-semibold">PASS ✓</span>
                  </div>
                </div>

                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-amber-700 uppercase tracking-wide">Women Welfare</span>
                    <span className="text-xs bg-emerald-50 text-emerald-700 border border-emerald-200 font-semibold px-2 py-0.5 rounded">Eligible</span>
                  </div>
                  <h4 className="font-bold text-slate-900 text-sm">KMUT (Magalir Urimai Thittam)</h4>
                  <p className="text-xs text-slate-600">₹1,000 monthly rights-based support for eligible female heads of family.</p>
                  <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                    <span>Source: G.O. (Ms) No. 49</span>
                    <span className="text-teal-700 font-semibold">PASS ✓</span>
                  </div>
                </div>

                <div className="text-center pt-1">
                  <span className="text-xs text-slate-500 italic">Evaluated against 6 official Tamil Nadu & Central schemes</span>
                </div>
              </div>

            </div>
          </div>

        </div>
      </div>
    </section>
  );
};
