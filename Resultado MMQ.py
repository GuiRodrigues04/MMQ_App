import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def open_result(d):
    # Função que cria uma tabela 2xN com dicionário de entrada
    def tabelayx2(janela, dic, color, font):
        lista = list(dic.keys())
        tabela = tk.Frame(janela)
        for i in lista:
            c1 = color[0]
            c2 = color[1]
            fundo = tk.Canvas(tabela, width=140, height=40, highlightbackground=color[4])
            fundo.grid(column=1, row=lista.index(i), sticky='EWNS')
            fundo2 = tk.Canvas(tabela, width=120, height=40, highlightbackground=color[4])
            fundo2.grid(column=2, row=lista.index(i), sticky='EWNS')
            if lista.index(i) % 2 == 0:
                c1 = color[2]
                c2 = color[3]
            fundo['background'] = c1
            fundo2['background'] = c2
            label = ttk.Label(tabela, text=i, background=c1, font=font)
            label.grid(column=1, row=lista.index(i))
            if dic[i] == '*':
                label2 = ttk.Label(tabela, text=dic[i], background=c2, font=font)
            else:
                label2 = ttk.Label(tabela, text="%.4f" % dic[i], background=c2, font=font)
            label2.grid(column=2, row=lista.index(i))
        return tabela

    Resultado = tk.Tk()

    Resultado.configure(background='white')
    Resultado.geometry('1100x800')

    # Note dos graficos
    Note = ttk.Notebook(Resultado)
    Note.pack()

    # Frame de graficos
    Graficos = tk.Frame(Resultado, background='white')
    Graficos.pack()

    # criação do grafico de MMQ
    fig, mmq = plt.subplots(figsize=(8, 5))
    mmq.scatter([float(i) for i in d[0]['variaveis_X']], [float(i) for i in d[0]['variaveis_y']], label='Dados reais')
    mmq.plot(
        [(min(d[0]['variaveis_X'])) * -1.5, (max(d[0]['variaveis_X'])) * 1.5],
        [d[0]['variavel_a'] * ((min(d[0]['variaveis_X'])) * -1.5) + d[0]['variavel_b'],
         d[0]['variavel_a'] * ((max(d[0]['variaveis_X'])) * 1.5)
         + d[0]['variavel_b']],
        color='C1',
        label='Reta MMQ'
    )
    a = f"%.3f" % d[0]['variavel_a']
    b = f"%.3f" % d[0]['variavel_b']

    mmq.set_title(f'Y = {a} * X + {b}')
    mmq.axis([0, (max(d[0]['variaveis_X'])) * 1.1, 0, (max(d[0]['variaveis_y']) * 1.1)])
    mmq.grid(True)
    mmq.legend()

    # Colocando Grafico MMQ na janela
    canva = FigureCanvasTkAgg(fig, Graficos)
    canva.get_tk_widget().grid(column=2, columnspan=2, row=1, rowspan=2)

    # Grafico de incerteza normal
    labels_U1 = ['Ux', 'Uy']
    color_U1 = ['#048200', '#698269']
    sizes = [1]
    if len(d[0]['Incertezas_Y']) > 1:
        sizes = [(sum(d[0]['Incertezas_X'])) / len(d[0]['Incertezas_X']),
                 (sum(d[0]['Incertezas_Y'])) / len(d[0]['Incertezas_Y'])]
    elif (d[0]['Incertezas_X'])[0] == 0 and (d[0]['Incertezas_Y'])[0] == 0:
        color_U1 = ['#5d5f60']
        labels_U1 = ['*']
    else:
        sizes = [(d[0]['Incertezas_X'])[0], (d[0]['Incertezas_Y'])[0]]
    fig2, ax2 = plt.subplots(figsize=(3, 3))
    ax2.pie(sizes, autopct='%1.1f%%', shadow=False, startangle=90, colors=color_U1)
    ax2.legend(labels_U1)
    ax2.axis('equal')

    # Colocando grafico de Incerteza normal na janela
    canva2 = FigureCanvasTkAgg(fig2, Graficos)
    canva2.get_tk_widget().grid(column=3, row=3)

    # Criando graficos de incertezas ao quadrado
    labels_U2 = ['Ux²', 'Uy²']
    colors_U2 = ['#720000', '#bc6a90']
    sizes = [1]
    if len(d[0]['Incertezas_Y']) > 1:
        sizes = [((sum(d[0]['Incertezas_X']))/len(d[0]['Incertezas_X']))**2,
                 ((sum(d[0]['Incertezas_Y']))/len(d[0]['Incertezas_Y']))**2]
    elif (d[0]['Incertezas_X'])[0] == 0 and (d[0]['Incertezas_Y'])[0] == 0:
        colors_U2 = ['#5d5f60']
        labels_U2 = ['*']
    else:
        sizes = [(d[0]['Incertezas_X'])[0]**2, (d[0]['Incertezas_Y'])[0]**2]
    fig1, ax1 = plt.subplots(figsize=(3, 3))
    ax1.pie(sizes, autopct='%1.1f%%', shadow=False, startangle=90, colors=colors_U2)
    ax1.legend(labels_U2)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Colocando grafico de icertezas ao quadrado na janela
    canva1 = FigureCanvasTkAgg(fig1, Graficos)
    canva1.get_tk_widget().grid(column=2, row=3)

    # colocando dados e criando a tabela
    tabelayx2(
        Graficos,
        d[1],
        ['#ffac84', '#ffac84', '#ff9684', '#ff9684', 'white'],
        'Arial 12'
    ).grid(column=1, row=1, rowspan=3, padx=5)

    # criando Frame com Tabelas do "mais dados"
    dados = tk.Frame(Note, background='white')
    dados.pack()
    # criando lista com x's y's ux's uy's e xy
    lista_treeview = []
    ux = 0
    uy = 0
    ys = 0
    xy = 0
    variaveis_geral = []
    for i in (d[0]['variaveis_X']):
        alk = []
        alk.append(i)
        if len(d[0]['Incertezas_X']) > 1:
            alk.append((d[0]['Incertezas_X'])[ux])
            ux += 1
        else:
            alk.append((d[0]['Incertezas_X'])[0])
        alk.append((d[0]['variaveis_y'])[ys])
        ys += 1
        if len(d[0]['Incertezas_X']) > 1:
            alk.append((d[0]['Incertezas_Y'])[uy])
            uy += 1
        else:
            alk.append((d[0]['Incertezas_Y'])[0])
        alk.append((d[0]['lista_xy'])[xy])
        xy += 1
        variaveis_geral.append(alk)
    print(variaveis_geral)

    # cirnado tabela de x's e y's
    treeview = ttk.Treeview(
        dados,
        columns=['Xs', 'Uxs', 'Ys', 'Uys', 'XYs'],
        show='headings',
        height=30
    )
    treeview.column('Xs', width=100, minwidth=100)
    treeview.heading('Xs', text='X\'s')

    treeview.column('Uxs', width=100, minwidth=100)
    treeview.heading('Uxs', text='Ux\'s')

    treeview.column('Ys', width=100, minwidth=100)
    treeview.heading('Ys', text='Y\'s')

    treeview.column('Uys', width=100, minwidth=100)
    treeview.heading('Uys', text='Uy\'s')

    treeview.column('XYs', width=100, minwidth=100)
    treeview.heading('XYs', text='XY\'s')
    treeview.pack()

    # Adicionando Graficos ao note
    Note.add(Graficos, text='Graficos')
    Note.add(dados, text='Mais Dados')

    Resultado.mainloop()

open_result([{'variaveis_X': [1.0, 2.0, 3.0], 'variaveis_y': [2.0, 3.0, 4.0], 'Incertezas_X': [0.0], 'somatorio_xs': 6.0, 'lista_xs2': [1.0, 4.0, 9.0], 'somatorio_xs²': 14.0, 'lista_xy': [2.0, 6.0, 12.0], 'somatorio_xy': 20.0, 'somatorio_ys': 9.0, 'variavel_n': 3.0, 'variavel_delta': 6.0, 'variavel_a': 1.0, 'variavel_b': 1.0, 'incerteza_a': 0.0, 'incerteza_b': 0.0, 'alinha': '*', 'ualinha': '*', 'blinha': '*', 'ublinha': '*', 'lista_ws': '*', 'lista_wx': '*', 'lista_wxy': '*', 'lista_wx2': '*', 'lista_wy': '*', 'Incertezas_Y': [0.0], 'Incertezas_Juntas_sla': '*', 'lista_de_residuos': [0.0, 0.0, 0.0], 'residuo_total': 0.0}, {'variavel_a': 1.0, 'incerteza_a': 0.0, 'variavel_b': 1.0, 'incerteza_b': 0.0, 'somatorio_xs': 6.0, 'somatorio_xs²': 14.0, 'somatorio_xy': 20.0, 'somatorio_ys': 9.0, 'variavel_n': 3.0, 'variavel_delta': 6.0, 'alinha': '*', 'ualinha': '*', 'blinha': '*', 'ublinha': '*'}]
)