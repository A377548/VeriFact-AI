
class ClaimEvaluator:
    """
    Evaluates extracted claims against manually annotated
    reference claims using normalized exact matching.
    """

    @staticmethod
    def normalize_claim(claim: str) -> str:
        """
        Normalize a claim for case-insensitive exact matching.
        """

        return " ".join(claim.casefold().split()).rstrip(".")
    
    def evaluate_dataset(self, dataset: list, predictions: dict) -> dict:
        """
        Evaluate predictions for multiple dataset examples.

        predictions format:
        {
            "E001": ["claim one", "claim two"],
            "E002": ["claim three"]
        }
        """

        if not isinstance(dataset, list):
            raise ValueError("Dataset must be a list.")

        if not isinstance(predictions, dict):
            raise ValueError("Predictions must be a dictionary.")

        example_results = []

        total_tp = 0
        total_fp = 0
        total_fn = 0

        for example in dataset:
            example_id = example["example_id"]

            predicted_claims = predictions.get(example_id, [])
            reference_claims = example["reference_claims"]

            result = self.evaluate(
                predicted_claims,
                reference_claims
            )

            total_tp += result["true_positives"]
            total_fp += result["false_positives"]
            total_fn += result["false_negatives"]

            example_results.append({
                "example_id": example_id,
                "metrics": result
            })

        precision = (
            total_tp / (total_tp + total_fp)
            if total_tp + total_fp > 0 else 0.0
        )

        recall = (
            total_tp / (total_tp + total_fn)
            if total_tp + total_fn > 0 else 0.0
        )

        f1_score = (
            2 * precision * recall / (precision + recall)
            if precision + recall > 0 else 0.0
        )

        return {
            "examples": example_results,
            "total_true_positives": total_tp,
            "total_false_positives": total_fp,
            "total_false_negatives": total_fn,
            "micro_precision": round(precision, 4),
            "micro_recall": round(recall, 4),
            "micro_f1_score": round(f1_score, 4)
        }


    def evaluate(
        self,
        predicted_claims: list,
        reference_claims: list
    ) -> dict:

        if not isinstance(predicted_claims, list):
            raise ValueError("Predicted claims must be a list.")

        if not isinstance(reference_claims, list):
            raise ValueError("Reference claims must be a list.")

        if not all(
            isinstance(claim, str) and claim.strip()
            for claim in predicted_claims + reference_claims
        ):
            raise ValueError("All claims must be non-empty strings.")

        # Normalize claims
        predictions = [
            self.normalize_claim(claim)
            for claim in predicted_claims
        ]

        references = [
            self.normalize_claim(claim)
            for claim in reference_claims
        ]

        # Use sets to prevent duplicate predictions
        # from artificially increasing true positives.
        prediction_set = set(predictions)
        reference_set = set(references)

        true_positives = len(prediction_set & reference_set)
        false_positives = len(prediction_set - reference_set)
        false_negatives = len(reference_set - prediction_set)

        # Calculate precision
        precision = (
            true_positives / (true_positives + false_positives)
            if true_positives + false_positives > 0
            else 0.0
        )

        # Calculate recall
        recall = (
            true_positives / (true_positives + false_negatives)
            if true_positives + false_negatives > 0
            else 0.0
        )

        # Calculate F1-score
        f1_score = (
            2 * precision * recall / (precision + recall)
            if precision + recall > 0
            else 0.0
        )

        return {
            "true_positives": true_positives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1_score, 4)
        }
