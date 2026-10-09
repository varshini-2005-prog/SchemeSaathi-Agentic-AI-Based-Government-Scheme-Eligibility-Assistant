"""
app/utils/evaluation.py
Benchmark evaluation metrics calculator for SchemeSaathi.
Evaluates agent performance across Scheme Matching Precision, Recall, Eligibility Accuracy,
False Eligibility Rate, Source Verification Accuracy, and Adaptive Question Efficiency.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from app.config import settings
from app.graph import run_schemesaathi_turn, create_initial_state
from app.utils.logger import logger


class BenchmarkEvaluator:
    """Evaluates agentic workflow against gold-standard dataset."""

    def __init__(self, dataset_path: Path = settings.DATA_DIR / "evaluation" / "dataset.json"):
        self.dataset_path = dataset_path

    def load_dataset(self) -> List[Dict[str, Any]]:
        """Loads evaluation dataset profiles."""
        if not self.dataset_path.exists():
            return []
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def evaluate(self) -> Dict[str, Any]:
        """
        Executes evaluation dataset and computes precision, recall, accuracy, and false eligibility rate.
        """
        dataset = self.load_dataset()
        if not dataset:
            logger.warning("Evaluation dataset empty or missing.")
            return {"status": "no_data"}

        tp = 0  # True Positive
        fp = 0  # False Positive (claimed eligible when not)
        fn = 0  # False Negative (claimed not eligible when eligible)
        tn = 0  # True Negative

        total_decisions = 0
        correct_decisions = 0
        verified_sources = 0

        lang_perf = {"en": {"correct": 0, "total": 0}, "ta": {"correct": 0, "total": 0}, "ta-en": {"correct": 0, "total": 0}}

        for item in dataset:
            msg = item["user_message"]
            lang = item.get("language", "en")
            expected_eligible = set(item.get("expected_eligible_schemes", []))
            expected_not_eligible = set(item.get("expected_not_eligible_schemes", []))

            init_state = create_initial_state()
            if "profile" in item:
                init_state["profile"].update(item["profile"])
            state = run_schemesaathi_turn(msg, init_state)

            results = state.get("eligibility_results", [])
            verifs = state.get("verification_results", [])

            predicted_eligible = set()
            predicted_not_eligible = set()

            for res in results:
                s_id = res["scheme_id"]
                status = res["overall_status"]
                if status == "ELIGIBLE":
                    predicted_eligible.add(s_id)
                elif status == "NOT ELIGIBLE":
                    predicted_not_eligible.add(s_id)

            for s_id in expected_eligible:
                total_decisions += 1
                if s_id in predicted_eligible:
                    tp += 1
                    correct_decisions += 1
                else:
                    fn += 1

            for s_id in expected_not_eligible:
                total_decisions += 1
                if s_id not in predicted_eligible:
                    tn += 1
                    correct_decisions += 1
                else:
                    fp += 1


            for v in verifs:
                if v.get("is_verified"):
                    verified_sources += 1

            # Update language performance
            if lang in lang_perf:
                lang_perf[lang]["total"] += 1
                if (predicted_eligible == expected_eligible):
                    lang_perf[lang]["correct"] += 1

        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        false_eligibility_rate = fp / total_decisions if total_decisions > 0 else 0.0
        decision_accuracy = correct_decisions / total_decisions if total_decisions > 0 else 1.0
        source_verification_accuracy = verified_sources / len(results) if results else 1.0

        metrics = {
            "total_test_cases": len(dataset),
            "total_eligibility_decisions": total_decisions,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "accuracy": round(decision_accuracy, 4),
            "false_eligibility_rate": round(false_eligibility_rate, 4),
            "source_verification_accuracy": round(source_verification_accuracy, 4),
            "language_accuracy": {
                k: round(v["correct"] / v["total"], 4) if v["total"] > 0 else 1.0
                for k, v in lang_perf.items()
            }
        }

        logger.info(f"Evaluation completed: {metrics}")
        return metrics


evaluator = BenchmarkEvaluator()
