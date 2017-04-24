from drawman import *

colours = ['red', 'green', 'blue']*5
back_colours = ['pink', 'lightgreen', 'lightblue']*5

init_drawman()
pendown()
begin_fill()
on_vector(100, 0)
on_vector(0, 100)
on_vector(-100, 0)
on_vector(0, -100)
end_fill()
penup()

