# Perceval_Quandela_Training
Introduction à Perceval

1. Install and Import Dependencies
pip install perceval-quandela

2. Check Perceval Version
import perceval as pcvl
from tqdm.notebook import tqdm
# tqdm pour barre de progression
import time
pcvl.__version__

3. Build circuit
.................................

4. Configure Cloud Access
from perceval import RemoteConfig, RemoteProcessor

remote_config = RemoteConfig()
# stocke la configuration pour se connecter au cloud

remote_config.set_token("ENTER_YOUR_TOKEN_HERE")
# token pour t’identifier auprès du cloud

OU

import os
token = os.environ.get("QUANDELA_TOKEN")
remote_config.set_token(token)

# pour que le token soit sur mon systeme et ne figure pas dans le code
# utiliser .gitignore
remote_config.save()
# sauvegarde le token et la configuration sur ta machine



5. Run a Job on Quandela's Quantum Computer
remote_processor = RemoteProcessor("sim:slos", noise=noise_model)
# sim = simulation sur classical hardware     qpu = quantum hardware
# noise_model definit au 3.
remote_processor.set_circuit(circuit)
# circuit définit au 3.
remote_processor.min_detected_photons_filter(1)
remote_processor.with_input(input_state)
# input_state définit au 3.
remote_sampler = Sampler(remote_processor, max_shots_per_call=1e6)

remote_sampler.default_job_name = "Hello World" 
remote_job = remote_sampler.sample_count.execute_async(nsamples)
print(remote_job.id)

