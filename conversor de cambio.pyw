import importlib.util
import tkinter as tk
from tkinter import ttk, messagebox

if importlib.util.find_spec('requests') is not None:
    print('tudo certo')
else:
    try:
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível instalar a biblioteca 'requests': {e}")
        sys.exit(1)

import requests

API_KEY = 'fca_live_dX0jAVjgZnQ8aTSHHAwBcLtuSrqYMyIEBnreN0Fr'
Url = f'https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}'
#PARAM_CONV = '&currencies=EUR%2CUSD%2CEUR&base_currency=BRL'

janelas = []

def cria_janela(titulo: str = "Minha Janela", largura: int = 400, altura: int = 300, maximizado: bool = False, centralizado: bool = True, resizable: bool = True):
    janela = tk.Tk()
    janela.title(titulo)
    janela.resizable(resizable, resizable)  
    if centralizado:
        posX = janela.winfo_screenwidth() // 2 - largura // 2
        posY = janela.winfo_screenheight() // 2 - altura // 2
    else:
        posX = 0
        posY = 0
    janela.geometry(f"{largura}x{altura}+{posX}+{posY}")
    if maximizado:
        janela.state('zoomed')
    janelas.append(janela)
    return janela

MainWindow = cria_janela(titulo= 'Conversor de câmbio', largura= 300, altura= 300, resizable=False, centralizado=True)
SecondaryWindow = cria_janela(titulo= 'Conversor de câmbio 2', largura= 300, altura= 300, resizable=False, centralizado=True)

def converter_moeda():
    try:
        busca = requests.get(f'{Url}&currencies={selector_de_moeda_sai.get()}&base_currency={selector_de_moeda_entra.get()}')
        retorno = busca.json()
        paraValor = retorno.get('data', {}).get(f'{selector_de_moeda_sai.get()}')
        finalVAlor = float(entrada_valor.get()) * paraValor
        resultado_label.config(text=f'{float(entrada_valor.get())} {selector_de_moeda_entra.get()} = {round(finalVAlor, 2)} {selector_de_moeda_sai.get()}', font=('Arial', 12))
    except requests.exceptions.RequestException as e:
        resultado_label.config(text=f"Erro ao buscar dados da API: {e}", font=('Arial', 9))
    except ValueError:
        resultado_label.config(text="Erro ao converter o valor, verifique a entrada. Use apenas números e \".\"", font=('Arial', 9))

TitleLabel = ttk.Label(MainWindow, text='Conversor de Câmbio', font=('Arial', 16))
TitleLabel.pack(pady=10)

grid_frame = ttk.Frame(MainWindow)
grid_frame.pack(pady=10)

label1 = ttk.Label(grid_frame, text='Valor:')
label1.grid(row=0, column=0, padx=5, pady=5)

entrada_valor = ttk.Entry(grid_frame, width=10)
entrada_valor.grid(row=0, column=2, padx=5, pady=5)

label2 = ttk.Label(grid_frame, text='De:')
label2.grid(row=1, column=0, padx=5, pady=5)

selector_de_moeda_entra = ttk.Combobox(grid_frame, textvariable='entrada' ,values=['BRL', 'USD', 'EUR', 'JPY', 'RUB', 'AUD', 'CAD', 'CNY', 'HKD', 'INR', 'KRW', 'MXN', 'ZAR'], width=10)
selector_de_moeda_entra.set('BRL')
selector_de_moeda_entra['state'] = 'readonly'
selector_de_moeda_entra.grid(row=1, column=2, padx=5, pady=5)

label3 = ttk.Label(grid_frame, text='Para:')
label3.grid(row=2, column=0, padx=5, pady=5)

selector_de_moeda_sai = ttk.Combobox(grid_frame, textvariable='saida' ,values=['BRL', 'USD', 'EUR', 'JPY', 'RUB', 'AUD', 'CAD', 'CNY', 'HKD', 'INR', 'KRW', 'MXN', 'ZAR'], width=10)
selector_de_moeda_sai.set('BRL')
selector_de_moeda_sai['state'] = 'readonly'
selector_de_moeda_sai.grid(row=2, column=2, padx=5, pady=5)

botao_converter = ttk.Button(MainWindow, text='Converter', command=lambda: converter_moeda())
botao_converter.pack(pady=10)

resultado_label = ttk.Label(MainWindow, text='', font=('Arial', 12), wraplength=250, justify='center')
resultado_label.pack(pady=10)

for janela in janelas:
    janela.mainloop()
