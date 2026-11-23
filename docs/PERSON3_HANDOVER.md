# Person 3 – Evidence Verification and Dashboard Integration

## 1. Role and Responsibility

Person 3 was responsible for implementing the evidence-based verification component of VeriFact AI.

The main objective was to verify factual claims extracted from AI-generated answers by retrieving external evidence, ranking relevant passages, analysing evidence using Natural Language Inference (NLI), and generating explanations for verification results.

Person 3 also contributed to integrating the verification pipeline into the Streamlit dashboard.

## 2. Modules Implemented

### 2.1 Evidence Retrieval

**Directory:** `evidence_retrieval/`

Main files:

- `wikipedia_retriever.py`
- `evidence_ranker.py`
- `evidence_pipeline.py`
- `evidence_verification_pipeline.py`

The evidence retrieval component uses the Wikipedia API to retrieve information related to extracted factual claims.

Key features:

- Searches for relevant Wikipedia articles.
- Uses query expansion to improve retrieval.
- Extracts relevant article passages.
- Implements caching and retry handling.
- Removes duplicate evidence.
- Uses TF-IDF and cosine similarity to rank retrieved passages.
- Supports evidence diversity and relevance filtering.

### 2.2 Evidence-Based NLI Verification

**File:** `hallucination_detection/evidence_nli_detector.py`

This module uses the `cross-encoder/nli-deberta-v3-small` model to compare retrieved evidence with a factual claim.

The evidence passage is provided as the premise, while the factual claim is provided as the hypothesis.

The model evaluates three relationships:

- **Entailment:** Evidence supports the claim.
- **Contradiction:** Evidence contradicts the claim.
- **Neutral:** Evidence does not provide enough information to establish either relationship.

The module combines NLI results to produce an overall verification verdict.

The implemented verdict categories are:

- `supported`
- `contradicted`
- `insufficient_evidence`

The verification logic considers evidence relationships, configured confidence thresholds, and source diversity. Repeated passages or URLs from the same publisher should not automatically count as independent corroboration.

### 2.3 Adaptive Evidence Verification

**File:** `explanation/adaptive_verifier.py`

The adaptive verifier improves evidence collection when the initial verification result is uncertain.

Workflow:

1. Retrieves an initial set of evidence using a limit of 5.
2. Ranks the retrieved passages and selects the top 3.
3. Performs NLI-based verification.
4. Checks whether the result is uncertain.
5. If necessary, performs expanded retrieval using a limit of 10 and selects the top 8 passages.
6. Combines the initial and expanded evidence.
7. Removes duplicate evidence.
8. Performs final verification using the combined evidence.

This approach allows the system to gather additional context instead of relying only on initial retrieval results.

### 2.4 Claim Explanation

**File:** `explanation/claim_explainer.py`

This module generates explanations based on the verification verdict and retrieved evidence.

It helps users understand why a claim was classified as supported, contradicted, or insufficiently supported.

### 2.5 Evidence Quality and Publisher Diversity

The evidence verification implementation includes checks to avoid treating multiple URLs from the same publisher as independent confirmation.

The test suite covers:

- Duplicate evidence handling.
- Repeated URLs from the same publisher.
- Conflicting passages from the same publisher.
- Evidence from multiple publishers.
- Insufficient evidence from a single source.

These checks improve the evidence assessment process, although they do not guarantee that the sources themselves are accurate or independent.

## 3. Dashboard Integration

**Main dashboard file:** `app_test.py`

The Person 3 verification component is integrated into the Streamlit dashboard.

The dashboard includes the following sections:

1. Ask a Question
2. AI-Generated Answer
3. Factual Claim Extraction
4. Consistency and Hallucination Analysis
5. Evidence-Based Verification
6. Verification Summary

The evidence verification component processes valid extracted claims and uses `claim_id` to associate verification results with corresponding claims.

For each verified claim, the dashboard can display:

- Claim text.
- Verification verdict.
- Number of evidence passages.
- Entailment, contradiction, and neutral counts.
- Whether adaptive retrieval was performed.
- Retrieved evidence details.
- Explanation of the verification result.

Person 2's consistency analysis and Person 3's external evidence verification serve different purposes.

- **Person 2:** Evaluates consistency across independently generated answers.
- **Person 3:** Evaluates factual claims against retrieved external evidence.

Together, these components provide complementary signals for analysing potentially hallucinated information.

## 4. Testing and Validation

Automated tests cover the major components of the project, including:

- Evidence retrieval.
- Evidence ranking.
- Evidence verification.
- Evidence NLI detection.
- Publisher diversity handling.
- Claim explanation.
- Adaptive verification.
- SelfCheck detection.
- BERTScore detection.
- NLI detection.
- Combined scoring.
- Claim processing and pipeline integration.

### Full Project Test Execution

Command:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -v
```

**Latest result: 47 tests passed.**

```text
===========================================
47 passed in 26.22s
===========================================
```

No test failures were reported.

The automated tests use mock components where appropriate to validate pipeline logic and expected behaviour. They do not establish the factual accuracy of every retrieved passage or the real-world reliability of the NLI model.

### Dashboard Validation

Both execution modes were tested successfully.

**Demo Mode:**
- Demonstration data loaded successfully.
- 2 claims processed.
- 2 claims passed through verification.
- Zero processing errors.

**Live Mode:**
- Gemini answer generation completed successfully.
- 10 claims extracted and validated.
- Consistency analysis completed.
- Evidence verification processed all 10 claims.
- Zero processing errors.

The latest manual Live Mode test returned `INSUFFICIENT EVIDENCE` for all 10 claims. This demonstrates successful pipeline execution, but not successful factual verification of those claims.

The verification results should therefore be interpreted as experimental assessments rather than guaranteed factual conclusions.

## 5. Running the Dashboard

From the project root directory, execute:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app_test.py
```

The dashboard provides Demo Mode and Live Mode.

- **Demo Mode:** Uses saved sample output and executes the verification workflow without requiring a new Gemini response.
- **Live Mode:** Generates a new AI answer and claims using the configured Gemini model before proceeding through the analysis workflow.

## 6. Known Limitations

The current implementation has several limitations:

1. **Limited evidence sources:** Evidence retrieval primarily relies on Wikipedia.
2. **Retrieval relevance:** TF-IDF ranking may not always identify the most contextually appropriate passage.
3. **NLI limitations:** The NLI model may incorrectly classify evidence, especially when claims require historical or contextual understanding.
4. **Source independence:** Multiple articles from the same publisher do not necessarily provide independent confirmation.
5. **Insufficient evidence:** Some claims may not receive enough relevant evidence to produce a reliable verdict.
6. **Experimental verification:** Verification verdicts are model-assisted assessments, not guaranteed factual conclusions.
7. **External dependencies:** Live Mode depends on the availability and correct configuration of the Gemini API and external evidence retrieval services.

## 7. Future Improvements

Possible improvements include:

- Adding reliable evidence sources beyond Wikipedia.
- Improving evidence retrieval and passage selection.
- Increasing source and publisher diversity.
- Evaluating the NLI model using a labelled factual verification dataset.
- Improving contextual understanding of historical and complex claims.
- Improving confidence calibration and verification thresholds.
- Expanding end-to-end testing with real-world evidence.

## 8. Conclusion

Person 3 implemented the evidence-based verification component of VeriFact AI, including external evidence retrieval, evidence ranking, NLI-based verification, adaptive retrieval, publisher-diversity checks, and claim explanations.

The component was integrated into the Streamlit dashboard to provide users with evidence-based assessments of factual claims.

The complete project test suite passed 47 tests, and both Demo Mode and Live Mode were successfully executed.

Together with the answer generation and consistency analysis components developed by the other team members, this work contributes to VeriFact AI's goal of identifying and analysing potentially unsupported or hallucinated information in AI-generated answers.