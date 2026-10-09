import React from 'react';
import { EvaluationResponse } from '../types/scheme';
import { CheckCircle2, XCircle, AlertTriangle, ShieldCheck, ExternalLink, FileText, ArrowLeft, RefreshCw } from 'lucide-react';

interface ResultsViewProps {
  results: EvaluationResponse;
  onReset: () => void;
  onOpenSimulator: () => void;
}

export const ResultsView: React.FC<ResultsViewProps> = ({ results, onReset, onOpenSimulator }) => {
  const { eligibility_results, verification_results, required_documents, next_steps, missing_fields } = results;

  const eligibleSchemes = eligibility_results.filter((r) => r.overall_status === 'ELIGIBLE');
  const notEligibleSchemes = eligibility_results.filter((r) => r.overall_status === 'NOT ELIGIBLE');
  const needInfoSchemes = eligibility_results.filter((r) => r.overall_status === 'NEED MORE INFORMATION');

  return (
    <section className="py-12 bg-slate-50 min-h-screen">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 space-y-8">
        
        {/* Results Header & Summary Stats */}
        <div className="bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-md space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-6">
            <div>
              <button
                onClick={onReset}
                className="inline-flex items-center text-xs font-semibold text-slate-500 hover:text-slate-800 mb-2"
              >
                <ArrowLeft className="w-3.5 h-3.5 mr-1" /> Re-enter Profile Details
              </button>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">Your Eligibility Report</h2>
              <p className="text-xs sm:text-sm text-slate-600 mt-1">
                Deterministic rule evaluation complete. Claims cross-referenced against official G.O. documents.
              </p>
            </div>

            <button
              onClick={onOpenSimulator}
              className="bg-teal-50 text-teal-800 border border-teal-200 hover:bg-teal-100 font-semibold text-xs px-4 py-2.5 rounded-xl transition-all shadow-xs flex items-center space-x-1.5 self-start sm:self-auto"
            >
              <RefreshCw className="w-4 h-4 text-teal-600" />
              <span>Simulate "What-If" Scenarios</span>
            </button>
          </div>

          {/* Metric Badges Summary */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="bg-emerald-50 border border-emerald-200 p-4 rounded-xl flex items-center justify-between">
              <div>
                <span className="text-xs font-bold text-emerald-800 uppercase tracking-wider">Eligible Schemes</span>
                <p className="text-2xl font-black text-emerald-900 mt-0.5">{eligibleSchemes.length}</p>
              </div>
              <CheckCircle2 className="w-8 h-8 text-emerald-600" />
            </div>

            <div className="bg-amber-50 border border-amber-200 p-4 rounded-xl flex items-center justify-between">
              <div>
                <span className="text-xs font-bold text-amber-800 uppercase tracking-wider">Need More Info</span>
                <p className="text-2xl font-black text-amber-900 mt-0.5">{needInfoSchemes.length}</p>
              </div>
              <AlertTriangle className="w-8 h-8 text-amber-600" />
            </div>

            <div className="bg-rose-50 border border-rose-200 p-4 rounded-xl flex items-center justify-between">
              <div>
                <span className="text-xs font-bold text-rose-800 uppercase tracking-wider">Not Eligible</span>
                <p className="text-2xl font-black text-rose-900 mt-0.5">{notEligibleSchemes.length}</p>
              </div>
              <XCircle className="w-8 h-8 text-rose-600" />
            </div>
          </div>
        </div>

        {/* Evaluated Scheme Result Cards */}
        <div className="space-y-6">
          <h3 className="text-lg font-extrabold text-slate-900">Evaluated Candidate Schemes</h3>

          {eligibility_results.map((scheme) => {
            const isEligible = scheme.overall_status === 'ELIGIBLE';
            const isNotEligible = scheme.overall_status === 'NOT ELIGIBLE';
            const verif = verification_results.find((v) => v.scheme_id === scheme.scheme_id);

            return (
              <div
                key={scheme.scheme_id}
                className={`bg-white rounded-2xl border ${
                  isEligible
                    ? 'border-emerald-300 shadow-md'
                    : isNotEligible
                    ? 'border-slate-200 opacity-90'
                    : 'border-amber-300 shadow-xs'
                } p-6 space-y-6`}
              >
                {/* Header */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                  <div>
                    <span className="text-xs font-mono text-slate-400">{scheme.scheme_id}</span>
                    <h4 className="text-lg font-bold text-slate-900 leading-snug">{scheme.scheme_name}</h4>
                  </div>

                  {/* 3-Way Status Badge */}
                  {isEligible && (
                    <div className="inline-flex items-center space-x-1.5 bg-emerald-100 border border-emerald-300 text-emerald-900 px-3.5 py-1.5 rounded-full text-xs font-extrabold shrink-0">
                      <CheckCircle2 className="w-4 h-4 text-emerald-700" />
                      <span>✅ ELIGIBLE</span>
                    </div>
                  )}

                  {isNotEligible && (
                    <div className="inline-flex items-center space-x-1.5 bg-rose-100 border border-rose-300 text-rose-900 px-3.5 py-1.5 rounded-full text-xs font-extrabold shrink-0">
                      <XCircle className="w-4 h-4 text-rose-700" />
                      <span>❌ NOT ELIGIBLE</span>
                    </div>
                  )}

                  {!isEligible && !isNotEligible && (
                    <div className="inline-flex items-center space-x-1.5 bg-amber-100 border border-amber-300 text-amber-900 px-3.5 py-1.5 rounded-full text-xs font-extrabold shrink-0">
                      <AlertTriangle className="w-4 h-4 text-amber-700" />
                      <span>⚠️ MORE INFO REQUIRED</span>
                    </div>
                  )}
                </div>

                {/* Benefits */}
                <div className="bg-slate-50 p-3.5 rounded-xl text-xs text-slate-800">
                  <span className="font-bold text-slate-900">Scheme Benefits: </span>
                  <span className="text-teal-800 font-medium">{scheme.benefits}</span>
                </div>

                {/* Rule-by-Rule Breakdown Table */}
                <div className="space-y-3">
                  <h5 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                    Rule-by-Rule Condition Check
                  </h5>

                  <div className="space-y-2">
                    {scheme.rule_evaluations.map((rule, idx) => (
                      <div
                        key={idx}
                        className={`p-3 rounded-xl border text-xs flex flex-col sm:flex-row sm:items-center justify-between gap-2 ${
                          rule.status === 'PASS'
                            ? 'bg-emerald-50/50 border-emerald-200 text-emerald-950'
                            : rule.status === 'FAIL'
                            ? 'bg-rose-50/50 border-rose-200 text-rose-950'
                            : 'bg-amber-50/50 border-amber-200 text-amber-950'
                        }`}
                      >
                        <div className="space-y-0.5">
                          <div className="font-semibold text-slate-900">{rule.description}</div>
                          <div className="text-[11px] text-slate-500">
                            Required: <code className="bg-white/80 px-1 py-0.5 rounded border border-slate-200">{rule.operator} {JSON.stringify(rule.target_value)}</code> |
                            Your Value: <code className="bg-white/80 px-1 py-0.5 rounded border border-slate-200">{JSON.stringify(rule.user_value ?? 'UNKNOWN')}</code>
                          </div>
                        </div>

                        <span
                          className={`font-black text-xs px-2.5 py-1 rounded-md shrink-0 border ${
                            rule.status === 'PASS'
                              ? 'bg-emerald-700 text-white border-emerald-800'
                              : rule.status === 'FAIL'
                              ? 'bg-rose-700 text-white border-rose-800'
                              : 'bg-amber-600 text-white border-amber-700'
                          }`}
                        >
                          {rule.status}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Verification Citation */}
                <div className="bg-slate-900 text-white p-4 rounded-xl flex items-center justify-between text-xs">
                  <div className="flex items-center space-x-2">
                    <ShieldCheck className="w-4 h-4 text-emerald-400" />
                    <span>Citation: <strong>{scheme.source_document}</strong></span>
                  </div>
                  <a
                    href={scheme.official_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-teal-300 font-semibold hover:underline flex items-center"
                  >
                    <span>Official Portal</span>
                    <ExternalLink className="w-3.5 h-3.5 ml-1" />
                  </a>
                </div>

              </div>
            );
          })}
        </div>

        {/* Required Documents Aggregate List */}
        {required_documents.length > 0 && (
          <div className="bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-md space-y-4">
            <h3 className="text-lg font-bold text-slate-900 flex items-center">
              <FileText className="w-5 h-5 text-teal-700 mr-2" />
              <span>Required Documents for Eligible Schemes</span>
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              {required_documents.map((doc, idx) => (
                <div key={idx} className="bg-slate-50 p-3 rounded-xl border border-slate-200 font-medium text-slate-800 flex items-center">
                  <span className="w-2 h-2 rounded-full bg-teal-600 mr-2.5 shrink-0"></span>
                  <span>{doc}</span>
                </div>
              ))}
            </div>
          </div>
        )}

      </div>
    </section>
  );
};
