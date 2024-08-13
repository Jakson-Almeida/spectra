import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

# Função para ler os dados do arquivo e retornar duas listas: frequência e ganho
def ler_dados_arquivo(caminho_arquivo):
    frequencias = []
    ganhos = []
    
    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            # Separar a linha pelos pontos e vírgulas
            dados = linha.strip().split(';')
            if len(dados) == 2:
                # Converter os valores para float e adicionar às listas
                frequencias.append(float(dados[0]))
                ganhos.append(float(dados[1]))
    
    return frequencias, ganhos

# Função para plotar os dados
def plotar_espectro(frequencias, ganhos):
    plt.figure(figsize=(10, 6))
    plt.plot(frequencias, ganhos, label='Espectro')
    plt.xlabel('Frequência')
    plt.ylabel('Ganho')
    plt.title('Espectro de Frequência')
    plt.legend()
    plt.grid(True)
    plt.show()

# Função para selecionar o arquivo e plotar o espectro
def selecionar_arquivo_e_plotar():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    caminho_arquivo = filedialog.askopenfilename(title="Selecione o arquivo de espectro", filetypes=[("Text Files", "*.txt")])
    
    if caminho_arquivo:
        frequencias, ganhos = ler_dados_arquivo(caminho_arquivo)
        plotar_espectro(frequencias, ganhos)

# Menu principal
if __name__ == "__main__":
    selecionar_arquivo_e_plotar()
