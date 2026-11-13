from app.services.insights import generate_insights

def test_high_form_abandonment_creates_recommendation():
    overview={"form_abandonment_rate":48,"email_click_rate":12,"email_opens":100}
    result=generate_insights(overview,[],[{"step":"page_view","sessions":100},{"step":"form_start","sessions":80}])
    assert result["insights"][0]["severity"]=="high"
    assert "shorter form" in result["insights"][0]["recommendation"]
