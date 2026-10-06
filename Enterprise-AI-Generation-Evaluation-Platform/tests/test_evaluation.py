from app.services.evaluation import safety_check, groundedness, quality_score

def test_safety():
    assert safety_check('This is clean',['badword'])[0]
    assert not safety_check('This contains badword',['badword'])[0]

def test_groundedness():
    score=groundedness('The premium product is available today',[{'content':'Our premium product is available today.'}])
    assert score > 0.5

def test_quality():
    assert quality_score('answer',[{'content':'source'}],True)==1.0
