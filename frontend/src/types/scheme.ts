export interface EligibilityRule {
  rule_id: string;
  field: string;
  operator: string;
  target_value: any;
  description: string;
  source: string;
}

export interface Scheme {
  scheme_id: string;
  scheme_name: string;
  scheme_category: string;
  government_level: string;
  state: string;
  description: string;
  benefits: string;
  eligibility_rules: EligibilityRule[];
  required_documents: string[];
  application_method: string;
  official_url: string;
  source_document: string;
  last_verified_date: string;
}

export interface RuleEvaluationResult {
  rule_id: string;
  field: string;
  operator: string;
  target_value: any;
  description: string;
  source: string;
  status: 'PASS' | 'FAIL' | 'UNKNOWN';
  user_value: any;
  reason: string;
}

export interface SchemeEvaluationResult {
  scheme_id: string;
  scheme_name: string;
  overall_status: 'ELIGIBLE' | 'NOT ELIGIBLE' | 'NEED MORE INFORMATION';
  pass_count: number;
  fail_count: number;
  unknown_count: number;
  missing_fields: string[];
  rule_evaluations: RuleEvaluationResult[];
  official_url: string;
  source_document: string;
  required_documents: string[];
  benefits: string;
}

export interface VerificationResult {
  scheme_id: string;
  scheme_name: string;
  overall_status: string;
  verification_status: 'VERIFIED' | 'UNVERIFIED';
  is_verified: boolean;
  citation: string;
  official_url: string;
  evidence_snippet: string;
}

export interface UserProfile {
  age?: number | null;
  gender?: string | null;
  district?: string | null;
  annual_family_income?: number | null;
  occupation?: string | null;
  education_status?: string | null;
  govt_school_study_class_6_to_12?: boolean | null;
  land_ownership?: boolean | null;
  wet_land_acres?: number | null;
  four_wheeler_ownership?: boolean | null;
  annual_electricity_units?: number | null;
  is_bpl_or_destitute?: boolean | null;
  is_institutional_landholder?: boolean | null;
  is_income_tax_payer?: boolean | null;
}

export interface EvaluationResponse {
  profile: UserProfile;
  eligibility_results: SchemeEvaluationResult[];
  verification_results: VerificationResult[];
  required_documents: string[];
  next_steps: string[];
  missing_fields: string[];
  sources: any[];
}

export interface WhatIfComparisonItem {
  scheme_id: string;
  scheme_name: string;
  baseline_status: string;
  simulated_status: string;
  status_changed: boolean;
}

export interface WhatIfResponse {
  baseline_profile: UserProfile;
  simulated_profile: UserProfile;
  simulated_changes: Record<string, any>;
  comparison: WhatIfComparisonItem[];
  baseline_results: SchemeEvaluationResult[];
  simulated_results: SchemeEvaluationResult[];
}
