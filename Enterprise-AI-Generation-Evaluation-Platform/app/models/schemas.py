from pydantic import BaseModel, Field

class BrandRequest(BaseModel):
    brand_name: str
    tone: str = 'professional, clear and friendly'
    forbidden_terms: list[str] = []
    required_terms: list[str] = []
    safety_rules: list[str] = []

class PromptRequest(BaseModel):
    name: str = 'brand-generation'
    version: int = Field(ge=1)
    system_instruction: str
    active: bool = False

class GenerateRequest(BaseModel):
    brand_name: str
    question: str
    top_k: int = Field(default=5, ge=1, le=10)
    task: str = 'general'
    model: str | None = None
    prompt_version: int | None = None

class EvaluationRequest(BaseModel):
    brand_name: str
    answer: str
    source_texts: list[str] = []
