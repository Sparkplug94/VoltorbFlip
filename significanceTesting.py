import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

def flipBiasedCoin(P): #flip a coin with P probability of heads
    number = np.random.rand(1)
    if number > P:
        return 0
    else:
        return 1

def experiment(P, trials):
    success = np.zeros(trials,)
    for i in range(0,trials):
        success[i] = flipBiasedCoin(P)
    winrate = np.sum(success)/trials
    return winrate

#let's define an "experiment" as testing our algorithm on 1,000 trials
Pref = 0.7173 #win probability of the reference algorithm
games = 3000 #how many games do we play?

#let's run 1000 experiments and find the mean and standard deviation
trials = 10000
experiments = np.zeros(trials,)
for i in tqdm(range(0,trials)):
    experiments[i] = experiment(Pref, games)

stdev = np.std(experiments)
print("Mean success rate: "+ str(np.mean(experiments)))
print("Standard Deviation: "+ str(stdev))

#This is the win probability for the test algorithm
Ptest = 0.744

#The z score of the test algorithm
Z = Ptest/stdev - Pref/stdev
print('Z score: '+str(Z))

PtestVec = np.linspace(Pref - 6*stdev,Pref + 6*stdev,100)
plt.plot(PtestVec, np.abs(PtestVec-Pref)/stdev)
plt.xlabel('Win Rate of Algorithm')
plt.ylabel('Z score against reference algorithm')
plt.show()
