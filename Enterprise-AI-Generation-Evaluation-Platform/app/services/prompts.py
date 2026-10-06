from app.db.repository import get_prompt

def build_prompt(question, context, brand, prompt_version=None):
    prompt=get_prompt('brand-generation',prompt_version)
    if not prompt: raise ValueError('Prompt version not found')
    brand_rules=f"Brand: {brand['brand_name']}\nTone: {brand['tone']}\nForbidden terms: {', '.join(brand['forbidden_terms']) or 'none'}\nRequired terms: {', '.join(brand['required_terms']) or 'none'}\nSafety rules: {', '.join(brand['safety_rules']) or 'standard safety'}"
    text=f"""{prompt['system_instruction']}\n\nBRAND RULES:\n{brand_rules}\n\nRETRIEVED CONTEXT:\n{context or 'No retrieved context.'}\n\nUSER REQUEST:\n{question}\n\nReturn only the final answer."""
    return prompt['version'],text
