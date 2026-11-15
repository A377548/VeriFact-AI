# Experiment 3: Claim Extraction Performance

## Objective
To evaluate the VeriFact AI claim extraction pipeline by comparing automatically extracted claims against manually annotated reference claims.

## Dataset
- Total examples: 8
- Total manually annotated reference claims: 23
- Successfully processed examples: 6
- Examples not processed: 2
- Reference claims evaluated: 17

## Method
Each successfully processed answer was passed through the VeriFact AI claim extraction pipeline.

Extracted claims were compared against manually annotated reference claims using normalized exact matching. Matching was case-insensitive, whitespace-normalized and ignored trailing periods.

Precision, recall and F1-score were calculated using micro-averaging.

## Overall Results

| Metric | Result |
|---|---:|
| True Positives | 16 |
| False Positives | 1 |
| False Negatives | 1 |
| Micro Precision | 0.9412 |
| Micro Recall | 0.9412 |
| Micro F1-score | 0.9412 |

## Example-wise Results

| Example | TP | FP | FN | F1-score |
|---|---:|---:|---:|---:|
| E001 | 3 | 1 | 1 | 0.75 |
| E002 | 3 | 0 | 0 | 1.00 |
| E003 | 2 | 0 | 0 | 1.00 |
| E004 | 3 | 0 | 0 | 1.00 |
| E005 | 2 | 0 | 0 | 1.00 |
| E006 | 3 | 0 | 0 | 1.00 |

## Observations
1. Six examples were successfully processed by the claim extraction pipeline.
2. The pipeline matched all reference claims in E002, E003, E004, E005 and E006.
3. E001 produced one false positive and one false negative because two semantically similar claims had different wording.
4. The six evaluated examples achieved a micro F1-score of 0.9412.
5. E007 and E008 could not be processed because the Gemini API free-tier daily request quota was exceeded.

## Limitations
1. Only six of the eight examples were evaluated.
2. The dataset is small and manually constructed.
3. Exact matching may penalize semantically equivalent claims with different wording.
4. The results cannot be generalized to all domains or types of text.
5. API quota limitations reduced the number of completed evaluations.

## Conclusion
The VeriFact AI claim extraction pipeline achieved a micro precision of 0.9412, recall of 0.9412 and F1-score of 0.9412 on the six successfully evaluated examples.

The results demonstrate promising claim extraction performance on this small exploratory dataset. Further evaluation using larger datasets and semantic matching methods is required before drawing broader conclusions.