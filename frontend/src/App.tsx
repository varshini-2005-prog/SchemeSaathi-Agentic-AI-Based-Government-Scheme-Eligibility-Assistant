import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { HowItWorks } from './components/HowItWorks';
import { SchemeCatalog } from './components/SchemeCatalog';
import { EligibilityChecker } from './components/EligibilityChecker';
import { ResultsView } from './components/ResultsView';
import { WhatIfSimulator } from './components/WhatIfSimulator';
import { SchemeModal } from './components/SchemeModal';
import { Footer } from './components/Footer';

import { Scheme, EvaluationResponse, UserProfile } from './types/scheme';
import { fetchSchemes } from './services/api';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('home');
  const [language, setLanguage] = useState<string>('en');
  
  const [schemes, setSchemes] = useState<Scheme[]>([]);
  const [selectedSchemeModal, setSelectedSchemeModal] = useState<Scheme | null>(null);

  const [evaluationResults, setEvaluationResults] = useState<EvaluationResponse | null>(null);
  const [currentProfile, setCurrentProfile] = useState<UserProfile>({
    age: 20,
    gender: 'female',
    district: 'Coimbatore',
    annual_family_income: 180000,
    occupation: 'student',
    education_status: 'pursuing_higher_education',
    govt_school_study_class_6_to_12: true,
  });

  useEffect(() => {
    fetchSchemes().then((data) => setSchemes(data));
  }, []);

  const handleResultsGenerated = (res: EvaluationResponse) => {
    setEvaluationResults(res);
    setCurrentProfile(res.profile);
    setActiveTab('results');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
      
      {/* Navigation Bar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        language={language}
        setLanguage={setLanguage}
      />

      {/* Main Content Area */}
      <main className="flex-1">
        {activeTab === 'home' && (
          <>
            <Hero
              onStartChecker={() => setActiveTab('checker')}
              onExploreSchemes={() => setActiveTab('schemes')}
            />
            <HowItWorks />
            <SchemeCatalog
              schemes={schemes}
              onSelectScheme={(s) => setSelectedSchemeModal(s)}
              onCheckEligibility={() => setActiveTab('checker')}
            />
          </>
        )}

        {activeTab === 'schemes' && (
          <SchemeCatalog
            schemes={schemes}
            onSelectScheme={(s) => setSelectedSchemeModal(s)}
            onCheckEligibility={() => setActiveTab('checker')}
          />
        )}

        {activeTab === 'checker' && (
          <EligibilityChecker onResultsGenerated={handleResultsGenerated} />
        )}

        {activeTab === 'results' && evaluationResults && (
          <ResultsView
            results={evaluationResults}
            onReset={() => setActiveTab('checker')}
            onOpenSimulator={() => setActiveTab('simulator')}
          />
        )}

        {activeTab === 'simulator' && (
          <WhatIfSimulator baselineProfile={currentProfile} />
        )}
      </main>

      {/* Scheme Detail Modal */}
      <SchemeModal
        scheme={selectedSchemeModal}
        onClose={() => setSelectedSchemeModal(null)}
      />

      {/* Footer */}
      <Footer setActiveTab={setActiveTab} />

    </div>
  );
}

export default App;
