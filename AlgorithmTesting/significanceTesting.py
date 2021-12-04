import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import scipy.stats

def flipBiasedCoin(P): #flip a coin with P probability of landing heads
    number = np.random.rand(1)
    if number > P:
        return 0
    else:
        return 1

def experiment(P, trials): #flip a biased coin trials number of times and record the times it lands heads
    success = np.zeros(trials,)
    for i in range(0,trials):
        success[i] = flipBiasedCoin(P)
    winrate = np.sum(success)/trials
    return winrate

PFoM = 0.7083 #success rate of the FoM algorithm
games = 10000 #this rate was calculated over 10,000 trials

#run 1,000 iterations of the test we did to construct a probability distribution
trials = 1000
experiments = np.zeros(trials,)
for i in tqdm(range(0,trials)):
    experiments[i] = experiment(PFoM, games)
stdev = np.std(experiments)

#and print the statistics
print("Mean success rate: "+ str(np.mean(experiments)))
print("Standard Deviation: "+ str(stdev))

PR = 0.6899 #success rate of the R score algorithm in 10,000 trials

Z = PR/stdev - PFoM/stdev #z score
print('Z score: '+str(Z))
p = 2* scipy.stats.norm.sf(abs(Z)) #p value of Z score
print('p value: '+str(p))

# PtestVec = np.linspace(Pref - 6*stdev,Pref + 6*stdev,100)
# plt.semilogy(PtestVec, scipy.stats.norm.sf(np.abs(PtestVec-Pref)/stdev))
# plt.xlabel('Win Rate of Algorithm')
# plt.ylabel('Z score against reference algorithm')
# plt.show()
