#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import turtle
import random
import sys

# ---------- Configurações ------------------------------------
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
COLOR_PALETTE = [
    "#8B4513",  # marrom escuro (tronco)
    "#228B22",  # verde floresta (folhas)
    "#32CD32",  # verde limão
    "#ADFF2F",  # verde claro
    "#6B8E23",  # verde oliva
    "#9ACD32",  # verde amarelo
]
BRANCH_ANGLE = 30
SIZE_REDUCTION = 0.75

# ---------- Funções -------------------------------------------
def draw_branch(t, branch_len, depth):
    if depth == 0:
        return

    t.pencolor(random.choice(COLOR_PALETTE))
    t.forward(branch_len)

    pos = t.position()
    heading = t.heading()

    t.left(BRANCH_ANGLE)
    draw_branch(t, branch_len * SIZE_REDUCTION, depth - 1)

    t.setposition(pos)
    t.setheading(heading)

    t.right(BRANCH_ANGLE)
    draw_branch(t, branch_len * SIZE_REDUCTION, depth - 1)

    t.setposition(pos)
    t.setheading(heading)
    t.backward(branch_len)

def setup_turtle():
    screen = turtle.Screen()
    screen.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
    screen.title("Árvore Fractal - Turtle")
    screen.bgcolor("#F0F8FF")

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.left(90)
    t.penup()
    t.setposition(0, -WINDOW_HEIGHT / 2 + 50)
    t.pendown()
    t.pensize(2)
    return t

def main():
    try:
        depth = int(input("Profundidade (ex.: 9) [padrão 9]: ") or 9)
        base_length = int(input("Comprimento inicial dos ramos [padrão 120]: ") or 120)
    except ValueError:
        print("Valor inválido. Usando valores padrão.")
        depth = 9
        base_length = 120

    t = setup_turtle()
    draw_branch(t, base_length, depth)
    turtle.done()

if __name__ == "__main__":
    main()