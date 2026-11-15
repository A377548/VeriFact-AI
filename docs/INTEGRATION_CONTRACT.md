
# VeriFact AI – Module Integration Contract

## 1. Purpose

This document defines the standardized data interface
between the three members developing VeriFact AI.

All modules must follow this contract to ensure smooth
integration.

**Schema Version:** 1.0

## 2. Overall Architecture

The system is divided into three major responsibilities.

### Person 1 – LLM Integration and Claim Intelligence

- Generate the original LLM response.
- Generate independent response samples.
- Extract atomic factual claims.
- Perform sentence segmentation.
- Extract named entities.
- Validate claims.
- Produce standardized JSON output.

### Person 2 – SelfCheckGPT and Hallucination Detection

- Compare original claims against independent samples.
- Calculate claim-level consistency scores.
- Implement SelfCheckGPT-based detection methods.
- Identify suspicious or inconsistent claims.
- Return claim-level detection results.

### Person 3 – Evidence Verification and Dashboard

- Retrieve external evidence.
- Rank relevant evidence passages.
- Perform NLI-based evidence verification.
- Classify claims as Supported, Refuted or Not Enough Information.
- Generate explanations.
- Display results in the Streamlit dashboard.

## 3. Standardized Input Structure

The output produced by Person 1 follows this structure:

{
    "project": "VeriFact AI",
    "schema_version": "1.0",
    "question": "Who discovered penicillin?",
    "original_answer": "Alexander Fleming discovered penicillin in 1928.",
    "model": "gemini-3.8-flash",

    "samples": [
        {
            "sample_id": 1,
            "answer": "Alexander Fleming discovered penicillin in 1928."
        }
    ],

    "claims": [
        {
            "claim_id": "C001",
            "claim": "Alexander Fleming discovered penicillin.",
            "source_sentence_indices": [1],
            "source_sentences": [
                "Alexander Fleming discovered penicillin in 1928."
            ],
            "entities": [],
            "is_valid": true,
            "issues": []
        }
    ],

    "claim_summary": {
        "sentence_count": 1,
        "claim_count": 1,
        "valid_claim_count": 1,
        "invalid_claim_count": 0
    }
}

## 4. Field Definitions

| Field | Description |
|---|---|
| project | Project identifier |
| schema_version | Output schema version |
| question | Original user question |
| original_answer | Initial LLM-generated answer |
| model | LLM model identifier |
| samples | Independent generated responses |
| sample_id | Unique sample number within this output |
| answer | Text of an independent sample |
| claims | Extracted factual claims |
| claim_id | Unique claim identifier within this output |
| claim | Atomic factual statement |
| source_sentence_indices | One-based source sentence positions |
| source_sentences | Original sentences associated with the claim |
| entities | Named entities identified by spaCy |
| is_valid | Result of claim quality validation |
| issues | Validation warnings or errors |
| claim_summary | Summary of extraction and validation |

## 5. Person 2 – Integration Requirements

Person 2 receives:

- question
- original_answer
- samples
- claims

The detector must:

1. Analyze each claim independently.
2. Compare claims with the generated samples.
3. Calculate consistency or inconsistency signals.
4. Preserve the original claim_id.
5. Return results associated with the same claim_id.

Do not treat consistency as proof of factual truth.

## 6. Person 3 – Integration Requirements

Person 3 receives:

- question
- original_answer
- claims
- source_sentences
- entities
- is_valid

The evidence verifier must:

1. Retrieve relevant evidence for each claim.
2. Rank evidence passages.
3. Perform NLI-based verification.
4. Classify claims as Supported, Refuted or Not Enough Information.
5. Preserve claim_id.
6. Return evidence sources and explanations.

Named entity labels are predictions and must not be treated as verified facts.

## 7. Important Integration Rules

1. Do not rename existing fields without agreement.
2. Preserve claim_id across every module.
3. Use one-based sentence indices.
4. Do not modify original_answer.
5. Keep samples independent of one another.
6. Do not silently delete invalid claims.
7. Distinguish consistency from factual verification.
8. Document any schema changes.
9. Use schema_version to identify interface changes.

## 8. Expected Integration Flow

Person 1
    |
    v
Standardized VeriFactOutput
    |
    +----------------------+
    |                      |
    v                      v
Person 2                Person 3
Consistency             Evidence
Detection               Verification
    |                      |
    +----------+-----------+
               |
               v
       Combined Results
               |
               v
       Streamlit Dashboard

## 9. Current Implementation Status

Completed:

- Original answer generation
- Independent response generation
- Sentence segmentation
- Atomic claim extraction
- Source sentence traceability
- Named entity extraction
- Claim validation
- Claim extraction evaluation
- Pydantic output schema
- Standardized output builder
- Main application integration
- Mock integration tests

Pending integration:

- SelfCheckGPT detection
- External evidence retrieval
- NLI verification
- Adaptive verification
- Dashboard integration

## 10. Versioning

Current contract version: 1.0

Any changes to required fields, field names or data types
must be discussed with all team members before implementation.
