# Perceval_Quandela_Training
Introduction à Perceval

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
# Le token ne figure pas dans le code
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
