import tkinter as tk
from tkinter import ttk


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
        ua = (((-1 / a ** 2) ** 2) * (ua ** 2)) ** 0.5
        ub = (((-1 / a) ** 2) * (ub ** 2)) ** 0.5
        a = 1 / a
        blinha = b
        ublinha = ub
        b = -b * a


    # Calculando Erro total, ou residuo:
    kl = 0
    lista_residuo = []
    for i in xs1:
        lista_residuo.append((ys1[kl] - (b + (a * i))) ** 2)
        kl += 1

    dados = {
        "variaveis_X": xs1, "variaveis_y": ys1, "Incertezas_X": ux1, 'somatorio_xs': sum(xs1),
        "lista_xs2": quadrado(xs1),
        "somatorio_xs2": sum(quadrado(xs1)), "lista_xy": xy, "somatorio_xy": sum(xy), 'somatorio_ys': sum(ys1),
        "variavel_n": n, "variavel_delta": delta, "variavel_a": a, "variavel_b": b, "incerteza_a": ua,
        "incerteza_b": ub, "alinha": alinha, "ualinha": ualinha, 'blinha': blinha, 'ublinha': ublinha, 'lista_ws': ws,
        "lista_wx": wx, "lista_wxy": wxy, "lista_wx2": wx2, "lista_wy": wy, "Incertezas_Y": uy1,
        "Incertezas_Juntas_sla": uyt, "lista_de_residuos": lista_residuo, "residuo_total": sum(lista_residuo)
    }

    return dados


# print(mmq("2 3 5", "1 5 8", "0.2 0.3 0.1", "0.1 0.1 0.3", 0, 1))

print(mmq("0.13877 0.18857 0.23887 0.14861 0.16827 0.21807 0.26837", "0.0783 0.2630 0.4110 0.1480 0.1841 0.5442 0.6091",
          '0.00005 0.00005 0.00005 0.00005 0.00005 0.00005 0.00005', '0.0001 0.0005 0.001 0.0002 0.0003 0.002 0.002', 1, 0))




#print(mmq("1,1 1,9 3,2 4,1 4,8", "1 2 3 4 5", "0.3 0.4 0.3 0.3 0.3", "0", 0, 0))

#print(mmq("1,12 1,89 3,16 4,04 4,86", "1 2 3 4 5", "0,02 0,03 0,04 0,02 0,03", "0,3 0,4 0,3 0,3 0,3", 1, 0))

#print(mmq("1,1 1,9 3,2 4,1 4,8", "1,0 2,0 3,0 4,0 5,0", "0,3", "0,2", 0, 1))

#print(mmq("0,5 2,5 2,0 4,0 3,5 6,0 5,5", "1 2 3 4 5 6 7", "0", "0", 0, 0))
