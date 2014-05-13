import random

M = 50
N = 50
VICTIM_RECYCLE = 1
PREDATOR_HUNGER_CYCLES = 20
PREDATOR_REPRODUCTION_CYCLES = 3
distance = lambda predator, point: max(abs(predator.x - point[0]), abs(predator.y - point[1]))
signum = lambda x: (x > 0) - (x < 0)


class Victim(object):
    """
    Class of cell-victim. Each object has only position.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, value):
        self.x, self.y = value


class Predator(object):
    """
    Class of cell-predator. Each object has position, behaviour of moving, hunger parameter (cycles without eating),
     bellyful parameter (consecutive cycles with eating).
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hunger = 0
        self.bellyful = 0
        self.behavior = None  # hunting | keeping | walking
        self.target = None

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, value):
        self.x, self.y = value


class World(object):
    """
    Main class of whole world with predators and victims. Each object stores population of predators and victims,
     moves predators, controls hunger of predators, produces new victims and predators, kills eaten victims and
     hungry predators.
    """

    def __init__(self):
        self.victims = {}
        self.predators = {}
        x = random.randint(0, M - 1)
        y = random.randint(0, N - 1)
        self.create_predator(x, y)
        self.time = 0
        self.statistics = []

    def create_predator(self, x, y):
        """
        Creates new predator in cell with coordinate (x, y).

        :param x: coordinate x of world
        :type x: int
        :param y: coordinate y of world
        :type y: int
        """
        self.predators[x, y] = Predator(x, y)

    def move_predator(self, predator):
        """
        Selects cells of moving depending on behavior of predator and neighbors.

        :param predator: predator that will be moved
        :type predator: Predator
        :return: True if predator ate victim, otherwise False
        :rtype: bool
        """
        x_axis = range(max(predator.x - 1, 0), min(predator.x + 1, M - 1) + 1)
        y_axis = range(max(predator.y - 1, 0), min(predator.y + 1, N - 1) + 1)
        neighbours = [(x, y) for x in x_axis for y in y_axis if predator.position != (x, y)]
        random.shuffle(neighbours)
        if predator.target:
            try:
                neighbours.remove(predator.target)
            except ValueError:
                pass
            else:
                neighbours.insert(0, predator.target)
        food = False
        point = predator.position
        behavior = predator.behavior
        for point in neighbours[:]:
            if point in self.predators.iterkeys():
                neighbours.remove(point)
                continue
            elif point in self.victims.iterkeys():
                if behavior in ('hunting', 'walking'):
                    self.kill_victim(self.victims[point])
                    food = True
                    break
            else:
                if behavior in ('keeping', 'walking'):
                    break
        else:
            if neighbours:
                point = neighbours[0]
        self.predators[point] = self.predators.pop(predator.position)
        predator.position = point
        return food

    def kill_predator(self, predator):
        """
        Removes predator from predator population.

        :param predator: predator that will be killed
        :type predator: Predator
        """
        del self.predators[predator.position]

    def create_victim(self):
        """
        Creates new victim in random empty cell.
        """
        while True:
            x = random.randint(0, M - 1)
            y = random.randint(0, N - 1)
            is_correct = True
            for victim in self.victims.iterkeys():
                if victim == (x, y):
                    is_correct = False
                    break
            if not is_correct:
                continue
            for predator in self.predators.iterkeys():
                if predator == (x, y):
                    is_correct = False
                    break
            if not is_correct:
                continue
            self.victims[x, y] = Victim(x, y)
            break

    def kill_victim(self, victim):
        """
        Removes victim from prey population.

        :param victim: victim that will be killed
        :type victim: Victim
        """
        del self.victims[victim.position]

    def cycle(self):
        """
        One period of life cycle. During this period each predator will be moved to the new place, some of them
         may eat victims depending on their behavior and neighbours. Hungry predators will be killed.
        At the end of this period current level of prey population and predator population will be saved.
        """
        self.time += 1
        if not self.time % VICTIM_RECYCLE:
            self.create_victim()

        for predator in self.predators.values()[:]:
            old_x, old_y = predator.position
            predator.target = None
            predator.behavior = 'walking'
            if predator.hunger > (PREDATOR_HUNGER_CYCLES / 2):
                predator.behavior = 'hunting'
                targets = sorted(self.victims.keys(), key=lambda point: distance(predator, point))
                if targets:
                    nearest = targets[0]
                    x = predator.x + signum(nearest[0] - predator.x)
                    y = predator.y + signum(nearest[1] - predator.y)
                    predator.target = (x, y)
            else:
                remaining_cycles = PREDATOR_HUNGER_CYCLES - predator.hunger
                for victim in self.victims.iterkeys():
                    if distance(predator, victim) < remaining_cycles:
                        predator.behavior = 'keeping'
                        break

            food = self.move_predator(predator)
            if food:
                predator.hunger = 0
                predator.bellyful += 1
            else:
                predator.hunger += 1
                predator.bellyful = 0
            if predator.hunger > PREDATOR_HUNGER_CYCLES:
                self.kill_predator(predator)
            if predator.bellyful >= PREDATOR_REPRODUCTION_CYCLES:
                self.create_predator(old_x, old_y)
                predator.bellyful = 0
        self.statistics.append((len(self.predators), len(self.victims)))
