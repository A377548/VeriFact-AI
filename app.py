
import streamlit as st

from generation.response_generator import ResponseGenerator
from claim_extraction.claim_pipeline import ClaimExtractionPipeline
from explanation.adaptive_verifier import AdaptiveEvidenceVerifier
from explanation.claim_explainer import ClaimExplainer


st.set_page_config(
    page_title="VeriFact AI",
    page_icon="🔍",
    layout="wide"
)


# -------------------------------
# Page Header
# -------------------------------

st.title("🔍 VeriFact AI")
st.subheader("AI-powered factual claim verification")

st.write(
    "Generate an AI answer, extract factual claims, "
    "retrieve external evidence and examine whether "
    "the evidence supports or contradicts each claim."
)

st.divider()


# -------------------------------
# Question Input
# -------------------------------

with st.form("verification_form"):

    question = st.text_area(
        "Enter your question",
        placeholder="Example: Does the Earth revolve around the Sun?",
        height=100
    )

    submitted = st.form_submit_button(
        "Verify Answer",
        type="primary",
        use_container_width=True
    )


# -------------------------------
# Main Verification Process
# -------------------------------

if submitted:

    if not question.strip():
        st.warning("Please enter a question first.")

    else:

        try:

            # Step 1: Generate original answer

            with st.spinner("Generating the AI answer..."):

                response_generator = ResponseGenerator()

                original_result = (
                    response_generator.generate_original_response(
                        question.strip()
                    )
                )

                original_answer = original_result["answer"]


            # Step 2: Extract claims

            with st.spinner("Extracting factual claims..."):

                claim_pipeline = ClaimExtractionPipeline()

                claim_result = claim_pipeline.process_answer(
                    original_answer
                )

                claims = claim_result["claims"]


            # Step 3: Separate valid and invalid claims

            valid_claims = [
                claim for claim in claims
                if claim.get("is_valid", True)
                and isinstance(claim.get("claim"), str)
                and claim["claim"].strip()
            ]

            invalid_claims = [
                claim for claim in claims
                if claim not in valid_claims
            ]


            # Step 4: Adaptive evidence verification

            verification_output = {
                "results": []
            }

            if valid_claims:

                with st.spinner(
                    "Retrieving evidence and verifying claims. "
                    "This may take a little while..."
                ):

                    adaptive_verifier = AdaptiveEvidenceVerifier()

                    verification_output = (
                        adaptive_verifier.process(valid_claims)
                    )


            # Step 5: Display original answer

            st.divider()
            st.header("1. Original AI Answer")

            st.info(original_answer)


            # Step 6: Display claim summary

            st.header("2. Claim Extraction Summary")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total Claims",
                claim_result["claim_count"]
            )

            col2.metric(
                "Valid Claims",
                claim_result["valid_claim_count"]
            )

            col3.metric(
                "Invalid Claims",
                claim_result["invalid_claim_count"]
            )


            # Step 7: Verification results

            st.header("3. Evidence-Based Verification")

            results = verification_output.get("results", [])

            supported = 0
            contradicted = 0
            uncertain = 0
            errors = 0

            for result in results:

                relation = result.get(
                    "final_relation",
                    "verification_error"
                )

                if relation == "supported":
                    supported += 1

                elif relation == "contradicted":
                    contradicted += 1

                elif relation == "verification_error":
                    errors += 1

                else:
                    uncertain += 1


            # Verification metrics

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Supported", supported)
            col2.metric("Contradicted", contradicted)
            col3.metric("Insufficient Evidence", uncertain)
            col4.metric("Errors", errors)


            # Overall summary

            if contradicted > 0:

                st.warning(
                    "Some claims have evidence classified as "
                    "contradicting them. Review the evidence below."
                )

            elif uncertain > 0:

                st.info(
                    "Some claims could not be verified with "
                    "sufficient evidence."
                )

            elif errors > 0:

                st.warning(
                    "Some claims encountered verification errors."
                )

            elif results:

                st.success(
                    "All processed claims were classified as supported "
                    "by the retrieved evidence."
                )

            else:

                st.info("No valid claims were available for verification.")


            # Step 8: Individual claim explanations

            st.header("4. Detailed Claim Analysis")

            explainer = ClaimExplainer()

            for result in results:

                relation = result.get(
                    "final_relation",
                    "verification_error"
                )

                claim_id = result.get("claim_id", "Unknown")
                claim_text = result.get("claim", "")

                # Adapt Phase 7 output to the explainer's input format.

                explanation_input = {
                    **result,
                    "overall_relation": relation
                }

                explanation = explainer.explain(
                    explanation_input
                )

                with st.expander(
                    f"{claim_id}: {claim_text}",
                    expanded=True
                ):

                    if relation == "supported":
                        st.success("Verdict: SUPPORTED")

                    elif relation == "contradicted":
                        st.error("Verdict: CONTRADICTED")

                    elif relation == "verification_error":
                        st.warning("Verdict: VERIFICATION ERROR")

                    else:
                        st.info(
                            "Verdict: INSUFFICIENT EVIDENCE"
                        )

                    st.write(explanation["explanation"])

                    st.write(
                        f"Evidence passages: "
                        f"{result.get('evidence_count', 0)}"
                    )

                    st.write(
                        f"Adaptive retrieval used: "
                        f"{'Yes' if result.get('expanded') else 'No'}"
                    )

                    # Display relation counts

                    relation_counts = result.get(
                        "relation_counts",
                        {}
                    )

                    if relation_counts:

                        st.write("NLI Evidence Classification:")

                        st.write(
                            f"- Entailment: "
                            f"{relation_counts.get('entailment', 0)}"
                        )

                        st.write(
                            f"- Contradiction: "
                            f"{relation_counts.get('contradiction', 0)}"
                        )

                        st.write(
                            f"- Neutral: "
                            f"{relation_counts.get('neutral', 0)}"
                        )


                    # Display evidence

                    evidence_items = explanation[
                        "evidence_summaries"
                    ]

                    if evidence_items:

                        st.markdown("**Retrieved Evidence**")

                        for index, evidence in enumerate(
                            evidence_items,
                            start=1
                        ):

                            st.markdown(
                                f"**Evidence {index}**"
                            )

                            st.write(
                                "Title:",
                                evidence.get("title") or "Not available"
                            )

                            st.write(
                                "Source:",
                                evidence.get("source") or "Not available"
                            )

                            st.write(
                                "NLI relation:",
                                evidence.get("relation") or "Not available"
                            )

                            if evidence.get("url"):
                                st.markdown(
                                    f"[Open Source]({evidence['url']})"
                                )

                            st.write(
                                "Entailment:",
                                evidence.get("entailment")
                            )

                            st.write(
                                "Contradiction:",
                                evidence.get("contradiction")
                            )

                            st.write(
                                "Neutral:",
                                evidence.get("neutral")
                            )

                            st.divider()

                    else:

                        st.info(
                            "No evidence passages were available."
                        )


            # Step 9: Invalid claims

            if invalid_claims:

                st.header("5. Claims Not Sent for Verification")

                st.caption(
                    "These claims were marked invalid during "
                    "claim extraction."
                )

                for claim in invalid_claims:

                    st.warning(
                        f"{claim.get('claim_id', 'Unknown')}: "
                        f"{claim.get('claim', 'No claim text')}"
                    )


            st.divider()

            st.caption(
                "VeriFact AI — Evidence-assisted claim verification. "
                "Model classifications are not guaranteed proof of truth."
            )


        except Exception as error:

            st.error(
                "The verification process could not be completed."
            )

            st.exception(error)


# -------------------------------
# Footer
# -------------------------------

st.divider()

st.caption(
    "VeriFact AI | AI Hallucination Detection and "
    "Evidence-Based Fact Verification"
)
