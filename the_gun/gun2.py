from tkinter import *
from random import choice, randint
from math import*
from tkinter import messagebox

screen_width = 400
screen_height = 400
timer_delay = 20
initial_number = 20
shell_limit = 25# число выстрелов

class Ball:
    """
    Абстрактный класс -- предок для шариков-мишеней и для снарядов.
    Имеет атрибуты x, y, Vx, Vy, R, avatar
    а также метод fly -- абстрактный (т.е. его нельзя реально вызывать)
    """
    def __init__(self, x, y, Vx, Vy, R, avatar):

        self._R = R
        self._x = x
        self._y = y
        self._Vx = Vx
        self._Vy = Vy
        self._avatar = avatar

    def fly(self):
        """
        Абстрактный метод! Нельзя вызывать.
        Требуется реализовывать в классах-потомках.
        """
        raise RuntimeError()

    def delete(self): # удаление объекта
        canvas.delete(self._avatar)

class Target(Ball):
    """
    Мишень, шары разного цвета и диаметра, отражающиеся от стен
    """
    minimal_radius = 15
    maximal_radius = 30
    available_colors = ['green', 'blue', 'red']

    def __init__(self):
        """
        Cоздаёт шарик в случайном месте игрового холста canvas,
        при этом шарик не выходит за границы холста!
        """
        R = randint(Target.minimal_radius, Target.maximal_radius)
        x = randint(0, screen_width-1-2*R)
        y = randint(0, screen_height-1-2*R)
        color = choice(Target.available_colors)
        avatar = canvas.create_oval(x, y, x+2*R, y+2*R,width=1, fill=color,outline=color)
        Vx = 0
        # Проверяем, чтобы у шарика не получилось нулевое смещение
        while Vx ==0:
            Vx = randint(-2, 2)
        Vy = 0
        while Vy ==0:
            Vy = randint(-2, 2)
        super().__init__(x, y, Vx, Vy, R, avatar)

    def fly(self): #Движение мишени
        self._x += self._Vx
        self._y += self._Vy
        # отражается от горизонтальных стенок
        if self._x < 0:
            self._x = 0
            self._Vx = -self._Vx
        elif self._x + 2*self._R >= screen_width:
            self._x = screen_width - 2*self._R
            self._Vx = -self._Vx
        # отражается от вертикальных стенок
        if self._y < 0:
            self._y = 0
            self._Vy = -self._Vy
        elif self._y + 2*self._R >= screen_height:
            self._y = screen_height - 2*self._R
            self._Vy = -self._Vy
        canvas.coords(self._avatar, self._x, self._y,
                      self._x + 2*self._R, self._y + 2*self._R)

    def delete(self): # удаление экземпляра шарика
        canvas.delete(self._avatar)

class Shell(Ball):
    """
    Снаряд, вылетающий из пушки.
    Не отражается от стенок, уничтожается, если вылетел за пределы поля.
    Двигается по гравитационной траектории.
    """
    color = 'black'

    def __init__(self, x, y, Vx, Vy):
        R = 5
        avatar = canvas.create_oval(x, y, x+2*R, y+2*R, width=1, fill=Shell.color,
                                          outline=Shell.color)
        super().__init__(x, y, Vx, Vy, R, avatar)

    def fly(self):
        ax = 0
        ay = 0.02 #угловая скорость
        dt = 3  # квант физического времени
        self._x += self._Vx*dt + ax*dt**2/2
        self._y += self._Vy*dt + ay*dt**2/2
        self._Vx += ax*dt
        self._Vy += ay*dt
        canvas.coords(self._avatar, self._x, self._y,
                      self._x + 2*self._R, self._y + 2*self._R)
class Gun:  #Пушка
    def __init__(self):
        self._x = 0
        self._y = screen_height
        self.lx = 30
        self.ly = -30
        self.avatar = canvas.create_line(self._x, self._y, self._x+self.lx, self._y+self.ly,width=4)

    def shoot(self):
        """  :return возвращает объект снаряда (класса Shell) по щелчку мышки  """
        shell = Shell(self._x - 5 + self.lx, self._y - 5+ self.ly, self.lx/10, self.ly/10)
        return shell

    def move(self,dx,dy):
        """Движение пушки за мышкой"""
        dy = self._y-dy
        r = sqrt(dx**2+dy**2)
        self.lx =int(42*(dx/r))
        self.ly = -int(42*(dy/r))
        canvas.delete(self.avatar)
        self.avatar = canvas.create_line(self._x, self._y, self._x+self.lx, self._y+self.ly,width=4)

def init_game():
    """     Создаём необходимое для игры количество объектов-шариков,
    а также объект - пушку.    """
    global balls, gun, shells_on_fly
    balls = [Target() for i in range(initial_number)]
    gun = Gun()
    shells_on_fly = [] # массив снарядов на поле

def move_gun(event): #движение пушки если указатель мышки в пределах поля
    if 1 < event.x < screen_width and 1 < event.y < screen_height:
        gun.move(event.x, event.y)

def meeting(event):
    """  Проверяем, соприкасаются ли снаряд и мишень если ДА, добавляем очки
    в зависимомти от радиуса снаряда и удаляем мишень
    Если мишень поражена, то функция выдает True, иначе False"""
    global goals_value
    count = False
    for ball in balls:
        if ((ball._x+ball._R)-(event._x+event._R))**2+((ball._y+ball._R)-(event._y+event._R))**2<(ball._R+event._R)**2:
            if ball._R>25:
                goals_value.set(goals_value.get()+1)
            elif ball._R>20:
                goals_value.set(goals_value.get()+2)
            else:
                goals_value.set(goals_value.get()+3)
            balls.remove(ball)
            ball.delete()
            count =True #если произощло столкновение, фиксируем
    return count

def click_event_handler(event):
    """ По клику левой клавиши мышки и при наличии снарядов shell_value.get()>0
    выпускается новый снаряд, если снарядов нет, вызывается функция для завершения игры"""
    global shells_on_fly
    if shell_value.get()>0:
        shell = gun.shoot()
        shells_on_fly.append(shell)
        shell_value.set(shell_value.get()-1)
    else:
        selection()

def timer_event():
    # все периодические рассчёты, которые я хочу, делаю здесь
    for ball in balls: #сдвигаем все снаряды из массива
        ball.fly()
    for shell in shells_on_fly:
        # Проверка вылета снаряда за пределы поля
        if shell._x+shell._Vx+10>screen_width or shell._y+shell._Vy<0 or  shell._x - shell._Vx<0 or shell._y + shell._Vy>screen_height:
            shell.delete()
        elif meeting(shell):# Если попали в мишень
            shells_on_fly.remove(shell)# удаляем снаряд из массива
            shell.delete() # удаляем объект снаряда
        else:
            shell.fly()# двигаем снаряд
    canvas.after(timer_delay, timer_event)# задержка

def close_win():# уничтожаем главное окно со всеми объектами
    root.destroy()

def rules():
    # вывод правил игры
    rule = "На поле движется 20 шариков\n Надо сбить шарики как можно меньшим числом снарядов\n "
    rule +='Чем мешьше шарик, тем больше очков за него дается\n '
    rule +='Движение курсора мышки управляет поворотом пушки\n '
    rule +='Снаряд выпускается по щелчку левой клавиши мышки\n '
    tex = messagebox.showinfo("Правила игры",rule)

def init_menu():# создание меню
    m = Menu(root)
    root.config(menu = m)
    fm = Menu(m)
    m.add_cascade(label="Меню", menu=fm)
    fm.add_command(label="Правила игры", command=rules)
    fm.add_command(label="Выход", command=close_win)

def new_game():# инициализация новой игры
    win.destroy()
    frame.destroy()
    init_frame()

def selection():# диалоговое окно, выводиться если закончились снаряды
    global win, tex , close
    canvas.destroy()# убираем canvas иначе на каждый щелчок мышки будет выводиться Toplevel
    win = Toplevel(root)#дочернее окно
    tex = Label(win, text='Снаряды закончились', width=20,height= 1, font="Verdana 12")
    tex.pack()
    new = Button(win, text="Начать новую игру",command=new_game)#Срабатывает на нажатие и отпуск мышки
    new.pack()
    close = Button(win, text="Выход",command=close_win)#Срабатывает на нажатие и отпуск мышки
    close.pack()

def init_frame():
    global canvas, goals_text, goals_value, shell_value, frame
    frame =Frame(root)
    goals_value = IntVar()
    shell_value = IntVar()
    shell_value.set(shell_limit)
    goals_text = Label(frame, text='Число набранных очков', font='Calibri 14')
    goals_text.grid(row=0, column=0 )
    goals_count = Label(frame, width=5,bg='white', textvariable=goals_value, font='Calibri 14')
    goals_count.grid(row=0, column=1)
    shell_text = Label(frame, text='Осталось снарядов', font='Calibri 14')
    shell_text.grid(row=1, column=0)
    shell_count = Label(frame,width=5, bg='white', textvariable=shell_value, font='Calibri 14')
    shell_count.grid(row=1, column=1)
    canvas = Canvas(frame, width=screen_width, height=screen_height,bg="white")
    canvas.grid(row=2, column=0, columnspan=2)
    frame.pack()
    canvas.bind('<Button-1>', click_event_handler)
    canvas.bind("<Motion>", move_gun)
    init_game()
    timer_event()

def init_main_window():
    global root, canvas
    root = Tk()
    root.title("Пушка")
    root.minsize(450, 500)
    root.maxsize(450, 500)
    init_frame()
    init_menu()

if __name__ == "__main__":
    init_main_window()
    root.mainloop()
