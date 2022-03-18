from matplotlib import pyplot as plt
import numpy as np
import time


# Criando uma pessoa que contem o estado dela (saudavel ou gripada) e a quantidade de dias que ela esta gripada
class person():
    def __init__(self, state, days, immunity) -> None:
        self.state = state
        self.days = days
        self.immunity = immunity

days_until_healed = 14
time_to_spread = 3
initial_prob = 0.4
total_days = []
print(total_days)

def draw():
    fig = plt.figure(figsize=(5,4))
    axes_1 = fig.add_axes([0.1,0.1,0.9,0.9])
    axes_1.set_ylabel('Number of infected people in the classroom')
    axes_1.set_xlabel('Days')
    axes_1.plot( total_days, infected, label='Infected',color = 'red')
    
    plt.show()

# Imprimindo o estado de cada pessoa da sala
def printgrid():
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j].state == 'S':
                plt.scatter(i, j, color = 'green', s = 5)
            else: 
                plt.scatter(i, j, color = 'red', s = 5)
    plt.show()
    print()

# Criando a sala
grid = [[person('S', 0, 1) for i in range(500)] for j in range(500)] 


# Populando a sala
for i in range(len(grid)):
    for j in range(len(grid)):
        grid[i][j] = person('S', 0, 1)


# Começando a contaminar a sala
for i in range(5):
    x = np.random.randint(0,len(grid))
    y = np.random.randint(0,len(grid))
    grid[x][y].state = 'G'

print("Dia Zero")
nearby = []

infected = []
healthy = []

for days in range(500):
    n_infected = 0
    n_healthy = 0
    # Correr cada lugar da sala e ver se ta contaminado
    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid[x][y].state == 'G':
                n_infected += 1
                if grid[x][y].days >= time_to_spread:
                    # Pegando o lugar das pessoas que possivelmente possam ser contaminadas
                    nearby = [[x, y - 1], [x, y + 1], [x + 1, y], [x - 1, y]]
                for i in nearby:
                    if i[0] >= len(grid) or i[1] >= len(grid) or i[0] < 0 or i[1] < 0:
                        continue 
                    if grid[i[0]][i[1]].state == 'S':
                        chance_of_infection = np.random.uniform(0,1)
                        # 30% de chance de ser infectado
                        if chance_of_infection <= initial_prob * 1/grid[i[0]][i[1]].immunity:
                            grid[i[0]][i[1]].state = 'G'
            else: 
                n_healthy += 1
    # Checking the days since he got the desease
    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid[x][y].state == 'G':
                # Checking the days since he got the desease
                if grid[x][y].days < days_until_healed:
                    grid[x][y].days+=1
                # Checking if he has healed the desease
                if grid[x][y].days == days_until_healed: 
                    grid[x][y].state = 'S'
                    grid[x][y].days = 0
                    grid[x][y].immunity += 1
    
    total_days.append(days + 1)
    
    infected.append(n_infected)
    
    healthy.append(n_healthy)
    

print(infected)
print(healthy)
draw()
