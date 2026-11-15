# Person 1 Handover — VeriFact AI

## 1. Responsibility

Person 1 implemented the LLM integration, independent response generation, factual claim extraction, named entity extraction, structured output and claim extraction evaluation.

## 2. Main modules

| Module | Responsibility |
|---|---|
| `generation/llm_client.py` | Gemini API connection |
| `generation/response_generator.py` | Generates the original answer |
| `generation/sample_generator.py` | Generates independent alternative answers |
| `claim_extraction/sentence_splitter.py` | Splits answers into sentences |
| `claim_extraction/atomic_claim_extractor.py` | Extracts atomic factual claims |
| `claim_extraction/entity_extractor.py` | Identifies named entities |
| `claim_extraction/claim_formatter.py` | Assigns claim IDs and source sentences |
| `claim_extraction/claim_validator.py` | Checks claim quality |
| `claim_extraction/claim_pipeline.py` | Coordinates claim extraction |
| `schemas/claim_schema.py` | Defines the standardized output schema |
| `schemas/output_builder.py` | Builds validated VeriFact AI output |
| `evaluation/claim_evaluator.py` | Evaluates claim extraction performance |

## 3. Main pipeline

1. Receive a user question.
2. Generate the original answer using Gemini.
3. Generate independent alternative responses.
4. Split the original answer into sentences.
5. Extract atomic factual claims.
6. Extract named entities from each claim.
7. Validate claims and assign stable claim IDs.
8. Build the standardized JSON output.
9. Pass the output to the detection and evidence verification modules.

## 4. Integration contract

The current schema version is `1.0`.

Important output fields:

- `question`: Original user question.
- `original_answer`: Original LLM response.
- `model`: Model identifier.
- `samples`: Independent alternative responses.
- `claims`: Extracted factual claims.
- `claim_id`: Unique claim identifier, such as C001.
- `claim`: Atomic factual statement.
- `source_sentence_indices`: One-based sentence indices.
- `source_sentences`: Original sentences associated with the claim.
- `entities`: Named entities detected in the claim.
- `is_valid`: Claim validation result.
- `issues`: Validation warnings.
- `claim_summary`: Counts of sentences and claims.

Use `data/sample_verifact_output.json` as the sample output fixture.

Preserve existing claim IDs and field names during integration. Discuss schema changes before modifying the contract.

## 5. Instructions for Person 2

Person 2 can use the extracted claims and independent samples as input to the SelfCheckGPT detection engine.

- Compare each original claim with relevant information in the alternative responses.
- Calculate consistency or inconsistency signals.
- Keep consistency scores separate from factual truth labels.
- Do not assume that agreement between samples proves correctness.
- Do not interpret disagreement alone as proof of hallucination.

## 6. Instructions for Person 3

Person 3 can consume the standardized JSON output.

- Display the original answer and extracted claims.
- Display named entities and source sentences.
- Display the validation status and warnings.
- Connect evidence verification results to the corresponding `claim_id`.
- Keep evidence verification results separate from SelfCheckGPT consistency results.

Person 3 owns the Streamlit dashboard implementation.

## 7. Running and testing

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run the main application:

```powershell
python main.py
```

Run the saved fixture validation:

```powershell
python validate_fixture.py
```

Run the tests:

```powershell
python -m tests.test_sample_generator_failure
python -m tests.test_claim_evaluation
python -m tests.test_output_builder
python -m tests.test_main_integration
```

## 8. Experiments and limitations

Experiment results are stored in the `data/` directory, and experiment scripts and analysis reports are stored in `experiments/`.

The claim extraction evaluation uses a small manually prepared reference dataset. The reported metrics are exploratory and should not be treated as evidence of general performance.

Exact-match evaluation can penalize semantically equivalent claims.

Gemini API requests may fail because of temporary service errors or free-tier quotas. The sample generator preserves successful responses and records failed requests.

The claim extraction and entity extraction components have limitations, including imperfect atomic decomposition, entity recognition errors and possible unresolved references.

## 9. Integration recommendation

The three modules should be integrated using the standardized claim IDs and JSON structure.

Each teammate should test their module independently before full end-to-end integration.

The final system should distinguish:

1. Claim extraction and validation.
2. Consistency-based hallucination detection.
3. External evidence verification.
4. Explainable claim-level results.
5. Adaptive verification decisions.
