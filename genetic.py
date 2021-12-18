from typing import List, Tuple, Optional
from random import randint


class Chromosome:
    def __init__(self, arr: List[int]):
        assert hasattr(arr, "__iter__"), f"arr is not iterable: {arr}"
        assert len(arr) == 64, f"arr size should be 64: {arr}"
        assert all(map(lambda e: True if e == 0 or e == 1 else False, arr)), f"arr contains non-bit char {arr}"
        self.arr = arr
        self.ft = 0  # fittness

    def mutate(self, possibility: float = 0.005):
        if possibility >= randint(0, 1000)/1000:
            random = randint(0, 63)
            if self.arr[random] == 0:  # if it was already 1 then let it go, otherwise make it 1
                start = (random//8)*8
                for i in range(start, start+8):
                    self.arr[i] = 0
                self.arr[random] = 1

    def fittness(self) -> int:
        # we are going to count how many Queens can take each other
        # to make it easy let's create a 8x8 array (I know it's bad.. :o)
        if self.ft != 0:  # cache
            return self.ft
        table = [
            self.arr[0:8],
            self.arr[8:16],
            self.arr[16:24],
            self.arr[24:32],
            self.arr[32:40],
            self.arr[40:48],
            self.arr[48:56],
            self.arr[56:64],
        ]
        # for each 1 in table, let's count how many 1s can be found..
        count = 0
        for i in range(8):
            for j in range(8):
                if table[i][j] == 1:
                    # now let's count..
                    # 1: Horizontal
                    x = i
                    y = j
                    while x < 7:
                        x += 1
                        if table[x][y] == 1:
                            count += 1
                            break
                    # 2: Horizontal - reverse
                    x = i
                    y = j
                    while x > 0:
                        x -= 1
                        if table[x][y] == 1:
                            count += 1
                            break
                    # 3: Vertical
                    x = i
                    y = j
                    while y < 7:
                        y += 1
                        if table[x][y] == 1:
                            count += 1
                            break
                    # 4: Vertical - reverse
                    x = i
                    y = j
                    while y > 0:
                        y -= 1
                        if table[x][y] == 1:
                            count += 1
                            break
                    # 5: Diagonal - element to top-left
                    x = i
                    y = j
                    while x > 0 and y > 0:
                        x -= 1
                        y -= 1
                        if table[x][y] == 1:
                            count += 1
                            break
                    # 6: Diagonal - element to down-left
                    x = i
                    y = j
                    while x > 0 and y < 7:
                        x -= 1
                        y += 1
                        if table[x][y] == 1:
                            count += 1
                            break
                    # 7: Diagonal - element to top-right
                    x = i
                    y = j
                    while x < 7 and y > 0:
                        x += 1
                        y -= 1
                        if table[x][y] == 1:
                            count += 1
                            break
                    # 7: Diagonal - element to down-right
                    x = i
                    y = j
                    while x < 7 and y < 7:
                        x += 1
                        y += 1
                        if table[x][y] == 1:
                            count += 1
                            break
        # alright - now the count is total number of Queens that can take each other
        # maximum of that is something like 8 Queens * 8 Queens = 64, so we can say 64 - count is the fittness
        self.ft = 64 - count
        return 64 - count

    def new(self, other: "Chromosome") -> Tuple["Chromosome", "Chromosome"]:
        """
        Create new Chromosome from self and other
        """
        # using one point cross over to create new chromosome
        # but the point should be at 0, 8, 16, 24, 32, 40, 48, 56, 64
        # due to how we are encoding the data, ask author for more info, or refer to README.md
        point = randint(0, 8) * 8
        first = Chromosome(self.arr[:point] + other.arr[point:])
        second = Chromosome(self.arr[point:] + other.arr[:point])
        return first, second


class Genetic:
    def __init__(self, population: int = 1000,
                 max_iter: int = 800, min_iter: int = 0,
                 pc: float = 0.80, lower_pc: float = 0.0,
                 pm: float = 0.005, lower_pm: float = 0.0,
                 max_fittness: Optional[int] = 64):
        self.generation = 1
        self.max_iter = max_iter
        self.min_iter = min_iter
        self.count_population = population
        self.population: List[Chromosome] = []
        self.avg_fittness = []
        self.best_fittness = []
        self.ans: Optional[Chromosome] = None
        self.pc: float = pc  # possibility of recombine
        self.lower_pc: float = lower_pc  # how much to reduce 'pc' in each generation
        self.pm: float = pm  # possibility of mutate
        self.lower_pm: float = lower_pm  # how much to reduce 'pm' in each generation
        self.max_fittness = max_fittness
        self._evaluate_population()

    def _evaluate_population(self):
        for i in range(self.count_population):
            lst = []
            for _ in range(8):
                lst2 = [0] * 8
                x = randint(0, 7)
                lst2[x] = 1
                lst.extend(lst2)
            self.population.append(Chromosome(lst))
        self.ans = self.population[0]
        self._calc_plotting_values()

    def _calc_plotting_values(self):
        # self.avg_fittness.append(round(sum(map(lambda e: e.fittness(), self.population)) / self.count_population, 2))
        x = 0
        maxi = self.population[0]
        for chromosome in self.population:
            x += chromosome.fittness()
            if chromosome.fittness() > maxi.fittness():
                maxi = chromosome
        self.avg_fittness.append(round(x/self.count_population, 2))
        self.best_fittness.append(maxi.fittness())
        if self.ans.fittness() < maxi.fittness():
            self.ans = maxi

    def termination_condition(self) -> bool:
        if self.min_iter <= self.generation and self.max_fittness <= self.ans.fittness():
            return True
        return self.generation >= self.max_iter

    def parent_selection(self, count: int = 0) -> List[Chromosome]:
        if count == 0:
            count = self.count_population
        # choose 'count' chromosomes by their chance based on fittness
        chances = []
        last = 0
        for chromosome in self.population:
            last += chromosome.fittness()
            chances.append((last, chromosome))
        # now last is end of the range
        parents: List[Chromosome] = []
        for i in range(count):
            random = randint(0, last)
            for key, value in chances:
                if random <= key:
                    break
            # noinspection PyUnboundLocalVariable
            parents.append(value)  # here value is the chosen chromosome
        return parents

    def recombine(self, parents: List[Chromosome]):
        childes: List[Chromosome] = []
        a = 0
        while a + 1 < len(parents):
            random = randint(0, 1000)
            if random >= self.pc * 1000:
                childes.append(Chromosome(parents[a].arr))  # necessary to create new object.
                childes.append(Chromosome(parents[a+1].arr))
            else:
                childes.extend(parents[a].new(parents[a+1]))  # add two new children to childes
            a += 2
        return childes

    def next_generation(self):
        # Parent Selection:
        parents = self.parent_selection()  # default is population size due to how we generate new population
        # Recombine and Create New Chromosomes
        childes = self.recombine(parents)  # default possibility is 0.8
        # Mutation
        for chromosome in childes:
            chromosome.mutate(possibility=self.pm)  # default possibility is 0.005
        # Set New Population
        self.population = childes
        self._calc_plotting_values()
        self.pm -= self.lower_pm
        if self.pm < 0:
            self.pm = 0
        self.pc -= self.lower_pc
        if self.pc < 0:
            self.pc = 0
        self.generation += 1
