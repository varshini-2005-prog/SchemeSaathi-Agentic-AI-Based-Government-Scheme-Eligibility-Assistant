import { Scheme, EvaluationResponse, UserProfile, WhatIfResponse } from '../types/scheme';

const API_BASE = '/api';

export async function fetchSchemes(): Promise<Scheme[]> {
  try {
    const res = await fetch(`${API_BASE}/schemes`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn('API fetchSchemes failed, using fallback repository data:', error);
    return getFallbackSchemes();
  }
}

export async function evaluateProfile(profile: UserProfile): Promise<EvaluationResponse> {
  try {
    const res = await fetch(`${API_BASE}/evaluate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ profile }),
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return await res.json();
  } catch (error) {
    console.error('API evaluateProfile error:', error);
    throw error;
  }
}

export async function simulateWhatIf(baselineProfile: UserProfile, simulatedChanges: Record<string, any>): Promise<WhatIfResponse> {
  try {
    const res = await fetch(`${API_BASE}/whatif`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        baseline_profile: baselineProfile,
        simulated_changes: simulatedChanges,
      }),
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return await res.json();
  } catch (error) {
    console.error('API simulateWhatIf error:', error);
    throw error;
  }
}

// Reliable fallback schemes for offline / initial loading
function getFallbackSchemes(): Scheme[] {
  return [
    {
      scheme_id: "TN_SCH_001",
      scheme_name: "Pudhumai Penn Scheme (Moovalur Ramamirtham Ammiyar Higher Education Assurance Scheme)",
      scheme_category: "Women Welfare / Student Scholarship",
      government_level: "State",
      state: "Tamil Nadu",
      description: "Financial assistance scheme by the Government of Tamil Nadu to encourage female students from government schools to pursue higher education.",
      benefits: "₹1,000 per month paid directly into the bank account until the completion of Undergraduate Degree, Diploma, ITI, or professional course.",
      eligibility_rules: [
        { rule_id: "PUDHUMAI_R1", field: "gender", operator: "equals", target_value: "female", description: "Applicant must be female", source: "G.O. (Ms) No. 18, Social Welfare & Women Empowerment Dept, TN" },
        { rule_id: "PUDHUMAI_R2", field: "education_status", operator: "in", target_value: ["pursuing_higher_education"], description: "Must be currently enrolled in higher education", source: "G.O. (Ms) No. 18, Social Welfare & Women Empowerment Dept, TN" },
        { rule_id: "PUDHUMAI_R3", field: "govt_school_study_class_6_to_12", operator: "equals", target_value: true, description: "Must have studied Class 6 to 12 in TN Govt Schools", source: "Pen Kalvi Portal Guidelines" }
      ],
      required_documents: ["Aadhaar Card", "School Transfer Certificate (Class 6-12 TN Govt School)", "College Admission Bonafide", "Bank Account Details (Aadhaar Seeded)"],
      application_method: "Online application via Pen Kalvi Portal (penkalvi.tn.gov.in) through the applicant's institution.",
      official_url: "https://penkalvi.tn.gov.in",
      source_document: "Tamil Nadu Social Welfare Department Notification 2022",
      last_verified_date: "2024-09-01"
    },
    {
      scheme_id: "TN_SCH_002",
      scheme_name: "Tamizh Pudhalvan Scheme",
      scheme_category: "Student Scholarship / Social Welfare",
      government_level: "State",
      state: "Tamil Nadu",
      description: "Financial assistance scheme by the Government of Tamil Nadu for male students from government schools pursuing higher education.",
      benefits: "₹1,000 per month deposited directly into bank accounts to support purchasing books, study materials, and educational expenses.",
      eligibility_rules: [
        { rule_id: "TAMIZH_R1", field: "gender", operator: "equals", target_value: "male", description: "Applicant must be male", source: "TN Higher Education Dept Announcement 2024" },
        { rule_id: "TAMIZH_R2", field: "education_status", operator: "in", target_value: ["pursuing_higher_education"], description: "Must be enrolled in higher education", source: "TN Higher Education Guidelines" },
        { rule_id: "TAMIZH_R3", field: "govt_school_study_class_6_to_12", operator: "equals", target_value: true, description: "Must have studied Class 6 to 12 in TN Govt Schools", source: "TN Higher Education Portal Guidelines" }
      ],
      required_documents: ["Aadhaar Card", "Class 10/12 Marksheets / School TC", "College Bonafide Certificate", "Bank Passbook copy"],
      application_method: "Online registration via official Tamil Nadu Higher Education Portal through respective colleges.",
      official_url: "https://www.tn.gov.in",
      source_document: "Tamil Nadu Higher Education Dept Budget Announcement 2024",
      last_verified_date: "2024-08-15"
    },
    {
      scheme_id: "TN_SCH_003",
      scheme_name: "Kalaignar Magalir Urimai Thittam (KMUT)",
      scheme_category: "Women Welfare / Social Assistance",
      government_level: "State",
      state: "Tamil Nadu",
      description: "Rights-based monthly financial assistance scheme for female heads of eligible families in Tamil Nadu.",
      benefits: "₹1,000 per month financial grant deposited directly into bank accounts.",
      eligibility_rules: [
        { rule_id: "KMUT_R1", field: "gender", operator: "equals", target_value: "female", description: "Applicant must be female head of family", source: "G.O. (Ms) No. 49, Special Programme Implementation Dept" },
        { rule_id: "KMUT_R2", field: "age", operator: "greater_than_or_equal", target_value: 21, description: "Applicant must be at least 21 years of age", source: "KMUT Official Guidelines 2023" },
        { rule_id: "KMUT_R3", field: "annual_family_income", operator: "less_than_or_equal", target_value: 250000, description: "Annual family income must not exceed ₹2,50,000", source: "G.O. (Ms) No. 49 Section 4(i)" },
        { rule_id: "KMUT_R4", field: "four_wheeler_ownership", operator: "equals", target_value: false, description: "Family must not own a four-wheeler car/jeep", source: "KMUT Official Exclusion Criteria" }
      ],
      required_documents: ["Aadhaar Card", "TN Smart Family Card (Ration Card)", "Electricity Consumer Number", "Bank Account Details"],
      application_method: "Special application camps organized at local e-Sevai centers and ward/village offices across Tamil Nadu.",
      official_url: "https://kmut.tn.gov.in",
      source_document: "G.O. (Ms) No. 49 Special Programme Implementation Dept, Govt of TN",
      last_verified_date: "2024-07-20"
    },
    {
      scheme_id: "TN_SCH_004",
      scheme_name: "Chief Minister's Comprehensive Health Insurance Scheme (CMCHIS)",
      scheme_category: "Health Insurance / Social Welfare",
      government_level: "State",
      state: "Tamil Nadu",
      description: "Comprehensive health insurance scheme to provide cashless medical treatment to low-income families in Tamil Nadu.",
      benefits: "Cashless hospitalization cover up to ₹5,00,000 per family per year for listed medical procedures across empanelled hospitals.",
      eligibility_rules: [
        { rule_id: "CMCHIS_R1", field: "annual_family_income", operator: "less_than_or_equal", target_value: 120000, description: "Annual family income must be ₹1,20,000 or less", source: "TN Health Dept G.O. (Ms) No. 314" }
      ],
      required_documents: ["Aadhaar Card of family members", "Smart Family Card (Ration Card)", "Revenue Income Certificate"],
      application_method: "Enrollment at District Kiosk / District Collectorate or empanelled hospital CMCHIS counter.",
      official_url: "https://www.cmchistn.com",
      source_document: "Tamil Nadu Health & Family Welfare Department Policy Note",
      last_verified_date: "2024-06-10"
    },
    {
      scheme_id: "CENT_SCH_001",
      scheme_name: "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
      scheme_category: "Farmer Support",
      government_level: "Central",
      state: "All India",
      description: "Central Sector scheme providing income support to all landholding farmers' families across the country.",
      benefits: "Financial benefit of ₹6,000 per year paid in three equal quarterly installments of ₹2,000 directly into bank accounts.",
      eligibility_rules: [
        { rule_id: "PMKISAN_R1", field: "occupation", operator: "equals", target_value: "farmer", description: "Applicant must be a landholding farmer", source: "PM-KISAN Operational Guidelines" },
        { rule_id: "PMKISAN_R2", field: "land_ownership", operator: "equals", target_value: true, description: "Must own cultivable agricultural land", source: "PM-KISAN Guidelines Section 2.1" }
      ],
      required_documents: ["Aadhaar Card", "Land Ownership Documents (Patta/Chitta)", "Savings Bank Account Details"],
      application_method: "Self-registration via PM-KISAN Portal (pmkisan.gov.in) or through Common Service Centers (CSCs).",
      official_url: "https://pmkisan.gov.in",
      source_document: "Ministry of Agriculture & Farmers Welfare PM-KISAN Revised Guidelines",
      last_verified_date: "2024-07-01"
    },
    {
      scheme_id: "CENT_SCH_002",
      scheme_name: "Indira Gandhi National Old Age Pension Scheme (IGNOAPS / TN OAP)",
      scheme_category: "Pension / Social Welfare",
      government_level: "Central-State Joint",
      state: "Tamil Nadu & All India",
      description: "Social security pension scheme providing financial security to elderly destitute citizens belonging to BPL households.",
      benefits: "Monthly pension of ₹1,000 per month deposited directly into the beneficiary's bank account.",
      eligibility_rules: [
        { rule_id: "IGNOAPS_R1", field: "age", operator: "greater_than_or_equal", target_value: 60, description: "Applicant must be 60 years of age or older", source: "NSAP Guidelines, Ministry of Rural Development" },
        { rule_id: "IGNOAPS_R2", field: "is_bpl_or_destitute", operator: "equals", target_value: true, description: "Must belong to Below Poverty Line (BPL) household or be destitute", source: "TN Revenue Dept Social Security Pension G.O." }
      ],
      required_documents: ["Aadhaar Card", "Age Proof Certificate", "BPL Card / Income & Destitute Certificate", "Bank Passbook details"],
      application_method: "Application submitted at local e-Sevai Center or Tahsildar Office in Tamil Nadu.",
      official_url: "https://nsap.nic.in",
      source_document: "Ministry of Rural Development NSAP Guidelines & TN Revenue Dept Guidelines",
      last_verified_date: "2024-05-15"
    }
  ];
}
