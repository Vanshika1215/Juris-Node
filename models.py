from pydantic import BaseModel, Field
from typing import List

class ClauseAnalysis(BaseModel):
    clause_title: str = Field(description="The formal title or heading of the contract clause.")
    extracted_text: str = Field(description="The exact raw text sentence or paragraph parsed from the contract document.")
    risk_level: str = Field(description="Must be strictly classified as one of these strings: 'Standard', 'Caution', or 'Critical'.")
    reason: str = Field(description="A 1-2 sentence detailed breakdown explaining why this specific risk category was assigned.")

class ContractAnalysisResponse(BaseModel):
    contract_name: str = Field(default="Unknown", description="The original uploaded filename.")
    overall_safety_score: int = Field(description="An aggregated safety assessment score between 0 and 100.")
    executive_summary: str = Field(description="A clean, plain-English 2-3 sentence overview paragraph outlining the contract.")
    recommendations: List[str] = Field(description="A list of 2-4 actionable, high-priority specific negotiation tip elements.")
    clauses: List[ClauseAnalysis] = Field(description="The complete sequence array of broken down contract clauses.")