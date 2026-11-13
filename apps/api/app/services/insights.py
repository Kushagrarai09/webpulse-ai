def generate_insights(overview: dict, form_rows: list, funnel_rows: list):
    insights=[]
    if overview["form_abandonment_rate"]>=35:
        insights.append({"severity":"high","title":"Form abandonment may be hurting conversion","finding":f"{overview['form_abandonment_rate']}% of started forms are not completed in the selected period.","recommendation":"Review fields with the highest drop-off, remove non-essential questions, and test a shorter form.","metric":"form_abandonment_rate"})
    if overview["email_click_rate"]<10 and overview["email_opens"]>0:
        insights.append({"severity":"medium","title":"Email engagement has room to improve","finding":f"Click-to-open rate is {overview['email_click_rate']}%.","recommendation":"Test clearer calls to action, segment audiences by intent, and align email content with the landing page.","metric":"email_click_rate"})
    if len(funnel_rows)>=2 and funnel_rows[1]["sessions"]<funnel_rows[0]["sessions"]*.5:
        insights.append({"severity":"medium","title":"Large drop between page view and form start","finding":"Fewer than half of page-view sessions proceed to start a form.","recommendation":"Make the primary call to action more visible and check page load time and message clarity.","metric":"funnel"})
    if not insights: insights.append({"severity":"info","title":"No major rule-based issues detected","finding":"Current metrics did not cross the MVP's alert thresholds.","recommendation":"Compare performance by device, channel, landing page, and visitor segment to find smaller opportunities.","metric":"overview"})
    return {"generated_by":"WebPulse rules engine","disclaimer":"Recommendations are hypotheses; validate with experiments.","insights":insights}
