import perceval as pcvl
from tqdm.notebook import tqdm
import time

from perceval.algorithm import Sampler

input_state = pcvl.BasicState("|1,1>") 
circuit = pcvl.BS() 
noise_model = pcvl.NoiseModel(transmittance=1, indistinguishability=1, g2=0)

nsamples = 200_000

from perceval import RemoteConfig, RemoteProcessor
import os

remote_config = RemoteConfig()
token = os.environ.get("QUANDELA_TOKEN")
remote_config.set_token(token)
remote_config.save()

remote_processor = RemoteProcessor("sim:slos", noise=noise_model)
remote_processor.set_circuit(circuit)
remote_processor.min_detected_photons_filter(1)
remote_processor.with_input(input_state)

remote_sampler = Sampler(remote_processor, max_shots_per_call=1e6)
remote_sampler.default_job_name = "Simple_circuit" 
remote_job = remote_sampler.sample_count.execute_async(nsamples)
print(remote_job.id)

previous_prog = 0
with tqdm(total=1, bar_format='{desc}{percentage:3.0f}%|{bar}|') as tq:
    tq.set_description(f'Get {nsamples} samples from {remote_processor.name}')
    while not remote_job.is_complete:
        tq.update(remote_job.status.progress/100-previous_prog)
        previous_prog = remote_job.status.progress/100
        time.sleep(1)
    tq.update(1-previous_prog)
    tq.close()

print(f"Job status = {remote_job.status()}")

results = remote_job.get_results()
pcvl.pdisplay(results['results'])

