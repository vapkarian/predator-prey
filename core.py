import random

M = 30
N = 20
VICTIM_RECYCLE = 3
PREDATOR_HUNGER_CYCLES = 25
PREDATOR_REPRODUCTION_CYCLES = 3

signum = lambda x: (x > 0) - (x < 0)


class Victim(object):
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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hunger = 0
        self.bellyful = 0
        self._target = None

    def __unicode__(self):
        return 'Predator: (%d, %d)' % self.position

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, value):
        self.x, self.y = value

    @property
    def behavior(self):
        if self.hunger > (PREDATOR_HUNGER_CYCLES / 2):
            return 'hunting'
        return 'walking'


class World(object):
    def __init__(self):
        self.victims = []
        self.predators = []
        x = random.randint(0, M - 1)
        y = random.randint(0, N - 1)
        self.create_predator(x, y)
        self.time = 0
        self.statistics = []

    def create_predator(self, x, y):
        self.predators.append(Predator(x, y))

    def move_predator(self, predator):
        for iteration in xrange(100):
            x = random.randint(predator.x - 1, predator.x + 1)
            y = random.randint(predator.y - 1, predator.y + 1)
            if not iteration and predator.behavior == 'hunting':
                nearest = None
                nearest_distance = (M ** 2 + N ** 2) ** 0.5
                for victim in self.victims:
                    distance = ((predator.x - victim.x) ** 2 +
                                (predator.y - victim.y) ** 2) ** 0.5
                    if distance < nearest_distance:
                        nearest_distance = distance
                        nearest = victim
                if nearest:
                    x = predator.x + signum(nearest.x - predator.x)
                    y = predator.y + signum(nearest.y - predator.y)
            if not 0 <= x < M or not 0 <= y < N:
                continue
            for another_predator in self.predators:
                if another_predator.position == (x, y):
                    break
            else:
                predator.position = x, y
                for victim in self.victims:
                    if victim.position == (x, y):
                        self.kill_victim(victim)
                        return True
                return False
        raise

    def kill_predator(self, predator):
        self.predators.remove(predator)

    def create_victim(self):
        while True:
            x = random.randint(0, M - 1)
            y = random.randint(0, N - 1)
            is_correct = True
            for victim in self.victims:
                if victim.position == (x, y):
                    is_correct = False
                    break
            if not is_correct:
                continue
            for predator in self.predators:
                if predator.position == (x, y):
                    is_correct = False
                    break
            if not is_correct:
                continue
            self.victims.append(Victim(x, y))
            break

    def move_victim(self):
        raise NotImplementedError('Victim cannot move')

    def kill_victim(self, victim):
        self.victims.remove(victim)

    def cycle(self):
        self.time += 1
        if not self.time % VICTIM_RECYCLE:
            self.create_victim()

        for predator in self.predators[:]:
            old_x, old_y = predator.position
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
