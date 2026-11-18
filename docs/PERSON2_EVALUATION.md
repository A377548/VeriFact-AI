
# Person 2 - Hallucination Detection Evaluation

## 1. Overview

Person 2 implements consistency-based hallucination detection
for VeriFact AI.

The module contains three detection techniques:

- SelfCheck: Measures consistency between an original claim
  and independently generated answers.
- BERTScore: Measures semantic similarity between claims
  and independent sample answers.
- NLI: Predicts entailment, contradiction and neutral
  relationships between sample answers and claims.

## 2. NLI Model

Model: cross-encoder/nli-deberta-v3-small

The NLI detector uses:
- Premise: Independently generated sample answer.
- Hypothesis: Original claim.

The model predicts one of three relationships:
- Entailment
- Contradiction
- Neutral

## 3. Evaluation Dataset

A manually labelled diagnostic dataset containing
15 test cases was created.

| Relationship | Number of cases |
|---|---:|
| Entailment | 5 |
| Contradiction | 5 |
| Neutral | 5 |
| Total | 15 |

## 4. Evaluation Results

| Relationship | Correct | Total | Accuracy |
|---|---:|---:|---:|
| Entailment | 5 | 5 | 100% |
| Contradiction | 5 | 5 | 100% |
| Neutral | 0 | 5 | 0% |
| Overall | 10 | 15 | 66.67% |

### Confusion Matrix

| Actual / Predicted | Entailment | Contradiction | Neutral |
|---|---:|---:|---:|
| Entailment | 5 | 0 | 0 |
| Contradiction | 0 | 5 | 0 |
| Neutral | 0 | 5 | 0 |

## 5. Observations

The model correctly classified all five entailment
examples and all five explicit contradiction examples.

However, all five unrelated or neutral examples were
incorrectly classified as contradictions.

This indicates that the model has difficulty distinguishing
unrelated information from contradictory information.

The evaluation dataset is small and manually constructed.
Therefore, these results are diagnostic and should not
be interpreted as general benchmark performance.

## 6. Scoring Strategy

The default combined scoring weights are:

| Detector | Weight |
|---|---:|
| SelfCheck | 0.50 |
| BERTScore | 0.50 |
| NLI | 0.00 |

NLI remains active and its contradiction score is reported
for diagnostic analysis.

It is excluded from the default combined risk score because
its neutral-classification performance has not been
adequately validated.
The NLI detector is still executed for every claim, but its output does not contribute to the default combined risk score.

## 7. Limitations

- The evaluation dataset contains only 15 examples.
- The examples are manually constructed.
- NLI incorrectly classifies unrelated statements as
  contradictions.
- BERTScore measures semantic similarity, not factual truth.
- SelfCheck measures consistency, not factual correctness.
- The combined score is experimental and is not a calibrated
  probability of hallucination.

## 8. Conclusion

Person 2 successfully implemented and tested the
consistency-based hallucination detection module.

The pipeline integrates SelfCheck, BERTScore, NLI and a
combined scoring engine.

All 17 automated tests passed during the latest test run.
The real detection pipeline also executed successfully.

Further evaluation using a larger and more diverse
labelled dataset is required before making strong claims
about detection accuracy.
