from drawman_by_turtle.drawman import *

colours = ['red', 'green', 'blue']*5
back_colours = ['pink', 'lightgreen', 'lightblue']*5

init_drawman()

def f(x):
    return x*x

x=-5.0
to_point(x,f(x))
pendown()
while x <= 5:
    pendown()
    begin_fill()
    to_point(x,f(x))
    end_fill()
    penup()
    x +=0.1



