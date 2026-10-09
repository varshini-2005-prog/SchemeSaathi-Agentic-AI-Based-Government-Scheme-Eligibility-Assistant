import React from 'react';
import { Scheme } from '../types/scheme';
import { X, ExternalLink, ShieldCheck, FileCheck, Landmark } from 'lucide-react';

interface SchemeModalProps {
  scheme: Scheme | null;
  onClose: () => void;
}

export const SchemeModal: React.FC<SchemeModalProps> = ({ scheme, onClose }) => {
  if (!scheme) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl max-w-2xl w-full max-h-[90vh] flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        {/* Modal Header */}
        <div className="bg-slate-900 text-white p-6 flex items-start justify-between">
          <div className="flex items-start space-x-3">
            <div className="w-10 h-10 rounded-lg bg-teal-600 flex items-center justify-center shrink-0">
              <Landmark className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs bg-teal-800 text-teal-200 px-2 py-0.5 rounded font-mono font-semibold">
                  {scheme.scheme_id}
                </span>
                <span className="text-xs bg-slate-800 text-slate-300 px-2 py-0.5 rounded">
                  {scheme.government_level} ({scheme.state})
                </span>
              </div>
              <h3 className="text-lg font-bold text-white mt-1 leading-snug">{scheme.scheme_name}</h3>
            </div>
          </div>

          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6 text-slate-800 text-sm">
          
          {/* Category & Description */}
          <div>
            <span className="text-xs font-semibold text-teal-700 uppercase tracking-wide">Category: {scheme.scheme_category}</span>
            <p className="mt-1 text-slate-700 leading-relaxed">{scheme.description}</p>
          </div>

          {/* Benefits */}
          <div className="bg-teal-50 border border-teal-200 p-4 rounded-xl">
            <h4 className="font-bold text-teal-900 text-xs uppercase tracking-wider mb-1">Financial / Service Benefits</h4>
            <p className="text-teal-800 font-medium">{scheme.benefits}</p>
          </div>

          {/* Eligibility Rules */}
          <div>
            <h4 className="font-bold text-slate-900 text-sm mb-3 flex items-center">
              <ShieldCheck className="w-4 h-4 text-teal-600 mr-2" />
              <span>Mandatory Deterministic Eligibility Rules</span>
            </h4>
            <div className="space-y-2.5">
              {scheme.eligibility_rules.map((rule, idx) => (
                <div key={idx} className="bg-slate-50 p-3 rounded-lg border border-slate-200 text-xs space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-slate-900">Condition: {rule.field}</span>
                    <span className="bg-slate-200 text-slate-800 px-2 py-0.5 rounded font-mono">
                      {rule.operator} {JSON.stringify(rule.target_value)}
                    </span>
                  </div>
                  <p className="text-slate-600">{rule.description}</p>
                  <p className="text-slate-400 text-[11px] italic">Source: {rule.source}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Required Documents */}
          <div>
            <h4 className="font-bold text-slate-900 text-sm mb-3 flex items-center">
              <FileCheck className="w-4 h-4 text-teal-600 mr-2" />
              <span>Mandatory Supporting Documents</span>
            </h4>
            <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              {scheme.required_documents.map((doc, idx) => (
                <li key={idx} className="flex items-center bg-slate-50 p-2.5 rounded-lg border border-slate-200 text-slate-700">
                  <span className="w-1.5 h-1.5 rounded-full bg-teal-600 mr-2 shrink-0"></span>
                  <span>{doc}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Application Method & Official Links */}
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2 text-xs">
            <h4 className="font-bold text-slate-900">Application Procedure</h4>
            <p className="text-slate-600 leading-relaxed">{scheme.application_method}</p>
            <div className="pt-2 flex items-center justify-between">
              <span className="text-slate-500">Official Citation: {scheme.source_document}</span>
              <a
                href={scheme.official_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center text-teal-700 font-semibold hover:underline"
              >
                <span>Visit Official Portal</span>
                <ExternalLink className="w-3.5 h-3.5 ml-1" />
              </a>
            </div>
          </div>

        </div>

        {/* Modal Footer */}
        <div className="bg-slate-100 p-4 border-t border-slate-200 flex justify-end">
          <button
            onClick={onClose}
            className="bg-slate-800 hover:bg-slate-900 text-white font-medium text-xs px-5 py-2.5 rounded-lg transition-colors"
          >
            Close Window
          </button>
        </div>

      </div>
    </div>
  );
};
