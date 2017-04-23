from turtle import Turtle   #чертежник из черепахи


def init_drawman():
    global t, x_cur, y_cur
    t = Turtle()
    t.penup()
    x_cur = 0
    y_cur = 0
    t.goto(x_cur, y_cur)


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
    global x_cur, y_cur
    x_cur += dx
    y_cur += dy
    t.goto(x_cur ,y_cur )


def to_point(x,y):
    global x_cur, y_cur
    x_cur = x
    y_cur = y
    t.goto(x,y)


init_drawman()
if __name__== '__main__':
    import time
    test_drawman()
    time.sleep(10)
