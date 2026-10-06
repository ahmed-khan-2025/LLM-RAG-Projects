import re

def safety_check(text, forbidden_terms):
    lower=text.lower()
    hits=[t for t in forbidden_terms if t.lower() in lower]
    return len(hits)==0, hits

def groundedness(text, sources):
    if not sources: return 0.0
    source_words=set(re.findall(r'\b[a-zA-Z]{5,}\b',' '.join(s['content'] for s in sources).lower()))
    answer_words=set(re.findall(r'\b[a-zA-Z]{5,}\b',text.lower()))
    if not answer_words: return 0.0
    return round(len(answer_words & source_words)/len(answer_words),4)

def quality_score(text, sources, safety_pass):
    score=0.0
    if text.strip(): score += 0.4
    if sources: score += 0.3
    if safety_pass: score += 0.3
    return round(score,4)
