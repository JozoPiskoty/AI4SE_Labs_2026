from typing import Literal

from pydantic import BaseModel, Field


class CandidateRequirement(BaseModel):
    name: str = Field(description="Short descriptive requirement name")
    category: str = Field(description="Functional, non-functional, constraint, security, business rule, or other")
    statement: str = Field(description="A single requirement, preferably testable and beginning with System shall")
    priority: Literal["P1", "P2", "P3", "P4"] = "P3"
    priority_rationale: str = ""
    priority_is_estimated: bool = True
    source_documents: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    confidence: str = "medium"
    candidate_refs: list[str] = Field(default_factory=list)


class RejectedCandidate(BaseModel):
    description: str
    source_documents: list[str] = Field(default_factory=list)
    reason: str
    related_requirements: list[str] = Field(default_factory=list)
    human_review_required: bool = False
    candidate_refs: list[str] = Field(default_factory=list)


class CoverageNote(BaseModel):
    source_document: str
    note: str


class ExtractionResult(BaseModel):
    candidates: list[CandidateRequirement] = Field(default_factory=list)
    rejected: list[RejectedCandidate] = Field(default_factory=list)
    coverage_notes: list[CoverageNote] = Field(default_factory=list)


class ConsolidatedRequirement(CandidateRequirement):
    related_questions: list[str] = Field(default_factory=list)
    candidate_refs: list[str] = Field(
        min_length=1,
        description="IDs of all input candidates represented by this requirement",
    )


class ConsolidationResult(BaseModel):
    requirements: list[ConsolidatedRequirement] = Field(default_factory=list)
    rejected: list[RejectedCandidate] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)


class ReviewFinding(BaseModel):
    issue: str
    repair_target: Literal["extract", "consolidate", "human", "none"] = "human"
    evidence: list[str] = Field(default_factory=list)
    affected_requirement_ids: list[str] = Field(default_factory=list)
    affected_candidate_refs: list[str] = Field(default_factory=list)


class DuplicateGroup(BaseModel):
    requirement_ids: list[str] = Field(min_length=2)
    rationale: str
    evidence: list[str] = Field(default_factory=list)


class ReviewResult(BaseModel):
    approved: bool
    findings: list[ReviewFinding] = Field(default_factory=list)
    duplicate_groups: list[DuplicateGroup] = Field(default_factory=list)
    missing_requirements: list[CandidateRequirement] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)
    coverage_notes: list[CoverageNote] = Field(default_factory=list)
    rejected: list[RejectedCandidate] = Field(default_factory=list)
