import tkinter

def button1_command():
    print('Button 1 default command.')

def print_hello(event):
    #print(event.char)
    #print(event.keycode)
    print(event.num)
    print(event.x, event.y)
    #print(event.x_root, event.y_root)
    me = event.widget
    if me==button1:
        print('Hello')
    elif me==button2:
        print('You pressed button2!')
    else:
        raise ValueError()


def init_main_window():
    global root, button1, button2, label, text, scale

    root = tkinter.Tk()

    button1 = tkinter.Button(root, text="Button 1", command=button1_command)  #создаем кнопку с названием
    button1.bind("<Button>",print_hello)

    button2 = tkinter.Button(root, text = "Button 2")  #создаем кнопку с названием
    button2.bind("<Button>",print_hello)  #создаем события работы

    variable = tkinter.IntVar(0)
    label = tkinter.Label(root,textvariable=variable)
    scale = tkinter.Scale(root, orient=tkinter.horizontal,length=300,
                          from_ =0, to=100, tickinterval=10, resolution=5,variable=variable)
    text = tkinter.Entry(root, textvariable=variable)

    for obj in button1, button2, label, scale, text:
        obj.pack()


if __name__ == "_main_":
    init_main_window()

    root.mainloop()
