import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from _utils import find_wlres, transmission_spectra

PLOT_WL_RES = True  # Definido para exibir o comprimento de onda ressonante

# Função para ler os dados do arquivo e retornar duas listas: frequência e ganho
def ler_dados_arquivo(caminho_arquivo):
    frequencias = []
    ganhos = []
    
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            for linha in arquivo:
                # Separar a linha pelos pontos e vírgulas
                dados = linha.strip().split(';')
                if len(dados) == 2:
                    # Converter os valores para float e adicionar às listas
                    frequencias.append(float(dados[0]))
                    ganhos.append(float(dados[1]))
    except FileNotFoundError:
        messagebox.showerror("Erro", f"O arquivo {caminho_arquivo} não foi encontrado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao ler o arquivo: {e}")
    
    return frequencias, ganhos

# Função para plotar os dados
def plotar_espectro(frequencias, ganhos):
    plt.figure(figsize=(10, 6))
    
    # Converter frequências para a mesma escala de wl_res
    frequencias_nm = np.array(frequencias) * 1e9  # Supondo que wl_res está em nanômetros (nm)
    
    plt.plot(frequencias_nm, ganhos, label='Espectro')

    if PLOT_WL_RES:
        # Converter listas para arrays numpy
        frequencias = np.array(frequencias)
        ganhos = np.array(ganhos)
        
        # Encontrar o comprimento de onda ressonante
        wl_res = find_wlres(frequencias, ganhos, lims=[1510e-9, 1586e-9], prominence=0.01)
        # Plotar o ponto de comprimento de onda ressonante
        err = np.abs(frequencias*1e9 - wl_res)
        loc = err == min(err)
        plt.plot(wl_res, ganhos[loc][0], 'ok', label='WL Res')  # Ponto ressonante
        print(f"wl_res: {wl_res}")
        print(f"Ganho: {ganhos[loc][0]}")
        print("")

    plt.xlabel('Frequência (nm)')
    plt.ylabel('Ganho')
    plt.title('Espectro de Frequência')
    plt.legend()
    plt.grid(True)
    plt.show()

# Função para selecionar o arquivo e atualizar o campo de entrada
def selecionar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(title="Selecione o arquivo de espectro", filetypes=[("Text Files", "*.txt")])
    if caminho_arquivo:
        entrada_endereco.delete(0, tk.END)
        entrada_endereco.insert(0, caminho_arquivo)
        atualizar_visualizacao()

# Função para atualizar a visualização do espectro
def atualizar_visualizacao():
    caminho_arquivo = entrada_endereco.get()
    frequencias, ganhos = ler_dados_arquivo(caminho_arquivo)
    if frequencias and ganhos:
        plotar_espectro(frequencias, ganhos)

# Criação da interface gráfica
root = tk.Tk()
root.title("Visualizador de Espectro")
root.geometry("500x250")

# Usando ttk para uma aparência melhor
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12))
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TEntry', font=('Helvetica', 12))

# Frame para organizar os widgets
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Label e campo de entrada para o endereço do arquivo
label_endereco = ttk.Label(frame, text="Endereço do arquivo:")
label_endereco.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

entrada_endereco = ttk.Entry(frame, width=40)
entrada_endereco.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

# Botão para selecionar o arquivo via gerenciador de arquivos
botao_selecionar = ttk.Button(frame, text="Selecionar Arquivo", command=selecionar_arquivo)
botao_selecionar.grid(row=1, column=1, padx=5, pady=5)

# Botão para atualizar a visualização
botao_atualizar = ttk.Button(frame, text="Atualizar Visualização", command=atualizar_visualizacao)
botao_atualizar.grid(row=2, column=0, columnspan=2, pady=10)

# Configuração de expansão das colunas
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=0)

# Inicia a interface
root.mainloop()
