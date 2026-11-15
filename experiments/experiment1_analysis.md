# Experiment 1: Effect of Sample Count

## Objective
To examine how the number of independently generated responses affects the observation of factual consistency.

## Model
Gemini 3.8 Flash (`gemini-3.8-flash`)

## Test Question
Who discovered penicillin and when?

## Experimental Setup
Five independent responses were requested using the same question. Three requests succeeded and two failed because of temporary API unavailability.

## Results

- Requested samples: 5
- Successful samples: 3
- Failed samples: 2
- Generation success rate: 60%
- Total generation time: 632.21 seconds
- Successful sample IDs: 1, 3 and 5

## Observations

All three successful responses consistently identified Alexander Fleming as the discoverer of penicillin and September 1928 as the discovery date.

They also agreed on St. Mary's Hospital in London, *Penicillium notatum* and *Staphylococcus*.

Minor wording differences were observed in descriptions of Fleming's professional background. No direct contradictions were identified among the selected core facts.

## Interpretation

The three successful responses demonstrated strong agreement on the selected factual details. This illustrates how independent sampling can provide consistency signals for a hallucination detection framework.

However, consistency does not establish factual correctness. Repeated responses may share the same incorrect information.

## Limitations

1. Only three of the five requested responses were successfully generated.
2. The experiment uses one question and one model.
3. The results are exploratory and cannot establish statistical significance.
4. The generation time was affected by temporary API unavailability.
5. The experiment measures observed agreement, not factual accuracy.

## Conclusion

The experiment produced three successful independent responses with strong agreement on the main factual details. The results support further investigation of sample-based consistency analysis in VeriFact AI. More questions and repeated trials are needed for stronger conclusions.