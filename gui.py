import Tkinter
import core

CELL_SIZE = 10
PAUSE_KEY = '<space>'
EMPTY_COLOR = 'black'
PREDATOR_COLOR = 'red'
VICTIM_COLOR = 'green'
TIMER = 100


class Window(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.world = core.World()
        self.title('Predator-prey simulation')
        self.resizable(width=Tkinter.FALSE, height=Tkinter.FALSE)
        self.bind(PAUSE_KEY, self.pause)
        self.canvas = Tkinter.Canvas(self, width=core.M * CELL_SIZE, height=core.N * CELL_SIZE, background=EMPTY_COLOR)
        self.canvas.bind('<Button-1>', self.click)
        self.canvas.pack()
        self.lock = False
        self.timer_update()

    def pause(self, event):
        self.lock = not self.lock
        if not self.lock:
            self.timer_update()

    def click(self, event):
        point = (event.x / CELL_SIZE, event.y / CELL_SIZE)

        for predator in self.world.predators.itervalues():
            if predator.position == point:
                self.world.kill_predator(predator)
                self.create_cell(point, EMPTY_COLOR)
                return
        for victim in self.world.victims.itervalues():
            if victim.position == point:
                self.world.kill_victim(victim)
                self.create_cell(point, EMPTY_COLOR)
                return

    def create_cell(self, point, color):
        x, y = point
        bbox = (x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE)
        self.canvas.create_rectangle(*bbox, tags=point, fill=color, width=0, activewidth=1)

    def timer_update(self):
        if self.lock:
            return
        self.canvas.delete(Tkinter.ALL)
        self.world.cycle()
        for victim in self.world.victims.iterkeys():
            self.create_cell(victim, color=VICTIM_COLOR)
        for predator in self.world.predators.iterkeys():
            self.create_cell(predator, color=PREDATOR_COLOR)
        if len(self.world.predators):
            self.after(TIMER, self.timer_update)
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
