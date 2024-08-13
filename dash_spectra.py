import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import os

# Inicializa a aplicação Dash
app = dash.Dash(__name__)

# Função para ler os dados do arquivo e retornar um DataFrame
def ler_dados_arquivo(caminho_arquivo):
    try:
        df = pd.read_csv(caminho_arquivo, delimiter=';', header=None, names=['Frequencia', 'Ganho'])
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        df = pd.DataFrame(columns=['Frequencia', 'Ganho'])
    return df

# Layout da aplicação
app.layout = html.Div([
    html.H1("Visualizador de Espectro"),
    dcc.Input(id='input-path', type='text', placeholder='Endereço do arquivo', style={'width': '50%'}),
    html.Button('Carregar Arquivo', id='load-button', n_clicks=0),
    dcc.Graph(id='spectro-plot'),
    html.Div(id='error-message', style={'color': 'red'})
])

# Callback para atualizar o gráfico
@app.callback(
    [Output('spectro-plot', 'figure'), Output('error-message', 'children')],
    [Input('load-button', 'n_clicks')],
    [State('input-path', 'value')]
)
def update_graph(n_clicks, caminho_arquivo):
    if not caminho_arquivo or not os.path.exists(caminho_arquivo):
        return go.Figure(), "Arquivo não encontrado ou caminho inválido."

    df = ler_dados_arquivo(caminho_arquivo)
    if df.empty:
        return go.Figure(), "Erro ao ler o arquivo ou arquivo vazio."

    figure = {
        'data': [
            go.Scatter(
                x=df['Frequencia'],
                y=df['Ganho'],
                mode='lines',
                name='Espectro'
            )
        ],
        'layout': go.Layout(
            title='Espectro de Frequência',
            xaxis={'title': 'Frequência'},
            yaxis={'title': 'Ganho'},
            hovermode='closest'
        )
    }

    return figure, ""

# Executa a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)
