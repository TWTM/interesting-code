import numpy as np
import time

# Criando uma pessoa que contem o estado dela (saudavel ou gripada) e a quantidade de dias que ela esta gripada
class person():
    def __init__(self, state, days) -> None:
        self.state = state
        self.days = days

days_until_healed = 5
time_to_spread = 2
initial_prob = 0.3


# Imprimindo o estado de cada pessoa da sala
def printgrid():
    for i in range(len(grid)):
        for j in range(len(grid)):
            print(grid[i][j].state,' ', end='')
        print()
    print()

# Criando a sala
grid = [[person('S', 0) for i in range(10)] for j in range(10)] 

# Populando a sala
for i in range(len(grid)):
    for j in range(len(grid)):
        grid[i][j] = person('S', 0)



# Começando a contaminar a sala
for i in range(5):
    x = np.random.randint(0,len(grid))
    y = np.random.randint(0,len(grid))
    grid[x][y].state = 'G'

print("Dia Zero")
printgrid()

nearby = []

for days in range(50):
    print(days + 1, "dia\n")
    # Correr cada lugar da sala e ver se ta contaminado
    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid[x][y].state == 'G' and grid[x][y].days >= time_to_spread:
                # Pegando o lugar das pessoas que possivelmente possam ser contaminadas
                nearby = [[x, y - 1], [x, y + 1], [x + 1, y], [x - 1, y]]
            for i in nearby:
                if i[0] >= len(grid) or i[1] >= len(grid) or i[0] < 0 or i[1] < 0:
                    continue 
                if grid[i[0]][i[1]].state == 'S':
                    chance_of_infection = np.random.uniform(0,1)
                    # 30% de chance de ser infectado
                    if chance_of_infection <= initial_prob:
                        grid[i[0]][i[1]].state = 'G'
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

    time.sleep(1)
    printgrid()
    print("--------------")
    print()
    print()
    