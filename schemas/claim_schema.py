
from pydantic import BaseModel, Field, ConfigDict


class EntitySchema(BaseModel):
    """Represents a named entity found in a factual claim."""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1)
    label: str = Field(min_length=1)
    description: str | None = None


class ClaimSchema(BaseModel):
    """Represents one structured factual claim."""

    model_config = ConfigDict(extra="forbid")

    claim_id: str = Field(min_length=1)
    claim: str = Field(min_length=1)

    source_sentence_indices: list[int] = Field(min_length=1)
    source_sentences: list[str] = Field(min_length=1)

    entities: list[EntitySchema] = Field(default_factory=list)

    is_valid: bool
    issues: list[str] = Field(default_factory=list)


class ClaimSummarySchema(BaseModel):
    """Provides a summary of extracted and validated claims."""

    model_config = ConfigDict(extra="forbid")

    sentence_count: int = Field(ge=0)
    claim_count: int = Field(ge=0)
    valid_claim_count: int = Field(ge=0)
    invalid_claim_count: int = Field(ge=0)


class VeriFactOutputSchema(BaseModel):
    """Standard output shared by all VeriFact AI modules."""

    model_config = ConfigDict(extra="forbid")

    project: str = "VeriFact AI"
    schema_version: str = "1.0"

    question: str = Field(min_length=1)
    original_answer: str = Field(min_length=1)
    model: str = Field(min_length=1)

    samples: list[dict] = Field(default_factory=list)
    claims: list[ClaimSchema] = Field(default_factory=list)

    claim_summary: ClaimSummarySchema
