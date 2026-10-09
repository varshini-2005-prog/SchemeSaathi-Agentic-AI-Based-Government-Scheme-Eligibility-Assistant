import React, { useState } from 'react';
import { Scheme } from '../types/scheme';
import { Search, Filter, ExternalLink, ShieldCheck, FileText, ChevronRight } from 'lucide-react';

interface SchemeCatalogProps {
  schemes: Scheme[];
  onSelectScheme: (scheme: Scheme) => void;
  onCheckEligibility: () => void;
}

export const SchemeCatalog: React.FC<SchemeCatalogProps> = ({
  schemes,
  onSelectScheme,
  onCheckEligibility,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedLevel, setSelectedLevel] = useState('All');

  const categories = ['All', 'Women Welfare', 'Student', 'Farmer Support', 'Pension', 'Social Welfare'];
  const levels = ['All', 'State', 'Central'];

  const filteredSchemes = schemes.filter((s) => {
    const matchesSearch =
      s.scheme_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.scheme_category.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesCategory =
      selectedCategory === 'All' ||
      s.scheme_category.toLowerCase().includes(selectedCategory.toLowerCase());

    const matchesLevel =
      selectedLevel === 'All' ||
      s.government_level.toLowerCase().includes(selectedLevel.toLowerCase());

    return matchesSearch && matchesCategory && matchesLevel;
  });

  return (
    <section className="py-12 bg-slate-50 min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-slate-200 pb-6">
          <div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">Official Scheme Directory</h2>
            <p className="text-slate-600 text-sm mt-1">
              Browse official Tamil Nadu and Central Government welfare schemes backed by verified Government Orders.
            </p>
          </div>

          <button
            onClick={onCheckEligibility}
            className="bg-teal-700 hover:bg-teal-800 text-white font-medium text-sm px-5 py-2.5 rounded-xl shadow-xs transition-all shrink-0 self-start md:self-auto"
          >
            Check My Personal Eligibility
          </button>
        </div>

        {/* Search & Filter Controls */}
        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs space-y-4">
          <div className="relative">
            <Search className="w-5 h-5 absolute left-3.5 top-3.5 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by scheme name, keywords (e.g. scholarship, income, farmer)..."
              className="w-full pl-11 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:bg-white transition-all"
            />
          </div>

          <div className="flex flex-wrap items-center justify-between gap-4 pt-2 border-t border-slate-100 text-xs">
            {/* Category Filter Pills */}
            <div className="flex items-center space-x-2 overflow-x-auto pb-1">
              <span className="font-semibold text-slate-500 flex items-center mr-1">
                <Filter className="w-3.5 h-3.5 mr-1" /> Category:
              </span>
              {categories.map((cat) => (
                <button
                  key={cat}
                  onClick={() => setSelectedCategory(cat)}
                  className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
                    selectedCategory === cat
                      ? 'bg-teal-700 text-white shadow-xs'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>

            {/* Level Selector */}
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-slate-500">Level:</span>
              {levels.map((lvl) => (
                <button
                  key={lvl}
                  onClick={() => setSelectedLevel(lvl)}
                  className={`px-2.5 py-1 rounded font-medium transition-all ${
                    selectedLevel === lvl
                      ? 'bg-slate-900 text-white'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {lvl}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Scheme Cards Grid */}
        {filteredSchemes.length === 0 ? (
          <div className="bg-white p-12 text-center rounded-2xl border border-slate-200 space-y-3">
            <FileText className="w-12 h-12 text-slate-300 mx-auto" />
            <h4 className="text-base font-bold text-slate-800">No schemes found matching criteria</h4>
            <p className="text-xs text-slate-500">Try adjusting your search query or category filters.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredSchemes.map((scheme) => (
              <div
                key={scheme.scheme_id}
                className="bg-white rounded-2xl border border-slate-200 p-6 flex flex-col justify-between hover:border-teal-300 transition-all hover:shadow-md group"
              >
                <div className="space-y-3">
                  
                  {/* Category & Level Badges */}
                  <div className="flex items-center justify-between text-xs">
                    <span className="bg-teal-50 text-teal-800 border border-teal-200 font-medium px-2.5 py-0.5 rounded-full">
                      {scheme.scheme_category}
                    </span>
                    <span className="text-slate-400 font-mono text-[11px]">
                      {scheme.government_level} ({scheme.state})
                    </span>
                  </div>

                  {/* Title */}
                  <h3 className="text-base font-bold text-slate-900 group-hover:text-teal-700 transition-colors leading-snug">
                    {scheme.scheme_name}
                  </h3>

                  {/* Description */}
                  <p className="text-xs text-slate-600 line-clamp-3 leading-relaxed">
                    {scheme.description}
                  </p>

                  {/* Benefit Banner */}
                  <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 text-xs">
                    <span className="font-semibold text-slate-900 block mb-0.5">Benefits:</span>
                    <span className="text-teal-700 font-medium">{scheme.benefits}</span>
                  </div>

                </div>

                {/* Card Footer Actions */}
                <div className="pt-4 mt-6 border-t border-slate-100 space-y-3">
                  <div className="flex items-center justify-between text-[11px] text-slate-500">
                    <span className="truncate pr-2">Citation: {scheme.source_document}</span>
                    <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                  </div>

                  <div className="flex items-center justify-between pt-1">
                    <button
                      onClick={() => onSelectScheme(scheme)}
                      className="text-xs font-semibold text-teal-700 hover:text-teal-800 flex items-center"
                    >
                      <span>View Eligibility Rules</span>
                      <ChevronRight className="w-4 h-4 ml-0.5" />
                    </button>

                    <a
                      href={scheme.official_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-slate-400 hover:text-slate-700 p-1"
                      title="Visit Official Portal"
                    >
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </div>
                </div>

              </div>
            ))}
          </div>
        )}

      </div>
    </section>
  );
};
