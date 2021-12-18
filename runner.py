from time import time
from tqdm import tqdm
from genetic import Genetic
from matplotlib import pyplot
import numpy as np
repeat = 1  # as my teacher says, a genetic algorithm should be executed for like 30 times
# Algorithm Parameters
population = 2000
max_iter = 800
min_iter = 400
pc = 0.80
lower_pc = 0.001
pm = 0.5
lower_pm = 0.009
max_fittness = 64


a = time()
genetics = []
with tqdm(total=repeat*min_iter if min_iter>50 else repeat*max_iter) as pbar:
    for i in range(repeat):
        x = Genetic(
            population=population, max_iter=max_iter, min_iter=min_iter,
            pc=pc, lower_pc=lower_pc, pm=pm,
            lower_pm=lower_pm, max_fittness=max_fittness
        )
        while not x.termination_condition():
            x.next_generation()
            pbar.update(1)
        genetics.append(x)
b = time()


# plot:
# find best
best_arr = genetics[0].population[0]
best_fittness = 0
best_genetic = genetics[0]
for genetic in genetics:
    if genetic.ans.fittness() > best_fittness:
        best_genetic = genetic
        best_fittness = genetic.ans.fittness()
        best_arr = genetic.ans.arr
table = [
    best_arr[0:8],
    best_arr[8:16],
    best_arr[16:24],
    best_arr[24:32],
    best_arr[32:40],
    best_arr[40:48],
    best_arr[48:56],
    best_arr[56:64],
]
table = [[1 - element for element in arr] for arr in table]
fig, ((ax1, ax3), (ax2, ax4)) = pyplot.subplots(2, 2)
fig.suptitle(f"Time: {round((b-a), 2)}s, "
             f"Population: {best_genetic.count_population}, "
             f"Generation: {best_genetic.generation}")
ax4.remove()
ax1.imshow(table, cmap="gray", vmin=0, vmax=1, interpolation="none", aspect="equal")
ax1.set_title(f"Best Found: (fittness: {best_fittness}/64)")

# Major ticks
ax1.set_xticks(np.arange(0, 8, 1))
ax1.set_yticks(np.arange(0, 8, 1))


# Labels for major ticks
ax1.set_xticklabels(np.arange(1, 9, 1))
ax1.set_yticklabels(np.arange(1, 9, 1))

# Minor ticks
ax1.set_xticks(np.arange(-.5, 8, 1), minor=True)
ax1.set_yticks(np.arange(-.5, 8, 1), minor=True)


# Gridlines based on minor ticks
ax1.grid(which='minor', color='black', linestyle='-', linewidth=1)
# pyplot.plot()

ax2.plot(range(best_genetic.generation), best_genetic.avg_fittness)
ax2.set_title("Population Average Fittness By Generation")
ax2.set_xlabel("Generation")
ax2.set_ylabel("Avg")


ax3.plot(range(best_genetic.generation), best_genetic.best_fittness)
ax3.set_title("Best Chromosome Fittness By Generation")
ax3.set_xlabel("Generation")
ax3.set_ylabel("Best")

