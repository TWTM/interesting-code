from matplotlib import pyplot as plt
import numpy as np
import time



# Criando uma pessoa que contem o estado dela (saudavel ou gripada) e a quantidade de dias que ela esta gripada
class person():
    def __init__(self, state, days, immunity, location_x, location_y,id) -> None:
        self.id = id
        self.state = state
        self.days = days
        self.immunity = immunity
        self.location_x = location_x
        self.location_y = location_y

"""def printgrid():
    infected_y = []
    infected_x = []
    healthy_y = []
    healthy_x = []
    recovered_x = []
    recovered_y = []
    for i in infected_people:
        infected_x.append(i.location_x)
        infected_y.append(i.location_y)
    for h in healthy_people:
        healthy_x.append(h.location_x)
        healthy_y.append(h.location_y)
    for r in recovered_people:
        recovered_x.append(r.location_x)
        recovered_y.append(r.location_y)
    
    for i in range(3):
        if i == 0:
            plt.scatter(healthy_x, healthy_y, color = 'green', s = 3)
            plt.pause(0.0001)
        elif i == 1:
            plt.scatter(infected_x, infected_y, color = 'red', s = 3)
            plt.pause(0.0001)
        else:
            plt.scatter(recovered_x, recovered_y, color = 'blue', s = 3)
            plt.pause(0.0001)
    plt.title(label= days)
    plt.xlabel(len(infected_people))"""


def draw():
    fig = plt.figure(figsize=(10,8))
    axes_1 = fig.add_axes([0.1,0.1,0.9,0.9])
    axes_1.set_ylabel('Number of infected people in the classroom')
    axes_1.set_xlabel('Days')
    axes_1.plot(total_days, infected, label='Infected',color = 'red')
    axes_1.plot(total_days, recovered, label='Recovered',color = 'blue')
    axes_1.plot(total_days, healthy, label='Healthy',color = 'green')
    leg = axes_1.legend()
    

# Criando a sala
def create_room(infected_proportion, total_people):
    global infected_people, healthy_people
    for x in range(total_people):
        random_x = np.random.uniform(0,total_people*0.1)
        random_y = np.random.uniform(0,total_people*0.1)
        if x % (total_people * infected_proportion) == 0:
            infected_people.append(person('G', 0, 1, random_x ,random_y,x))
            continue    
        healthy_people.append(person('S', 0, 1, random_x ,random_y,x))

    healthy_people = sorted(healthy_people, key=lambda x: x.location_x)
    infected_people = sorted(infected_people, key=lambda x: x.location_x)

def healing(days_until_healed):
    global days, infected_people, healthy_people, recovered_people
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
            # if he has been infected 4 times he now is categorized as immune and cant be infected again
            if i.immunity == 4:
                i.state = 'R'
                healthy_people.remove(i)
                recovered_people.append(i)

    recovered.append(len(recovered_people))
    
    days += 1              
    total_days.append(days)
    infected.append(len(infected_people))
    healthy.append(len(healthy_people))

    # if days % 3 == 0:
            # printgrid()

    healthy_people = sorted(healthy_people, key=lambda x: x.location_x)
    infected_people = sorted(infected_people, key=lambda x: x.location_x)



# Available distributions

def gamma_distribution(mean, std_dev):
    # Calculate the shape and scale parameters of the gamma distribution
    shape = mean**2 / std_dev**2
    scale = std_dev**2 / mean

    # Generate a random sample from the gamma distribution
    sample = np.random.gamma(shape, scale)

    return sample

def weibull_distribution(mean, std_dev):
    # Calculate the shape and scale parameters of the Weibull distribution
    shape = round(mean / std_dev**2)
    scale = round(std_dev**2)

    # Generate a random sample from the Weibull distribution
    sample = np.random.weibull(shape, scale)

    return sample

def lognormal_distribution(mean, std_dev):
    # Calculate the mean and standard deviation of the lognormal distribution
    mu = np.log(mean) - 0.5 * std_dev**2
    sigma = np.sqrt(np.log(std_dev**2 + 1))

    # Generate a random sample from the lognormal distribution
    sample = np.random.lognormal(mu, sigma)

    return sample

def distribution(distribution_type, mean, std_dev):
    if distribution_type == "ln":
        return lognormal_distribution(mean, std_dev)
    elif distribution_type == "wb":
        return weibull_distribution(mean, std_dev)
    elif distribution_type == "gm":
        return gamma_distribution(mean, std_dev)
    else:
        raise ValueError("Invalid distribution type")
    


def infecting(radius, time_to_spread, initial_prob, days_until_healed, distributiont, mean, stdd):
    while (len(infected_people) != 0):
    # Correr cada lugar da sala e ver se ta contaminado
        for x in infected_people:
            infection_line = x.location_x - radius
            if x.days >= time_to_spread:
                # Pegando o lugar das pessoas que possivelmente possam ser contaminadas
                for i in healthy_people:
                    if i.location_x < infection_line:
                        continue
                    elif ((i.location_x - x.location_x)**2 + (i.location_y - x.location_y)**2 <= radius**2):
                        # 30% de chance de ser infectado
                        if distribution(distributiont, mean, stdd) <= initial_prob * 1/i.immunity:
                            i.state = 'G'
                            healthy_people.remove(i)
                            infected_people.append(i)
                    else:
                        if i.location_x > x.location_x + radius:
                            break
        healing(days_until_healed)
        

def run_simulation(total_people, radius, days_until_healed, time_to_spread, initial_prob, infected_proportion, distributiont, mean, stdd):
    global mean_days
    create_room(infected_proportion, total_people)
    infecting(radius, time_to_spread, initial_prob, days_until_healed, distributiont, mean, stdd)
    mean_days += days

# Numero de simulações
num_sim = 10
import os
mean_time = 0
mean_days = 0

probs = [0.6,0.2,0.1]
for j in probs:
    mean_time = 0
    mean_days = 0
    for i in range(num_sim):

        # Used to draw the graph
        n_infected = 0
        n_healthy = 0
        n_recovered = 0
        recovered = []
        infected = []
        healthy = []

        # Used to draw the graph
        total_days = []
        infected_people = []
        healthy_people = []
        recovered_people = []
        population = [healthy_people, infected_people, recovered_people]
        days = 0


        initial_prob = j
        distributiont = "gm"
        mean = 6
        stdd = 1.9

        tempo = time.time()
        run_simulation(total_people= 2000, radius=8, days_until_healed= 6, time_to_spread= 3, initial_prob = initial_prob, distributiont = distributiont, mean = mean, stdd = stdd, infected_proportion= 1/20)
        mean_time += time.time() - tempo
        # Remover esse "if" se quiser ver o grafico para todas as simulações
        if i == 9:
            draw()
            filename = f"distribution = {distributiont} probabilidade = {initial_prob} media = {mean} desvio padrao = {stdd}.png"
            output_folder = r"C:\Users\thiag\OneDrive\Documents\Imagens Simulação"
            plt.savefig(os.path.join(output_folder, filename))


    print("Media de tempo:", mean_time / num_sim)
    print("Media de dias:", mean_days / num_sim)
    print("Media", mean)
    print("Desvio Padrao", stdd)
    print("Probabilidade Inicial", initial_prob)
    print()

    