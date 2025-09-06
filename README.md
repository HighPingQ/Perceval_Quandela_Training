# Perceval Basics

## 1. Fock states
```python
import perceval as pcvl

fock_state = pcvl.BasicState("|1,1>") # Equivalent à fock_state = pcvl.BasicState("[1,1]")
print("number of modes", fock_state.m)
print("number of photons", fock_state.n)
print("the state", fock_state)
```

## 2. Building a Circuit
```python
import perceval as pcvl

#OPTION 1
circuit = pcvl.Circuit(n) #n nombre de modes
circuit.add((0, 1), pcvl.BS())
# Premier Beam splitter entre les deux modes
circuit.add((0, 1), pcvl.BS())
# Phase shifter sur le mode 0
circuit.add(0, pcvl.PS(phi=value))
# Deuxième BS entre les deux modes
circuit.add((0, 1), pcvl.BS())
# Affiche le circuit
pcvl.pdisplay(circuit)

# OPTION 2 
circuit = pcvl.Circuit(2) // pcvl.BS() // pcvl.PS(phi=value) // pcvl.BS()
```

## 3. Noise 

Dans Perceval, NoiseModel permet d'ajouter du bruit à la simulation
```python
noise_model = pcvl.NoiseModel(
    brightness=1,          # Intensité ou taux de génération des photons
    g2=0,                  # Paramètre de cohérence à deux photons (photons supplémentaires possibles si >0)
    indistinguishability=1, # Indiscernabilité des photons (1 = parfait)
    transmittance=1,       # Fraction de photons passant à travers un élément optique sans perte
    phase_imprecision=0    # Erreurs sur la phase introduites par les composants
)
```


# Hello world Perceval
Premier programme Perceval

---

## 1. Install and Import Dependencies

```bash
pip install perceval-quandela
```

## 2. Check Perceval Version
```python
import perceval as pcvl
from tqdm.notebook import tqdm  # tqdm pour barre de progression
import time
pcvl.__version__  # Vérifie la version de Perceval installée
```

## 3. Build Circuit
......................

## 4. Configure Cloud Access
```python
from perceval import RemoteConfig, RemoteProcessor

# Sauvegarde la configuration du cloud sur ta machine
remote_config = RemoteConfig()

# Option 1 : insérer le token directement (à éviter pour les dépôts publics)
remote_config.set_token("ENTER_YOUR_TOKEN_HERE")

# Option 2 : récupérer le token depuis le systeme
# Pour enregistrer le token depuis powershell: setx QUANDELA_TOKEN "TON_TOKEN_ICI"
import os
token = os.environ.get("QUANDELA_TOKEN")
remote_config.set_token(token)  # Le token ne figure pas dans le code

remote_config.save()  # Sauvegarde la configuration sur la machine
```

## 5. Run a Job on Quandela's Quantum Computer
```python
# Crée le RemoteProcessor
remote_processor = RemoteProcessor("sim:slos", noise=noise_model)
# noise_model definit au 3.
# sim = simulation sur ordinateur classique
# qpu = matériel quantique

# Associer le circuit et l'état d'entrée
remote_processor.set_circuit(circuit)
# circuit définit au 3.
remote_processor.min_detected_photons_filter(1)
remote_processor.with_input(input_state)
# input_state définit au 3.

remote_sampler = Sampler(remote_processor, max_shots_per_call=1e6)
remote_sampler.default_job_name = "Hello World" 

# Exécute le job de manière asynchrone
remote_job = remote_sampler.sample_count.execute_async(nsamples)
print(remote_job.id)

```
## 6. Monitor Job Progress

Ajout d'une barre de progression pour voir l'avancement du programme

```python

previous_prog = 0 
with tqdm(total=1, bar_format='{desc}{percentage:3.0f}%|{bar}|') as tq:
    tq.set_description(f'Get {nsamples} samples from {remote_processor.name}')
    while not remote_job.is_complete:
        tq.update(remote_job.status.progress/100-previous_prog)
        previous_prog = remote_job.status.progress/100
        time.sleep(1) # Pause dans le programme
    tq.update(1-previous_prog)
    tq.close()

print(f"Job status = {remote_job.status()}")

```

## 7. Retrieve and Display Results
On affiche le résultat

```python
results = remote_job.get_results()
pcvl.pdisplay(results['results']) # afficher les résultats de manière lisible et ordonnée
```

Avec le job id on va pouvoir retrouver les résultats d'un job déjà lancé, terminé ou en cours. Il n’exécute pas le circuit à nouveau.

```python
job_id = "put_your_job_id_here" 
remote_processor = RemoteProcessor("put_your_platform_name_here")
remote_job = remote_processor.resume_job(job_id)

results = remote_job.get_results()   
pcvl.pdisplay(results['results'])

```
## 8. Extra Tools

Visualiser le circuit 

```python
pcvl.pdisplay(circuit)
```

Questionner les QPUs et afficher leurs performances.
Clock indique combien de photons sont générés par seconde (80 MHz signifie 80 millions de photons par seconde).

```python
ascella = pcvl.RemoteProcessor("qpu:ascella")
perf_ascella = ascella.performance
print(f"The Performance of Ascella is: {perf_ascella}")

belenos = pcvl.RemoteProcessor("qpu:belenos")
perf_belenos = belenos.performance
print(f"The Performance of Belenos is: {perf_belenos}")
```


