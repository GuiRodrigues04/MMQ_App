import tkinter as tk
from tkinter import Tk, Text, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# variaveis usadas

C1 = '#fcf3e6'
C2 = '#262400'

# mlk.theme_use('default')
# funçoes usadas:


def mmq(y, x, j, k, key, key3):
    # y = texto entrada de Y's
    # x = texto entrada de X's
    # j = incerteza de Y
    # k = incerteza de X
    # key chave que prediz se iremos inverter as variaveis ou não
    # key2 chave que prediz se possuimos mais que uma incerteza ou não
    # key3 chave que prediz se possuimos incertezas significativas nas duas variaveis

    key2 = 0
    uyt = '*'
    # função que cria a lista de x's ao quadrado

    def quadrado(g):

        quad = []
        for i in g:
            quad.append(i ** 2)
        return quad

    # Pegando a lista de valores de y e x e transformando em float.

    while y.count("  ") != 0:
        y = y.replace("  ", " ")
    while x.count("  ") != 0:
        x = x.replace("  ", " ")

    y = y.replace(",", ".")
    x = x.replace(",", ".")
    ys1 = [float(i) for i in y.split(" ")]
    xs1 = [float(i) for i in x.split(" ")]

    # Verificando se o numero de Y's é o mesmo que de X's e aparecendo o erro.

    if float(len(xs1)) != float(len(ys1)):
        janelaerro = tk.Tk()
        erro = ttk.Label(janelaerro, text='ERRO, numero de variaveis diferente.')
        erro.pack()
        janelaerro.mainloop()
        return print('erro 1')

    # verificando as incertezas de x e y, se precisamos inverter os valores ou se temos
    # incertezas diferentes

    j = j.replace(",", ".")
    k = k.replace(",", ".")
    uy1 = [float(i) for i in j.split(" ")]
    ux1 = [float(i) for i in k.split(" ")]

    uy = uy1
    ux = ux1
    if len(uy1) == 1:
        uy = uy1[0]
    if len(ux1) == 1:
        ux = ux1[0]
    if len(uy1) > 1:
        if float(len(uy1)) != float(len(ys1)):
            janelaerro = tk.Tk()
            erro = ttk.Label(janelaerro, text='ERRO, quando temos mais que uma incerteza precisamos que o numero de'
                                              'incertezas seja igual ao numero de valores em y. (em quantidade).')
            erro.pack()
            janelaerro.mainloop()
            return print('erro 2')
        key2 = 1


    ys, xs = ys1, xs1
    if key == 1:
        ys, xs = xs1, ys1
        uy, ux = ux, uy

    # pegando o valor de n. (numero de medidas)

    n = float(len(xs))

    # criando a lista de x * y

    kl = 0
    xy = []
    for i in xs:
        xy.append(i * ys[kl])
        kl += 1

    # criando a lista de w * x * y, w * x, w * y, w * x^2
    # w = 1 / u

    ws = "*"
    wxy = "*"
    wx = "*"
    wx2 = "*"
    wy = "*"

    for q in range(key3 + 1):
        if key2 == 1:
            ws = []
            wxy = []
            wx = []
            wx2 = []
            wy = []
            kl = 0
            for i in uy:
                w = (1 / (i ** 2))
                ws.append(w)
            for i in xy:
                wxy.append(i * ws[kl])
                kl += 1
            kl = 0
            for i in xs:
                wx.append(i * ws[kl])
                kl += 1
            kl = 0
            for i in ys:
                wy.append(i * ws[kl])
                kl += 1
            kl = 0
            for i in quadrado(xs):
                wx2.append(i * ws[kl])
                kl += 1

        # Formulas do MMQ

        # # Com apenas uma incerteza em Y. só um valor para incerteza
        if key2 == 0:
            delta = (n * sum(quadrado(xs))) - ((sum(xs)) ** 2.0)
            a = ((n * (sum(xy))) - (sum(xs) * sum(ys))) / delta
            b = (((sum(ys)) * (sum(quadrado(xs)))) - ((sum(xy)) * sum(xs))) / delta
            # calculando incertezass de x e y, mudando sinal caso necessario para não dar numero complexo
            if delta >= 0:
                ua = ((n / delta) ** 0.5) * uy
                ub = (((sum(quadrado(xs))) / delta) ** 0.5) * uy
            if delta < 0:
                ua = ((n / delta) ** 0.5) * uy
                ub = (((sum(quadrado(xs))) / delta) ** 0.5) * uy
        if key2 == 1:
            delta = ((sum(ws)) * (sum(wx2))) - ((sum(wx)) ** 2)
            a = ((sum(ws) * sum(wxy)) - (sum(wx) * sum(wy))) / delta
            b = ((sum(wy) * sum(wx2)) - (sum(wxy) * sum(wx))) / delta
            ub = (sum(wx2) / delta) ** (1 / 2)
            ua = (sum(ws) / delta) ** (1 / 2)

        if key3 == 1:
            kl = 0
            uyt = []
            for i in uy1:
                uyt.append(((i ** 2) + ((a ** 2) * (ux1[kl] ** 2))) ** (1 / 2))
                kl += 1
            if len(uyt) == 1:
                uy = uyt[0]
            else:
                uy = uyt
        key3 = 0

        # calculando função linha caso necessario (se a incerteza de x for maior que y):

    alinha = "*"
    ualinha = "*"
    blinha = "*"
    ublinha = "*"

    if key == 1:
        alinha = a
        ualinha = ua
        a = 1 / a
        ua = (((-1 / a ** 2) ** 2) * (ua ** 2)) ** 0.5
        blinha = b
        ublinha = ub
        b = -b * a
        ub = (((-1 / a) ** 2) * (ub ** 2)) ** 0.5

    # Calculando Erro total, ou residuo:
    kl = 0
    lista_residuo = []
    for i in xs1:
        lista_residuo.append((ys1[kl] - (b + (a * i))) ** 2)
        kl += 1

    dados = {
        "variaveis_X": xs1, "variaveis_y": ys1, "Incertezas_X": ux1, 'somatorio_xs': sum(xs1),
        "lista_xs2": quadrado(xs1),
        "somatorio_xs²": sum(quadrado(xs1)), "lista_xy": xy, "somatorio_xy": sum(xy), 'somatorio_ys': sum(ys1),
        "variavel_n": n, "variavel_delta": delta, "variavel_a": a, "variavel_b": b, "incerteza_a": ua,
        "incerteza_b": ub, "alinha": alinha, "ualinha": ualinha, 'blinha': blinha, 'ublinha': ublinha, 'lista_ws': ws,
        "lista_wx": wx, "lista_wxy": wxy, "lista_wx2": wx2, "lista_wy": wy, "Incertezas_Y": uy1,
        "Incertezas_Juntas_sla": uyt, "lista_de_residuos": lista_residuo, "residuo_total": sum(lista_residuo)
    }
    print(dados)
    dados_importatntes = {"variavel_a": a, "incerteza_a": ua,  "variavel_b": b, "incerteza_b": ub,
                          'somatorio_xs': sum(xs1), "somatorio_xs²": sum(quadrado(xs1)), "somatorio_xy": sum(xy),
                          'somatorio_ys': sum(ys1), "variavel_n": n, "variavel_delta": delta, "alinha": alinha,
                          "ualinha": ualinha, 'blinha': blinha, 'ublinha': ublinha}
    return [dados, dados_importatntes]


def open_result(d):
    # Função que cria uma tabela 2xN com dicionário de entrada
    def tabelayx2(dic, color, font):
        lista = list(dic.keys())
        tabela = tk.Frame(Graficos)
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
        d[1],
        ['#ffac84', '#ffac84', '#ff9684', '#ff9684', 'white'],
        'Arial 12'
    ).grid(column=1, row=1, rowspan=3, padx=5)

    # Criando Frame 2 com mais informações e tabelas

    # Adicionando Graficos ao note
    Note.add(Graficos, text='Graficos')


    Resultado.mainloop()


def checkbox(j):
    a = j.get()
    return a


# janelas

janela = Tk(className='e - Window Color')
janela.configure(background=C1)
janela.geometry('700x400')
janela.resizable(False, False)

# ##########       widgets da janela:
# Checkbox's:

FrameCB = tk.Frame(janela, background=C1)
style = ttk.Style()
style.configure('c1.TCheckbutton', background=C1)

chave1 = tk.IntVar() # Variavel da Checkbox1
Checkbox1 = ttk.Checkbutton(FrameCB, text="Inverter os eixos", variable=chave1, command=lambda: checkbox(chave1),
                            onvalue=1, offvalue=0, style='c1.TCheckbutton')
Checkbox1.pack()

chave3 = tk.IntVar()
Checkbox3 = ttk.Checkbutton(FrameCB, text="Incertezas de mesma magnitude em ambas variaveis", variable=chave3,
                            command=lambda: checkbox(chave3), onvalue=1, offvalue=0, style='c1.TCheckbutton')
Checkbox3.pack()


FrameCB.pack()
FrameCB.place(x=200, y=290)
# Frames
Entrada_Y1 = tk.Frame(janela, background=C1)

Texto_Entrada_Y = ttk.Label(Entrada_Y1, text='Variaveis Y', font=('Agency FB', 15), background=C1)
Texto_Entrada_Y.pack()

Entrada_Y = Text(Entrada_Y1, width=40, height=5, highlightthickness=2, highlightbackground='grey53',
                 highlightcolor='grey26', bd=0)
Entrada_Y.pack()


Entrada_Y1.pack()
Entrada_Y1.place(x=20, y=80)

Incerteza_Y = tk.Frame(janela, background=C1)
Texto_Entrada_IncertezaY = ttk.Label(Incerteza_Y, text='Incerteza de Y', font=('Agency FB', 12), background=C1)
Texto_Entrada_IncertezaY.pack()
Entrada_IncertezaY = Text(Incerteza_Y, height=4, highlightthickness=2, highlightbackground='grey53',
                          highlightcolor='grey26', bd=0, width=25)
Entrada_IncertezaY.insert('1.0', "0")
Entrada_IncertezaY.pack()

Incerteza_Y.pack()
Incerteza_Y.place(x=75, y=205)

Titulo = ttk.Label(text='Calculo de MMQ', font=('Agency FB', 30), foreground=C2, background=C1)
Titulo.pack(pady=25)

Entrada_X1 = tk.Frame(janela, background=C1)
Texto_Entrada_X = ttk.Label(Entrada_X1, text='Entrada X', font=('Agency FB', 15), background=C1)
Texto_Entrada_X.pack()

Entrada_X = Text(Entrada_X1, width=40, height=5, highlightthickness=2, highlightbackground='grey53',
                 highlightcolor='grey26', bd=0)

Entrada_X.pack()

Entrada_X1.pack()
Entrada_X1.place(x=355, y=80)

Incerteza_X = tk.Frame(janela, background=C1)
Texto_Entrada_IncertezaX = ttk.Label(Incerteza_X, text='Incerteza de X', font=('Agency FB', 12), background=C1)
Texto_Entrada_IncertezaX.pack()
Entrada_IncertezaX = Text(Incerteza_X, height=4, highlightthickness=2, highlightbackground='grey53',
                          highlightcolor='grey26', bd=0, width=25)
Entrada_IncertezaX.insert("1.0", "0")
Entrada_IncertezaX.pack()

Incerteza_X.pack()
Incerteza_X.place(x=425, y=205)


Botao = ttk.Button(janela, text='calcule', command=lambda: open_result((mmq(Entrada_Y.get('1.0', 'end'),
        Entrada_X.get('1.0', 'end'), Entrada_IncertezaY.get('1.0', 'end'), Entrada_IncertezaX.get('1.0', 'end'),
        (checkbox(chave1)), (checkbox(chave3))))))


Botao.pack()
Botao.place(y=350, x=320)


janela.mainloop()
