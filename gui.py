import Tkinter
import core

CELL_SIZE = 10
PAUSE_KEY = '<space>'
EMPTY_COLOR = 'white'
PREDATOR_COLOR = 'red'
VICTIM_COLOR = 'green'
TIMER = 100


class Cell(Tkinter.Frame):
    def __init__(self, window, master, x, y):
        Tkinter.Frame.__init__(self, master, width=CELL_SIZE, height=CELL_SIZE,
                               background=EMPTY_COLOR)
        self.config(borderwidth=1, relief=Tkinter.GROOVE)
        self.grid(row=y, column=x)
        self.window = window
        self.x = x
        self.y = y

    def hunt(self, event):
        self.config(background=EMPTY_COLOR)
        for predator in self.window.world.predators[:]:
            if predator.position == (self.x, self.y):
                self.window.world.predators.remove(predator)
                return
        for victim in self.window.world.victims[:]:
            if victim.position == (self.x, self.y):
                self.window.world.victims.remove(victim)
                return


class Window(Tkinter.Tk):

    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.lock = False
        self.bind(PAUSE_KEY, self.lock_wait)
        self.root = Tkinter.Frame(self, width=core.M * CELL_SIZE, height=core.N * CELL_SIZE)
        self.root.pack()
        self.root.pack_propagate(0)
        self.title('Predators and victims')
        self.cells = []
        for x in xrange(core.M):
            col = []
            for y in xrange(core.N):
                cell = Cell(self, self.root, x, y)
                cell.bind('<Button-1>', cell.hunt)
                col.append(cell)
            self.cells.append(col)
        self.world = core.World()
        self.timer_update()

    def lock_wait(self, event):
        self.lock = not self.lock
        if not self.lock:
            self.timer_update()

    def timer_update(self):
        if self.lock:
            return

        for elem in self.world.victims + self.world.predators:
            self.cells[elem.x][elem.y].config(background=EMPTY_COLOR)

        self.world.cycle()

        for victim in self.world.victims:
            self.cells[victim.x][victim.y].config(background=VICTIM_COLOR)

        for predator in self.world.predators:
            self.cells[predator.x][predator.y].config(background=PREDATOR_COLOR)

        if len(self.world.predators):
            self.root.after(TIMER, self.timer_update)
        else:
            self.destroy()


if __name__ == '__main__':
    window_obj = Window()
    window_obj.mainloop()
    try:
        from matplotlib import pyplot
    except ImportError:
        pyplot = None

    if pyplot is not None:
        predators_data = [line[0] for line in window_obj.world.statistics]
        victims_data = [line[1] for line in window_obj.world.statistics]
        period_data = range(len(window_obj.world.statistics))
        pyplot.plot(period_data, predators_data, 'r-', period_data, victims_data, 'g-')
        pyplot.axis([-1, max(period_data) + 1, -1, max(predators_data + victims_data) + 1])
        pyplot.show()
    else:
        for index, line in enumerate(window_obj.world.statistics):
            print '%d: predators - %d, victims - %d' % (index, line[0], line[1])
