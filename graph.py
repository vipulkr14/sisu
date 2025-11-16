import plotly.graph_objects as go

categories=['assess_product_trust_score','license_scan_trust_score','virustotal_trust_score', 
            'certs_scan_trust_score', 'cve_trust_score', 'security_assessment_trust_score']

def create_graph(product, trust_scores):
    assess_product_trust_score = trust_scores["assess_product_trust_score"]
    license_scan_trust_score = trust_scores["license_scan_trust_score"]
    virustotal_trust_score = trust_scores["virustotal_trust_score"]
    certs_scan_trust_score = trust_scores["certs_scan_trust_score"]
    cve_trust_score = trust_scores["cve_trust_score"]
    security_assessment_trust_score = trust_scores["security_assessment_trust_score"] 
    print(security_assessment_trust_score)
    fig = go.Figure(data=go.Scatterpolar(
        r=[assess_product_trust_score, license_scan_trust_score, virustotal_trust_score, 
           certs_scan_trust_score, cve_trust_score, security_assessment_trust_score],
        theta=categories,
        fill='toself'
        ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
                ),
            ),
        showlegend=False
    )
    #fig.show()
    graph_path = "output/"+product+"_radar_chart.png"
    fig.write_image(graph_path)
    return graph_path