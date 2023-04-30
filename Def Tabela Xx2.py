import tkinter as tk
from tkinter import ttk


janela_com_tabela = tk.Tk()

g = {
    'variavel_a': 0.7, 'incerteza_a': 0.0632455532033676, 'variavel_b': -0.3, 'incerteza_b': 0.2720294101747089, 'somatorio_xs': 16.0,
     'somatorio_xs²': 74.0, 'somatorio_xy': 47.0, 'somatorio_ys': 10.0, 'variavel_n': 4.0, 'variavel_delta': 40.0
}

cores = ['#98ffc4', '#98ff9a', '#98ffc4', '#98ff9a']
font = ['Arial']


def tabelayx2(dic, colors, font):
    lista = list(dic.keys())
    Tabela = ttk.Frame()
    for i in lista:
        c1 = colors[0]
        c2 = colors[1]
        fundo = tk.Canvas(Tabela, width=140, height=40)
        fundo.grid(column=1, row=lista.index(i), sticky='EWNS')
        fundo2 = tk.Canvas(Tabela, width=120, height=40)
        fundo2.grid(column=2, row=lista.index(i), sticky='EWNS')
        if lista.index(i) % 2 == 0:
            c1 = colors[2]
            c2 = colors[3]
        fundo['background'] = c1
        fundo2['background'] = c2
        label = ttk.Label(Tabela, text=i, background=c1, font=font)
        label.grid(column=1, row=lista.index(i))
        label2 = ttk.Label(Tabela, text="%.4f" % dic[i], background=c2, font=font)
        label2.grid(column=2, row=lista.index(i))
    return Tabela


(tabelayx2(g, cores, ('Arial', 12))).pack()



janela_com_tabela.mainloop()
