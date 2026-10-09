import React, { useState } from 'react';
import { UserProfile, EvaluationResponse } from '../types/scheme';
import { evaluateProfile } from '../services/api';
import { ShieldCheck, ArrowRight, RefreshCw, AlertCircle, HelpCircle } from 'lucide-react';

interface EligibilityCheckerProps {
  onResultsGenerated: (results: EvaluationResponse) => void;
}

export const EligibilityChecker: React.FC<EligibilityCheckerProps> = ({ onResultsGenerated }) => {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form Profile State
  const [profile, setProfile] = useState<UserProfile>({
    age: 20,
    gender: 'female',
    district: 'Coimbatore',
    annual_family_income: 180000,
    occupation: 'student',
    education_status: 'pursuing_higher_education',
    govt_school_study_class_6_to_12: true,
    land_ownership: false,
    wet_land_acres: 0,
    four_wheeler_ownership: false,
    annual_electricity_units: 2000,
    is_bpl_or_destitute: false,
    is_institutional_landholder: false,
    is_income_tax_payer: false,
  });

  const handleInputChange = (field: keyof UserProfile, val: any) => {
    setProfile((prev) => ({ ...prev, [field]: val }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const evaluationRes = await evaluateProfile(profile);
      onResultsGenerated(evaluationRes);
    } catch (err: any) {
      setError('Could not connect to backend server. Please verify FastAPI backend is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="py-12 bg-slate-50 min-h-screen">
      <div className="max-w-3xl mx-auto px-4 sm:px-6">
        
        {/* Card Container */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-xl overflow-hidden">
          
          {/* Header */}
          <div className="bg-slate-900 text-white p-6 sm:p-8">
            <div className="flex items-center space-x-2 text-xs text-teal-400 font-semibold uppercase tracking-wider mb-2">
              <ShieldCheck className="w-4 h-4" />
              <span>Stateful Eligibility Engine</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Scheme Eligibility Check
            </h2>
            <p className="text-slate-400 text-xs sm:text-sm mt-1">
              Enter your basic details. The agent checks deterministic rules without guessing your qualification.
            </p>

            {/* Step Progress Bar */}
            <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between text-xs font-medium">
              <span className={step >= 1 ? 'text-teal-400 font-bold' : 'text-slate-500'}>Step 1: Personal & Location</span>
              <span className="text-slate-600">•</span>
              <span className={step >= 2 ? 'text-teal-400 font-bold' : 'text-slate-500'}>Step 2: Education & Occupation</span>
              <span className="text-slate-600">•</span>
              <span className={step >= 3 ? 'text-teal-400 font-bold' : 'text-slate-500'}>Step 3: Assets & Family</span>
            </div>
            <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
              <div
                className="bg-teal-500 h-full transition-all duration-300"
                style={{ width: `${(step / 3) * 100}%` }}
              ></div>
            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="p-6 sm:p-8 space-y-6">
            
            {error && (
              <div className="bg-rose-50 border border-rose-200 text-rose-800 text-xs p-4 rounded-xl flex items-center space-x-3">
                <AlertCircle className="w-5 h-5 text-rose-600 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {/* STEP 1: Personal Details */}
            {step === 1 && (
              <div className="space-y-5 animate-in fade-in duration-200">
                <h3 className="text-base font-bold text-slate-900 pb-2 border-b border-slate-100">
                  Step 1: Personal Demographics
                </h3>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Age (Years)</label>
                    <input
                      type="number"
                      min={10}
                      max={100}
                      value={profile.age || ''}
                      onChange={(e) => handleInputChange('age', parseInt(e.target.value) || null)}
                      className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Gender</label>
                    <select
                      value={profile.gender || 'female'}
                      onChange={(e) => handleInputChange('gender', e.target.value)}
                      className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
                    >
                      <option value="female">Female</option>
                      <option value="male">Male</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">District in Tamil Nadu</label>
                    <input
                      type="text"
                      value={profile.district || ''}
                      onChange={(e) => handleInputChange('district', e.target.value)}
                      placeholder="e.g. Coimbatore, Chennai, Salem"
                      className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Annual Family Income (₹)</label>
                    <input
                      type="number"
                      step={10000}
                      value={profile.annual_family_income || ''}
                      onChange={(e) => handleInputChange('annual_family_income', parseFloat(e.target.value) || null)}
                      placeholder="e.g. 180000"
                      className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
                      required
                    />
                  </div>
                </div>

                <div className="flex justify-end pt-4">
                  <button
                    type="button"
                    onClick={() => setStep(2)}
                    className="bg-teal-700 hover:bg-teal-800 text-white font-medium text-sm px-6 py-2.5 rounded-xl flex items-center space-x-2 shadow-xs"
                  >
                    <span>Next: Education & Work</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            )}

            {/* STEP 2: Occupation & Schooling */}
            {step === 2 && (
              <div className="space-y-5 animate-in fade-in duration-200">
                <h3 className="text-base font-bold text-slate-900 pb-2 border-b border-slate-100">
                  Step 2: Occupation & Education
                </h3>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Current Occupation</label>
                    <select
                      value={profile.occupation || 'student'}
                      onChange={(e) => handleInputChange('occupation', e.target.value)}
                      className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
                    >
                      <option value="student">Student</option>
                      <option value="farmer">Farmer / Agriculturalist</option>
                      <option value="employed">Private / Govt Employee</option>
                      <option value="unemployed">Homemaker / Unemployed</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Higher Education Status</label>
                    <select
                      value={profile.education_status || 'pursuing_higher_education'}
                      onChange={(e) => handleInputChange('education_status', e.target.value)}
                      className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
                    >
                      <option value="pursuing_higher_education">Pursuing Degree / Diploma / ITI</option>
                      <option value="completed_degree">Completed Degree</option>
                      <option value="school_level">High School Level</option>
                    </select>
                  </div>
                </div>

                <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3">
                  <div className="flex items-start space-x-3">
                    <input
                      type="checkbox"
                      id="govt_school"
                      checked={profile.govt_school_study_class_6_to_12 === true}
                      onChange={(e) => handleInputChange('govt_school_study_class_6_to_12', e.target.checked)}
                      className="mt-1 w-4 h-4 text-teal-600 rounded focus:ring-teal-500"
                    />
                    <label htmlFor="govt_school" className="text-xs text-slate-800 leading-relaxed cursor-pointer">
                      <strong>Studied Class 6 to 12 in Tamil Nadu Government School</strong>
                      <span className="block text-slate-500 text-[11px] mt-0.5">
                        Required for Pudhumai Penn and Tamizh Pudhalvan schemes.
                      </span>
                    </label>
                  </div>
                </div>

                <div className="flex justify-between pt-4">
                  <button
                    type="button"
                    onClick={() => setStep(1)}
                    className="text-slate-600 hover:text-slate-900 text-sm font-medium px-4 py-2"
                  >
                    Back
                  </button>
                  <button
                    type="button"
                    onClick={() => setStep(3)}
                    className="bg-teal-700 hover:bg-teal-800 text-white font-medium text-sm px-6 py-2.5 rounded-xl flex items-center space-x-2 shadow-xs"
                  >
                    <span>Next: Assets & Household</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            )}

            {/* STEP 3: Assets & Family */}
            {step === 3 && (
              <div className="space-y-5 animate-in fade-in duration-200">
                <h3 className="text-base font-bold text-slate-900 pb-2 border-b border-slate-100">
                  Step 3: Family Assets & Support Status
                </h3>

                <div className="space-y-4">
                  <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 flex items-center justify-between">
                    <div>
                      <span className="text-xs font-semibold text-slate-800">Owns Agricultural Land?</span>
                      <p className="text-[11px] text-slate-500">Cultivable land holding for farmer schemes</p>
                    </div>
                    <select
                      value={profile.land_ownership ? 'true' : 'false'}
                      onChange={(e) => handleInputChange('land_ownership', e.target.value === 'true')}
                      className="bg-white px-3 py-1.5 border border-slate-300 rounded-lg text-xs"
                    >
                      <option value="false">No</option>
                      <option value="true">Yes</option>
                    </select>
                  </div>

                  <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 flex items-center justify-between">
                    <div>
                      <span className="text-xs font-semibold text-slate-800">Four-Wheeler Ownership (Car / Jeep)?</span>
                      <p className="text-[11px] text-slate-500">Required check for KMUT welfare scheme</p>
                    </div>
                    <select
                      value={profile.four_wheeler_ownership ? 'true' : 'false'}
                      onChange={(e) => handleInputChange('four_wheeler_ownership', e.target.value === 'true')}
                      className="bg-white px-3 py-1.5 border border-slate-300 rounded-lg text-xs"
                    >
                      <option value="false">No (Eligible)</option>
                      <option value="true">Yes (Excluded)</option>
                    </select>
                  </div>

                  <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 flex items-center justify-between">
                    <div>
                      <span className="text-xs font-semibold text-slate-800">BPL Card or Destitute Certificate?</span>
                      <p className="text-[11px] text-slate-500">Required for Old Age Pension (IGNOAPS)</p>
                    </div>
                    <select
                      value={profile.is_bpl_or_destitute ? 'true' : 'false'}
                      onChange={(e) => handleInputChange('is_bpl_or_destitute', e.target.value === 'true')}
                      className="bg-white px-3 py-1.5 border border-slate-300 rounded-lg text-xs"
                    >
                      <option value="false">No</option>
                      <option value="true">Yes (Eligible for Pension)</option>
                    </select>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                  <button
                    type="button"
                    onClick={() => setStep(2)}
                    className="text-slate-600 hover:text-slate-900 text-sm font-medium px-4 py-2"
                  >
                    Back
                  </button>

                  <button
                    type="submit"
                    disabled={loading}
                    className="bg-teal-700 hover:bg-teal-800 disabled:opacity-50 text-white font-bold text-sm px-8 py-3 rounded-xl shadow-md flex items-center space-x-2 transition-all"
                  >
                    {loading ? (
                      <>
                        <RefreshCw className="w-4 h-4 animate-spin" />
                        <span>Evaluating Rules...</span>
                      </>
                    ) : (
                      <>
                        <span>Evaluate My Eligibility</span>
                        <ShieldCheck className="w-5 h-5 ml-1" />
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}

          </form>

        </div>

      </div>
    </section>
  );
};
