from turtle import Turtle   #чертежник из черепахи


def init_drawman():
    global t, x_cur, y_cur, drawman_scale
    t = Turtle()
    t.penup()
    x_cur = 0
    y_cur = 0
    t.goto(x_cur, y_cur)
    drawman_scale = 10



def test_drawman():
    pen_down()
    for i in range(5):
        on_vector(10,20)
        on_vector(0,-20)
    pen_up()
    to_point(0,0)

def pen_down():
    t.pendown()


def pen_up():
    t.penup()


def on_vector(dx,dy):
    to_point(x_cur+dx, y_cur+dy)



def to_point(x,y):
    global x_cur, y_cur
    x_cur = x
    y_cur = y
    t.goto(drawman_scale *x,drawman_scale *y)


init_drawman()
if __name__== '__main__':
    import time
    test_drawman()
    time.sleep(10)
