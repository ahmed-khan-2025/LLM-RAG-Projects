from app.config import settings

def choose_model(task: str, preferred_model: str | None = None):
    if preferred_model:
        return preferred_model
    task=task.lower()
    if any(x in task for x in ['creative','campaign','copy','marketing']):
        return settings.default_model
    return settings.default_model
