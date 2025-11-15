import plotly.graph_objects as go

categories=['param1','param2','param3', 'param4']

def create_graph(product, param1: int, param2: int, param3: int, param4:int):
    fig = go.Figure(data=go.Scatterpolar(
        r=[param1, param2, param3, param4],
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