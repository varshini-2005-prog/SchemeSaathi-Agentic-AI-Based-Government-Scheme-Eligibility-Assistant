import React, { useState } from 'react';
import { UserProfile, WhatIfResponse } from '../types/scheme';
import { simulateWhatIf } from '../services/api';
import { RefreshCw, ArrowRight, ShieldCheck, CheckCircle2, XCircle, AlertCircle, HelpCircle } from 'lucide-react';

interface WhatIfSimulatorProps {
  baselineProfile: UserProfile;
}

export const WhatIfSimulator: React.FC<WhatIfSimulatorProps> = ({ baselineProfile }) => {
  const [simulatedIncome, setSimulatedIncome] = useState<number>(200000);
  const [simulatedAge, setSimulatedAge] = useState<number>(baselineProfile.age || 24);
  const [simulatedLand, setSimulatedLand] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [simulationResult, setSimulationResult] = useState<WhatIfResponse | null>(null);

  const handleRunSimulation = async () => {
    setLoading(true);
    try {
      const simChanges = {
        annual_family_income: simulatedIncome,
        age: simulatedAge,
        land_ownership: simulatedLand,
      };
      const res = await simulateWhatIf(baselineProfile, simChanges);
      setSimulationResult(res);
    } catch (err) {
      console.error('What-if simulation error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="py-12 bg-slate-50 min-h-screen">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 space-y-8">
        
        {/* Header */}
        <div className="bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-md space-y-4">
          <div className="flex items-center space-x-2 text-xs text-teal-700 font-bold uppercase tracking-wider">
            <RefreshCw className="w-4 h-4" />
            <span>Counterfactual Simulator</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            What-If Eligibility Simulator
          </h2>
          <p className="text-slate-600 text-xs sm:text-sm max-w-3xl leading-relaxed">
            Test how changes to your family income, age, or land holdings affect your eligibility across Tamil Nadu and Central schemes. Your baseline profile remains completely unchanged.
          </p>
        </div>

        {/* Simulator Controls & Original Profile Side-by-Side */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          {/* Original Profile Baseline */}
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-sm font-bold text-slate-900">Original Profile (Baseline)</h3>
              <span className="text-xs bg-slate-100 text-slate-700 px-2 py-0.5 rounded font-mono">Unchanged</span>
            </div>

            <div className="space-y-3 text-xs text-slate-700">
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-500">Age:</span>
                <span className="font-semibold">{baselineProfile.age || 20} years</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-500">Gender:</span>
                <span className="font-semibold uppercase">{baselineProfile.gender || 'female'}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-500">Annual Income:</span>
                <span className="font-semibold text-teal-700">₹{(baselineProfile.annual_family_income || 180000).toLocaleString('en-IN')}</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-500">Occupation:</span>
                <span className="font-semibold">{baselineProfile.occupation || 'student'}</span>
              </div>
            </div>
          </div>

          {/* Simulation Controls Form */}
          <div className="bg-white p-6 rounded-2xl border border-teal-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-sm font-bold text-teal-900">Simulated Profile Changes</h3>
              <span className="text-xs bg-teal-50 text-teal-800 border border-teal-200 px-2 py-0.5 rounded font-medium">Hypothetical</span>
            </div>

            <div className="space-y-4 text-xs">
              <div>
                <label className="block font-semibold text-slate-800 mb-1">Simulated Annual Family Income (₹)</label>
                <input
                  type="number"
                  step={10000}
                  value={simulatedIncome}
                  onChange={(e) => setSimulatedIncome(parseFloat(e.target.value) || 0)}
                  className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm font-semibold text-teal-800 focus:outline-none focus:ring-2 focus:ring-teal-500"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-800 mb-1">Simulated Age (Years)</label>
                <input
                  type="number"
                  value={simulatedAge}
                  onChange={(e) => setSimulatedAge(parseInt(e.target.value) || 0)}
                  className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
                />
              </div>

              <div className="pt-2">
                <button
                  type="button"
                  onClick={handleRunSimulation}
                  disabled={loading}
                  className="w-full bg-teal-700 hover:bg-teal-800 text-white font-bold text-sm py-3 rounded-xl shadow-xs transition-all flex items-center justify-center space-x-2"
                >
                  {loading ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" />
                      <span>Re-evaluating Rules...</span>
                    </>
                  ) : (
                    <>
                      <span>Run "What-If" Simulation</span>
                      <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

        </div>

        {/* Side-by-Side Simulation Comparison Results */}
        {simulationResult && (
          <div className="bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-md space-y-6 animate-in fade-in duration-300">
            <div className="border-b border-slate-100 pb-4">
              <h3 className="text-lg font-bold text-slate-900">Comparative Eligibility Results</h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Simulated Income: ₹{simulatedIncome.toLocaleString('en-IN')} vs Original Income: ₹{(baselineProfile.annual_family_income || 180000).toLocaleString('en-IN')}
              </p>
            </div>

            <div className="space-y-3">
              {simulationResult.comparison.map((item) => (
                <div
                  key={item.scheme_id}
                  className={`p-4 rounded-xl border flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs ${
                    item.status_changed
                      ? 'bg-teal-50/70 border-teal-300'
                      : 'bg-slate-50 border-slate-200'
                  }`}
                >
                  <div>
                    <span className="font-mono text-slate-400 text-[11px]">{item.scheme_id}</span>
                    <h4 className="font-bold text-slate-900">{item.scheme_name}</h4>
                  </div>

                  <div className="flex items-center space-x-4">
                    <div className="text-center">
                      <span className="text-[10px] text-slate-400 block uppercase font-bold">Baseline</span>
                      <span className="font-bold text-slate-700">{item.baseline_status}</span>
                    </div>

                    <ArrowRight className="w-4 h-4 text-slate-400" />

                    <div className="text-center">
                      <span className="text-[10px] text-teal-700 block uppercase font-bold">Simulated</span>
                      <span className={`font-black ${
                        item.simulated_status === 'ELIGIBLE' ? 'text-emerald-700' : 'text-rose-700'
                      }`}>
                        {item.simulated_status}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

      </div>
    </section>
  );
};
