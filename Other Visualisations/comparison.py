import plotly.express as px
import pandas as pd

#Funktion som gör ett lexikon av varje panel och dess scores
#När vi är klara med alla funktioner för att räkna ut scores kan man ju ropa på dom 
#funktionerna i denna funktion, istället för att skicka in alla scores som inputs
def panel_scores(panelnr, spr, tac, red):
    pan = {}
    pan['Panel nr.'] = str(panelnr)
    pan['Spridning'] = spr
    pan['Täckning'] = tac
    pan['Redundans'] = red
    return pan

#Plottar bars
def compare_plot(panels):
    fig = px.bar(panels, x="Panel nr.", y=["Spridning", "Täckning", "Redundans"], 
                color_discrete_sequence = ['Teal', 'RebeccaPurple', 'DarkSeaGreen'],
                barmode='group', range_y = [0,1])
    fig.update_layout(
    title='Jämförelse av testpaneler',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Score',
        titlefont_size=16,
        tickfont_size=14),
        template = 'plotly_dark')
    fig.show()

def main():
    compare_plot(pd.DataFrame(data = (panel_scores(1, 0.3, 0.7, 0.4), 
                                    panel_scores(2, 0.2, 0.9, 0.7))))

if __name__ == '__main__':
    main()

