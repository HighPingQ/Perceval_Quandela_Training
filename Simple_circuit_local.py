import perceval as pcvl
from tqdm.notebook import tqdm
import time

from perceval.algorithm import Sampler
#permet de generer des échantillons aléatoires
input_state = pcvl.BasicState("|1,1>") # un photon dans chaque mode

circuit = pcvl.BS() # beam splitter idéal

noise_model = pcvl.NoiseModel(transmittance=0.05, indistinguishability=0.85, g2=0.03) # On ajoute du bruit ( 5% de transmis, photon pas totalement identiques, avec du bruit)

#noise_model = pcvl.NoiseModel(transmittance=1, indistinguishability=1, g2=0) #Test du HOM effect

processor = pcvl.Processor("SLOS", circuit, noise=noise_model) # On définit un processeur qui va executé mon circuit
# "Slos" = Strong Linear Optical Simulator

processor.min_detected_photons_filter(1) # On pose un filtre qui garde uniquement les sorties qui ont au moins 1 photon détecté
processor.with_input(input_state) # on injecte l'état |1,1> dans le circuit

nsamples = 200_000
sampler = Sampler(processor)
samples = sampler.sample_count(nsamples)['results']
# On genere 200000 tirages aléatoires et on compte combien de fois chaque sortie est apparue

probs = sampler.probs()['results'] # on calcule directement les probabilités théoriques exactes de chaque sortie

print(f"Samples: {samples}")
print(f"Probabilities: {probs}")

