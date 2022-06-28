from matplotlib import pyplot as plt
import numpy as np
import time

tempo = time.time()

# Criando uma pessoa que contem o estado dela (saudavel ou gripada) e a quantidade de dias que ela esta gripada
class person():
    def __init__(self, state, days, immunity, location_x, location_y,id) -> None:
        self.id = id
        self.state = state
        self.days = days
        self.immunity = immunity
        self.location_x = location_x
        self.location_y = location_y

def printgrid():
    for i in healthy_people:
        plt.scatter(i.location_x, i.location_y, color = 'green', s = 5)
    for x in infected_people:
        plt.scatter(x.location_x, x.location_y, color = 'red', s = 5)
    plt.show()
    print()

def draw():
    fig = plt.figure(figsize=(10,8))
    axes_1 = fig.add_axes([0.1,0.1,0.9,0.9])
    axes_1.set_ylabel('Number of infected people in the classroom')
    axes_1.set_xlabel('Days')
    axes_1.plot(total_days, infected, label='Infected',color = 'red')
    axes_1.plot(total_days, recovered, label='Recovered',color = 'blue')
    axes_1.plot(total_days, healthy, label='Healthy',color = 'Green')
    leg = axes_1.legend()
    plt.show()

global n_infected, n_healthy, recovered ,infected ,healthy, total_days, infected_people, healthy_people,days

# Changeable Parameters
total_people = 7000
radius = 70
days_until_healed = 6
time_to_spread = 3
initial_prob = 0.1

# Used to draw the graph
n_infected = 0
n_healthy = 0
n_recovered = 0
recovered = []
infected = []
healthy = []

# Necessary variables
total_days = []
infected_people = []
healthy_people = []
days = 0

# Criando a sala
def create_room():
    for x in range(total_people):
                                      #size of the square
        random_x = np.random.uniform(0,total_people*0.15)
        random_y = np.random.uniform(0,total_people*0.15)
        if x % int(7000*0.1) == 0:
            #creating infected people
            infected_people.append(person('G', 0, 1, random_x ,random_y,x))
        else:
            healthy_people.append(person('S', 0, 1, random_x ,random_y,x))

    # sorting healthy and infected people based on their X position
    sorted(healthy_people, key=lambda x: x.location_x)
    sorted(infected_people, key=lambda x: x.location_x)

def healing():
    global n_infected, n_healthy, n_recovered, recovered ,infected ,healthy, total_days, infected_people, healthy_people, days
    # Checking the days since he got the desease
    for i in infected_people:
        # Checking the days since he got the desease
        if i.days < days_until_healed:
            i.days+=1
        # Checking if he has healed the desease
        if i.days == days_until_healed: 
            i.state = 'S'
            i.days = 0
            i.immunity += 1
            infected_people.remove(i)
            healthy_people.append(i)
            # if he has been infected 5 times he now is categorized as immune and cant be infected again
            if i.immunity == 5:
                i.state = 'R'
                n_recovered += 1
                healthy_people.remove(i)
    
    # appending for graph creation purposes
    recovered.append(n_recovered)
    days += 1              
    total_days.append(days)
    infected.append(len(infected_people))
    healthy.append(len(healthy_people))
    # sorting 
    sorted(healthy_people, key=lambda x: x.location_x)
    sorted(infected_people, key=lambda x: x.location_x)

def infecting():
    while (len(infected_people) != 0):
    # Go through each of the infected people and try to infected people nearby
        for x in infected_people:
            infection_circle = x.location_x - radius
            if x.days >= time_to_spread:
                # Pegando o lugar das pessoas que possivelmente possam ser contaminadas
                for i in healthy_people:
                    if i.location_x < infection_circle:
                        continue
                    elif ((i.location_x - x.location_x)**2 + (i.location_y - x.location_y)**2 <= radius**2):
                        chance_of_infection = np.random.uniform(0,1)
                        # 30% de chance de ser infectado
                        if chance_of_infection <= initial_prob * 1/i.immunity:
                            i.state = 'G'
                            healthy_people.remove(i)
                            infected_people.append(i)
                    else:
                        if i.location_x > x.location_x + radius:
                            break
        healing()

def main():
    create_room()
    infecting()
    draw()
    print(days)
    print(time.time() - tempo)

main()

