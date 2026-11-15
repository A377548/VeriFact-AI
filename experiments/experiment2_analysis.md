# Experiment 2: Sampling Diversity

## Objective
To measure the lexical diversity between independently generated responses to the same question.

## Model
Gemini 3.8 Flash (`gemini-3.8-flash`)

## Dataset
Three successful responses from Experiment 1.

## Method
Pairwise Jaccard similarity was calculated using sets of lowercase words extracted from each response.

Lexical diversity was calculated as one minus Jaccard similarity.

## Results

| Comparison | Jaccard Similarity | Lexical Diversity |
|---|---:|---:|
| Sample 1 vs Sample 3 | 0.6452 | 0.3548 |
| Sample 1 vs Sample 5 | 0.6393 | 0.3607 |
| Sample 3 vs Sample 5 | 0.7255 | 0.2745 |

Average Jaccard similarity: 0.6700

Average lexical diversity: 0.3300

## Observations

1. Samples 3 and 5 had the highest lexical similarity (0.7255).
2. Samples 1 and 5 had the lowest lexical similarity (0.6393).
3. The average lexical similarity was 0.67.
4. The responses shared vocabulary but differed in wording and descriptive detail.

## Interpretation

The results indicate moderate lexical variation between independently generated responses.

The experiment demonstrates that independent responses can contain different wording even when they agree on important factual details.

## Limitations

1. Only three successful responses were available.
2. The experiment used one question and one model.
3. Jaccard similarity does not capture semantic meaning.
4. Word-set comparison ignores word frequency and word order.
5. Lexical similarity cannot establish factual correctness.

## Conclusion

The three responses showed an average lexical similarity of 0.67 and lexical diversity of 0.33. This provides an exploratory baseline for response diversity in VeriFact AI.

Further experiments using more questions and semantic similarity measures are required for stronger conclusions.