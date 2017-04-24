from drawman import *
from time import sleep

a =[(0,0),(100,0),(100,100),(0,100)]
pen_down()
for x,y in a:
    to_point(x,y)
to_point(a[0][0],a[0][1])
pen_up()


sleep(20)
