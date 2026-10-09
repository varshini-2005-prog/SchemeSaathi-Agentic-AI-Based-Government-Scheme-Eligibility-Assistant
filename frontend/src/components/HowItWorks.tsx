import React from 'react';
import { UserCheck, Filter, FileText } from 'lucide-react';

export const HowItWorks: React.FC = () => {
  const steps = [
    {
      number: '01',
      icon: UserCheck,
      title: 'Share Basic Information',
      description: 'Enter basic details such as age, gender, district, income, or occupation in simple English, Tamil, or Tanglish.',
    },
    {
      number: '02',
      icon: Filter,
      title: 'Adaptive Smart Follow-up',
      description: 'The agent checks candidate schemes and prompts ONLY for missing parameters required by active schemes.',
    },
    {
      number: '03',
      icon: FileText,
      title: 'Review PASS/FAIL Rules & Documents',
      description: 'Inspect exact condition checks, required documents, official e-Sevai links, and Government Order (G.O.) citations.',
    },
  ];

  return (
    <section className="py-16 bg-white border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div className="text-center max-w-3xl mx-auto mb-12">
          <h2 className="text-xs font-bold text-teal-700 uppercase tracking-widest mb-2">Transparent Process</h2>
          <h3 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">How SchemeSaathi Works</h3>
          <p className="text-slate-600 text-sm sm:text-base mt-3">
            Designed to replace generic LLM text guesses with explicit, rule-based government scheme eligibility reasoning.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((step) => {
            const IconComponent = step.icon;
            return (
              <div
                key={step.number}
                className="relative bg-slate-50 rounded-2xl p-6 border border-slate-200 hover:border-teal-300 transition-all shadow-xs"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-xl bg-teal-100 text-teal-800 flex items-center justify-center">
                    <IconComponent className="w-6 h-6" />
                  </div>
                  <span className="text-2xl font-black text-slate-300">{step.number}</span>
                </div>
                <h4 className="text-lg font-bold text-slate-900 mb-2">{step.title}</h4>
                <p className="text-slate-600 text-xs sm:text-sm leading-relaxed">{step.description}</p>
              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
};
