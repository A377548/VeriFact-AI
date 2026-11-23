
import json
from pathlib import Path
import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="VeriFact AI",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 VeriFact AI")
st.subheader("Unified AI Answer Verification System")

st.write(
    "Generate AI answers, extract factual claims, "
    "analyse consistency, detect potential hallucinations "
    "and verify claims against external evidence."
)


# --------------------------------------------------
# CACHED COMPONENTS
# --------------------------------------------------

@st.cache_resource
def get_detection_pipeline():
    from hallucination_detection.detection_pipeline import (
        HallucinationDetectionPipeline
    )
    return HallucinationDetectionPipeline()


@st.cache_resource
def get_verifier():
    from explanation.adaptive_verifier import AdaptiveEvidenceVerifier
    return AdaptiveEvidenceVerifier()


@st.cache_resource
def get_explainer():
    from explanation.claim_explainer import ClaimExplainer
    return ClaimExplainer()


# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------

if "pipeline_output" not in st.session_state:
    st.session_state.pipeline_output = None

if "consistency_results" not in st.session_state:
    st.session_state.consistency_results = None

if "consistency_error" not in st.session_state:
    st.session_state.consistency_error = None

if "evidence_results" not in st.session_state:
    st.session_state.evidence_results = {}

if "pipeline_mode" not in st.session_state:
    st.session_state.pipeline_mode = None


# --------------------------------------------------
# INPUT AND MODE SELECTION
# --------------------------------------------------

st.divider()
st.header("1. Ask a Question")

mode = st.radio(
    "Choose execution mode:",
    ["Live Mode", "Demo Mode"],
    horizontal=True
)


# --------------------------------------------------
# CLEAR RESULTS WHEN MODE CHANGES
# --------------------------------------------------

if (
    st.session_state.pipeline_mode is not None
    and mode != st.session_state.pipeline_mode
):
    st.session_state.pipeline_output = None
    st.session_state.consistency_results = None
    st.session_state.consistency_error = None
    st.session_state.evidence_results = {}
    st.session_state.pipeline_mode = None


# --------------------------------------------------
# QUESTION INPUT
# --------------------------------------------------

if mode == "Live Mode":

    question = st.text_area(
        "Enter your question:",
        placeholder="Who discovered penicillin?",
        height=100
    )

else:

    st.info(
        "Demo Mode uses the saved sample output. "
        "It does not require fresh Gemini API calls."
    )

    question = None


# --------------------------------------------------
# RUN COMPLETE VERIFICATION
# --------------------------------------------------

if st.button("Run Complete Verification", type="primary"):

    # Clear all previous execution results.
    st.session_state.pipeline_output = None
    st.session_state.consistency_results = None
    st.session_state.consistency_error = None
    st.session_state.evidence_results = {}
    st.session_state.pipeline_mode = None

    input_data = None

    try:

        # ------------------------------------------
        # DEMO MODE
        # ------------------------------------------

        if mode == "Demo Mode":

            fixture_path = (
                Path(__file__).resolve().parent
                / "data"
                / "sample_verifact_output.json"
            )

            if not fixture_path.exists():
                raise FileNotFoundError(
                    "Demo fixture not found: "
                    "data/sample_verifact_output.json"
                )

            with st.spinner("Loading saved demonstration data..."):

                with open(
                    fixture_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    input_data = json.load(file)

            required_fields = [
                "question",
                "original_answer",
                "model",
                "samples",
                "claims",
                "claim_summary"
            ]

            missing_fields = [
                field
                for field in required_fields
                if field not in input_data
            ]

            if missing_fields:
                raise ValueError(
                    f"Demo fixture is missing fields: {missing_fields}"
                )

            st.success(
                "Demonstration data loaded successfully!"
            )

        # ------------------------------------------
        # LIVE MODE
        # ------------------------------------------

        else:

            # Import generation components only when Live Mode runs.
            from generation.response_generator import ResponseGenerator
            from generation.sample_generator import SampleGenerator
            from claim_extraction.claim_pipeline import ClaimExtractionPipeline
            from schemas.output_builder import OutputBuilder

            if not question or not question.strip():
                st.warning("Please enter a question.")
                st.stop()

            current_question = question.strip()

            with st.spinner("Generating AI answer..."):

                response_generator = ResponseGenerator()

                original_result = (
                    response_generator.generate_original_response(
                        current_question
                    )
                )

            with st.spinner("Extracting factual claims..."):

                claim_pipeline = ClaimExtractionPipeline()

                claim_result = claim_pipeline.process_answer(
                    original_result["answer"]
                )

            with st.spinner("Generating independent sample answers..."):

                sample_generator = SampleGenerator()

                sample_result = sample_generator.generate_samples(
                    current_question,
                    number_of_samples=3
                )

            with st.spinner("Preparing verification data..."):

                output_builder = OutputBuilder()

                final_output = output_builder.build_output(
                    question=current_question,
                    original_result=original_result,
                    sample_result=sample_result,
                    claim_result=claim_result
                )

                input_data = final_output.model_dump()

            st.success(
                "AI answer and claims generated successfully!"
            )

        # ------------------------------------------
        # VALIDATE STANDARDIZED INPUT
        # ------------------------------------------

        if not isinstance(input_data, dict):
            raise ValueError(
                "Pipeline input must be a dictionary."
            )

        if not isinstance(input_data.get("claims"), list):
            raise ValueError(
                "The generated output does not contain a valid claims list."
            )

        if not isinstance(input_data.get("samples"), list):
            raise ValueError(
                "The generated output does not contain a valid samples list."
            )

        # ------------------------------------------
        # SAVE CURRENT EXECUTION INPUT
        # ------------------------------------------

        st.session_state.pipeline_output = input_data
        st.session_state.pipeline_mode = mode

        # ------------------------------------------
        # VALID CLAIMS
        # ------------------------------------------

        valid_claims = [
            claim
            for claim in input_data["claims"]
            if claim.get("is_valid", True)
        ]

        # ------------------------------------------
        # CONSISTENCY AND HALLUCINATION ANALYSIS
        # ------------------------------------------

        if input_data["samples"] and valid_claims:

            try:

                with st.spinner(
                    "Analysing consistency and potential hallucinations..."
                ):

                    detection_pipeline = get_detection_pipeline()

                    consistency_input = dict(input_data)
                    consistency_input["claims"] = valid_claims

                    consistency_output = detection_pipeline.process(
                        consistency_input
                    )

                    st.session_state.consistency_results = (
                        consistency_output
                    )

            except Exception as error:

                st.session_state.consistency_error = str(error)

        else:

            st.session_state.consistency_error = (
                "Analysis skipped because no usable samples "
                "or valid claims were available."
            )

        # ------------------------------------------
        # EXTERNAL EVIDENCE VERIFICATION
        # ------------------------------------------

        evidence_results = {}

        if valid_claims:

            with st.spinner(
                "Verifying factual claims against external evidence..."
            ):

                verifier = get_verifier()
                explainer = get_explainer()

                for claim in valid_claims:

                    claim_id = claim["claim_id"]
                    claim_text = claim["claim"]

                    try:

                        verification = verifier.verify(
                            claim_id,
                            claim_text
                        )

                        explanation_input = dict(verification)

                        explanation_input["overall_relation"] = (
                            verification["final_relation"]
                        )

                        explanation = explainer.explain(
                            explanation_input
                        )

                        evidence_results[claim_id] = {
                            "verification": verification,
                            "explanation": explanation
                        }

                    except Exception as error:

                        evidence_results[claim_id] = {
                            "error": str(error)
                        }

        st.session_state.evidence_results = evidence_results

        st.success(
            "Verification pipeline execution finished!"
        )

    except Exception as error:

        # Do not display incomplete results as a successful execution.
        st.session_state.pipeline_output = None
        st.session_state.consistency_results = None
        st.session_state.consistency_error = None
        st.session_state.evidence_results = {}
        st.session_state.pipeline_mode = None

        st.error(
            f"Verification pipeline failed: {error}"
        )


# --------------------------------------------------
# DISPLAY VERIFICATION RESULTS
# --------------------------------------------------

if st.session_state.pipeline_output:

    data = st.session_state.pipeline_output

    # ----------------------------------------------
    # AI-GENERATED ANSWER
    # ----------------------------------------------

    st.divider()
    st.header("2. AI-Generated Answer")

    st.subheader("Original Answer")

    st.info(data["original_answer"])

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Generation Model", data["model"])

    with col2:
        st.metric(
            "Answer Words",
            len(data["original_answer"].split())
        )

    st.subheader("Independent Sample Answers")

    for sample in data["samples"]:

        with st.expander(f"Sample {sample['sample_id']}"):

            st.write(sample["answer"])

    st.caption(
        f"Successfully generated or loaded {len(data['samples'])} "
        "independent sample answers."
    )

    # ----------------------------------------------
    # FACTUAL CLAIM EXTRACTION
    # ----------------------------------------------

    st.divider()
    st.header("3. Factual Claim Extraction")

    st.write(
        "The generated answer is broken down into individual "
        "factual claims and checked for structural validity."
    )

    summary = data["claim_summary"]

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Claims", summary["claim_count"])
    col2.metric("Valid Claims", summary["valid_claim_count"])
    col3.metric("Invalid Claims", summary["invalid_claim_count"])

    for claim in data["claims"]:

        with st.expander(
            f"{claim['claim_id']} — {claim['claim']}"
        ):

            if claim.get("is_valid", True):
                st.success("Claim validation: VALID")
            else:
                st.warning("Claim validation: INVALID")

            st.write("**Source Sentences**")

            for sentence in claim.get("source_sentences", []):
                st.write(f"- {sentence}")

            st.write("**Extracted Entities**")

            st.json(claim.get("entities", []))

            if claim.get("issues"):
                st.write("**Validation Issues**")
                st.write(claim["issues"])

    # ----------------------------------------------
    # CONSISTENCY AND HALLUCINATION ANALYSIS
    # ----------------------------------------------

    st.divider()
    st.header("4. Consistency & Hallucination Analysis")

    st.write(
        "Analyses whether factual claims agree with independently "
        "generated answers using SelfCheck, BERTScore and NLI."
    )

    consistency = st.session_state.consistency_results

    if consistency:

        st.metric(
            "Overall Experimental Risk Score",
            f"{consistency['overall_risk_score']}%"
        )

        st.caption(
            "This is an experimental disagreement score, "
            "not a calibrated probability of hallucination."
        )

        st.write(consistency["interpretation"])

        consistency_map = {
            item["claim_id"]: item
            for item in consistency["results"]
        }

        for claim in data["claims"]:

            claim_id = claim["claim_id"]

            if claim_id not in consistency_map:
                continue

            result = consistency_map[claim_id]

            with st.expander(
                f"{claim_id} — Consistency Results"
            ):

                st.write(result["claim"])

                combined = result["combined_score"]

                st.metric(
                    "Combined Experimental Risk",
                    f"{combined['risk_score']}%"
                )

                st.write("**Risk Components**")
                st.json(combined["risk_components"])

                st.write("**Scoring Weights**")
                st.json(combined["weights"])

                st.write("**SelfCheck Results**")
                st.json(result["selfcheck"])

                st.write("**BERTScore Results**")
                st.json(result["bertscore"])

                st.write("**NLI Diagnostic Results**")
                st.json(result["nli"])

    elif st.session_state.consistency_error:

        st.warning(
            "Consistency analysis could not be completed: "
            f"{st.session_state.consistency_error}"
        )

    else:

        st.info("Consistency analysis was skipped.")

    # ----------------------------------------------
    # EXTERNAL EVIDENCE VERIFICATION
    # ----------------------------------------------

    st.divider()
    st.header("5. Evidence-Based Verification")

    st.write(
        "Each valid factual claim is checked against retrieved "
        "external evidence using Natural Language Inference."
    )

    evidence_results = st.session_state.evidence_results

    for claim in data["claims"]:

        claim_id = claim["claim_id"]

        if not claim.get("is_valid", True):

            st.warning(
                f"{claim_id}: Skipped because the claim failed validation."
            )

            continue

        if claim_id not in evidence_results:

            st.warning(
                f"{claim_id}: No evidence verification result available."
            )

            continue

        result = evidence_results[claim_id]

        st.subheader(claim_id)
        st.write(claim["claim"])

        if "error" in result:

            st.error(
                f"Evidence verification failed: {result['error']}"
            )

            st.divider()
            continue

        verification = result["verification"]
        explanation = result["explanation"]

        relation = verification["final_relation"]

        if relation == "supported":
            st.success("Verdict: SUPPORTED")

        elif relation == "contradicted":
            st.error("Verdict: CONTRADICTED")

        else:
            st.warning("Verdict: INSUFFICIENT EVIDENCE")

        st.write(
            "**Explanation:**",
            explanation["explanation"]
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Evidence Passages",
                verification["evidence_count"]
            )

        with col2:

            st.metric(
                "Adaptive Retrieval",
                "Yes" if verification["expanded"] else "No"
            )

        st.write("**NLI Relation Counts**")

        st.json(verification["relation_counts"])

        # ------------------------------------------
        # TEMPORARY DIAGNOSTIC OUTPUT
        # ------------------------------------------

        with st.expander(
            f"{claim_id} — Diagnostic: Raw NLI Evidence"
        ):

            st.write("**Raw NLI Evidence Results**")

            st.json(verification.get("evidence", []))

            st.write("**Independent Source Counts**")

            st.json(
                verification.get("independent_sources", {})
            )

            st.write("**Final Verification Details**")

            st.json(verification)

        # ------------------------------------------
        # EVIDENCE SOURCE SUMMARIES
        # ------------------------------------------

        st.write("**Retrieved Evidence Sources**")

        evidence_summaries = explanation.get(
            "evidence_summaries",
            []
        )

        if evidence_summaries:

            for item in evidence_summaries:

                title = item.get("title") or "Untitled source"

                with st.expander(
                    f"{title} — {item.get('relation', 'unknown')}"
                ):

                    st.write(
                        "Source:",
                        item.get("source", "Unknown")
                    )

                    if item.get("url"):

                        st.markdown(
                            f"[Open Source]({item['url']})"
                        )

                    st.write(
                        "Entailment:",
                        item.get("entailment")
                    )

                    st.write(
                        "Contradiction:",
                        item.get("contradiction")
                    )

                    st.write(
                        "Neutral:",
                        item.get("neutral")
                    )

        else:

            st.info(
                "No usable evidence summaries were returned."
            )

        st.divider()

    # ----------------------------------------------
    # FINAL VERIFICATION SUMMARY
    # ----------------------------------------------

    st.divider()
    st.header("6. Verification Summary")

    st.write("**Project:** VeriFact AI")

    st.write(
        "**Execution Mode:**",
        st.session_state.pipeline_mode
    )

    st.write(
        "**Schema Version:**",
        data.get("schema_version", "1.0")
    )

    st.write("**Question:**", data["question"])

    st.write(
        "**Claims Processed:**",
        len(data["claims"])
    )

    consistency_status = (
        "Completed"
        if st.session_state.consistency_results is not None
        else "Failed or Skipped"
    )

    valid_claim_count = sum(
        1
        for claim in data["claims"]
        if claim.get("is_valid", True)
    )

    evidence_success_count = sum(
        1
        for result in evidence_results.values()
        if "verification" in result
    )

    evidence_error_count = sum(
        1
        for result in evidence_results.values()
        if "error" in result
    )

    st.write(
        "**Consistency Analysis:**",
        consistency_status
    )

    st.write(
        "**Evidence Verification:**",
        f"{evidence_success_count}/{valid_claim_count} successful, "
        f"{evidence_error_count} errors"
    )

    if (
        st.session_state.consistency_results is not None
        and evidence_success_count == valid_claim_count
        and evidence_error_count == 0
    ):

        st.success(
            "All verification stages completed successfully."
        )

    else:

        st.warning(
            "The available results are displayed above. "
            "Some verification stages may have been skipped "
            "or encountered errors."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "VeriFact AI | AI Hallucination Detection "
    "and Evidence-Based Fact Verification"
)
