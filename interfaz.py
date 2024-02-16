import tkinter
import time
import mapas_barcos
from random import randint, choice
from functools import partial
from tkinter import messagebox

barcos = [5, 4, 3, 2, 2, 1, 1]
pb = 7
player = 0
bot = 0
d_i = []
d_l = []
u_d = []
posibles_barcos = []
posibles_barco = 0
b = False
e = False
ori = None
posibles = []
p_ud = None
play = False

# main window of the game

window = tkinter.Tk()
window.geometry("1165x565+10+10")
window.title("Hundir La Flota")

def start():
    global bot, player, play
    bot = mapas_barcos.MapaBot()
    bot.colocar_flota_aleatoria()
    player = mapas_barcos.Mapa('tu')
    play = True

def reset():
    global bot, player, barcos, pb, d_i, u_d, d_l, posibles_barcos, posibles_barco, b, e, ori, posibles, p_ud
    # REINICIO DEL CANVAS
    canvas.delete('all')
    canvas.create_line(2.5,5,1105,2.5,fill = "black",
                       width = 5)

    canvas.create_line(5,5,5,510,fill = "black",
                           width = 5)

    canvas.create_line(1058,5,1058,510,fill = "black",
                           width = 5)

    canvas.create_line(5,508,1105,508,fill = "black",
                           width = 5)

    canvas.create_line(530,0,530,510,fill = "black",
                           width = 50)

    for i in range(5,1150,50):
        canvas.create_line(i,5,i,610,fill = "black",
                           width = 2)

    for x in range(5,600,50):
        canvas.create_line(5,x,1160,x,fill = "black",
                           width = 2)
    # REINICIO DE TODAS LAS VARIABLES
    barcos = [5, 4, 3, 2, 2, 1, 1]
    pb = 7
    player = 0
    bot = 0
    d_i = []
    d_l = []
    u_d = []
    posibles_barcos = []
    posibles_barco = 0
    b = False
    e = False
    ori = None
    posibles = []
    p_ud = None
    start()

def end():
    if messagebox.askokcancel("Cerrar ventana", "¿Seguro que quieres cerrar la ventana?"):
        window.destroy()
    

def game(event):
    global player, x, y, barcos, canvas, bot, pb
    if play:
        x = event.x // 50
        y = event.y // 50
        if pb > 0 and x < 10:
            window.bind("<Right>", put_barco)
            window.bind("<Left>", put_barco)
            window.bind("<Up>", put_barco)
            window.bind("<Down>", put_barco)
            pb -= 1
        elif pb == 0:
            if x >= 11 and x < 21:
                int_disparo()
                bot_disparo()
            if len(player.barcos) < 1:
                messagebox.showwarning("Advertencia", "Perdiste!")
                if not messagebox.askokcancel("Cerrar ventana", "¿Quieres volver a jugar?"):
                    window.destroy()
                else:
                    reset()
            elif len(bot.barcos) < 1:
                messagebox.showwarning("Advertencia", "Ganaste!")
                if not messagebox.askokcancel("Cerrar ventana", "¿Quieres volver a jugar?"):
                    window.destroy()
                else:
                    reset()



def put_barco(event):
    global player, x, y, barcos, canvas, bot
    if event.keysym == 'Right':
        barco = mapas_barcos.Barco(get_key_by_value(player.tipos_barco, barcos[0]), barcos[0], [y, x], False, 'd')
    elif event.keysym == 'Left':
        barco = mapas_barcos.Barco(get_key_by_value(player.tipos_barco, barcos[0]), barcos[0], [y, x], False, 'i')
    elif event.keysym == 'Up':
        barco = mapas_barcos.Barco(get_key_by_value(player.tipos_barco, barcos[0]), barcos[0], [y, x], True, 'ar')
    elif event.keysym == 'Down':
        barco = mapas_barcos.Barco(get_key_by_value(player.tipos_barco, barcos[0]), barcos[0], [y, x], True, 'ab')
    barco.crear_barco()
    barco.guadar_alrededor()
    if player.validar_barco(barco):
        player.barcos.append(barco)
        barcos.remove(barcos[0])
        player.colocar_barcos()
        for barco in player.barcos:
            for posicion in barco.posiciones:
                canvas.create_rectangle(5+(50*posicion[1]),
                                        5+(50*posicion[0]), 
                                        5+(50*(posicion[1]+1)), 
                                        5+(50*(posicion[0]+1)), 
                                        fill='grey')
    else:
        messagebox.showwarning("Advertencia", "No puedes  colocar más de un barco en una misma casilla.")


def get_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None

def int_disparo():
    global d_i
    if [x, y] not in d_i:
        d, e = player.disparo(bot, x-11, y)
        if d:
            canvas.create_rectangle(5+(50*x), 
                                    5+(50*y), 
                                    5+(50*(x+1)),
                                    5+(50*(y+1)), 
                                    fill='red')
            if e == 2:
                messagebox.showwarning("Advertencia", "Hundido!")

        else:
            canvas.create_text(30+(50*x),
                               30+(50*y),
                               text='X',
                               fill="black",
                               font='tkDefaeultFont 42')
        d_i.append([x, y])


def bot_disparo():
    global b, e, ori, u_d, posibles
    y_b, x_b, ori = bot_disparo_logica(b, e, ori)
    b, e = bot.disparo(player, y_b, x_b)
    if b:
        canvas.create_rectangle(5+(50*x_b), 
                                5+(50*y_b), 
                                5+(50*(x_b+1)), 
                                5+(50*(y_b+1)), 
                                fill='red')
        if e == 2:
                messagebox.showwarning("Advertencia", "Hundido!")
                u_d = []
                posibles = []
        elif e == 1:
            messagebox.showwarning("Advertencia", "Tocado!")
            u_d.append([y_b, x_b])
    else:
        canvas.create_text(30+(50*x_b),
                           30+(50*y_b),
                           text='X',
                           fill="black",
                           font='tkDefaeultFont 42')
        try:
            posibles.remove([y_b, x_b])
        except:
            pass

def bot_disparo_logica(b, e, ori):
    global u_d, posibles_barcos, posibles_barco, posibles, bot, d_l, p_ud
    a = 0
    while True:
        if len(u_d) == 0:
            y_b = randint(0,9)
            x_b = randint(0,9)
        elif len(u_d) == 1:
            if len(posibles) == 0:
                p_ud = u_d[0]
                posibles = [[u_d[0][0]+1, u_d[0][1]], 
                            [u_d[0][0]-1, u_d[0][1]],
                            [u_d[0][0], u_d[0][1]+1],
                            [u_d[0][0], u_d[0][1]-1]]
                for pos in posibles:
                    if pos[0] < 0 or pos[0] > 9 or pos[1] < 0 or pos[1] > 9 or pos in bot.disparos:
                        posibles.remove(pos)
            d = choice(posibles)
            if d[0] == p_ud[0]+1:
                ori = 'd'
            elif d[0] == p_ud[0]-1:
                ori = 'u'
            elif d[1] == p_ud[1]+1:
                ori = 'r'
            elif d[1] == p_ud[1]-1:
                ori = 'l'
            y_b = d[0]
            x_b = d[1]
        else:
            y_b = u_d[-1][0]
            x_b = u_d[-1][1]
            if b  and e == 1:
                if ori == 'd':
                    y_b += 1
                elif ori == 'u':
                    y_b -= 1
                elif ori == 'r':
                    x_b += 1
                elif ori == 'l':
                    x_b -= 1
        if x_b > 9:
            x_b = p_ud[1] -1
            ori = 'l'
        elif x_b < 0:
            x_b = p_ud[1] +1
            ori = 'r'
        elif y_b > 9:
            y_b = p_ud[0] -1
        elif  y_b < 0:
            y_b = p_ud[0] +1
            ori = 'd'

        if [y_b, x_b] not in bot.disparos:
            break
        elif  len(u_d) >= 2:
            if ori == 'r':
                x_b = p_ud[1] -1
                ori = 'l'
            elif ori == 'l':
                x_b = p_ud[1] +1
                ori = 'r'
            elif ori == 'u':
                y_b = p_ud[0] +1
                ori = 'd'
            elif  ori == 'd':
                y_b = p_ud[0] -1
                ori = 'u'
            break
    return y_b, x_b, ori
    
                


canvas = tkinter.Canvas(window,
                        height = 510,
                        width = 1060,
                        background = "blue")
canvas.place(x = 100, y = 50)

canvas.create_line(2.5,5,1105,2.5,fill = "black",
                       width = 5)

canvas.create_line(5,5,5,510,fill = "black",
                       width = 5)

canvas.create_line(1058,5,1058,510,fill = "black",
                       width = 5)

canvas.create_line(5,508,1105,508,fill = "black",
                       width = 5)

canvas.create_line(530,0,530,510,fill = "black",
                       width = 50)

for i in range(5,1150,50):
    canvas.create_line(i,5,i,610,fill = "black",
                       width = 2)

for x in range(5,600,50):
    canvas.create_line(5,x,1160,x,fill = "black",
                       width = 2)

button_01 = tkinter.Button(window, text = "START",
                           command = start)

button_01.place(x = 15, y = 55, height = 30, width = 65 )

button_02 = tkinter.Button(window, text = "RESET",
                           command = reset)
button_02.place(x = 15, y = 105, height = 30, width = 65 )

button_03 = tkinter. Button(window, text = "END",
                             command = end)

button_03.place(x = 15, y = 155, height = 30, width = 65)

canvas_n = tkinter.Canvas(window,
                        height = 50,
                        width = 1060,
                        background = None)
canvas_n.place(x = 100, y = 0)

canvas_n.create_text((250, 25),
                    text='TÚ',
                    fill="black",
                    font='tkDefaeultFont 42')

canvas_n.create_text((800, 25),
                    text='BOT',
                    fill="black",
                    font='tkDefaeultFont 42')

canvas.bind("<Button-1>", game)

window.mainloop()