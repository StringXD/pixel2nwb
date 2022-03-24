from datetime import datetime
from dateutil.tz import tzlocal
from pynwb import NWBFile
import numpy as np
import h5py
import pandas as pd


currPath = r'H:\FC data\SPKINFO\191209_51_learning8_g0\191209_51_learning8_g0_imec0_cleaned\FR_All_1000.hdf5'

start_time = datetime(2019, 12, 9, 14, tzinfo=tzlocal())


nwbfile = NWBFile(session_description='DPA_WT',  # required
                  identifier='191209_51_learning8_g0',  # required
                  session_start_time=start_time)
nwbfile.add_trial_column(name='samp', description='sample odor type')
nwbfile.add_trial_column(name='test', description='test odor type')
nwbfile.add_trial_column(name='delay', description='delay duration')
nwbfile.add_trial_column(name='lick', description='lick or not')
nwbfile.add_trial_column(name='is_WT', description='is welltrain or not')
nwbfile.add_trial_column(name='outcome', description='correct or error')


with h5py.File(currPath, "r") as ffr:
    trials = np.array(ffr["Trials"], dtype="double").T

for tidx in range(trials.shape[0]):
    nwbfile.add_trial(start_time=trials[tidx,0], stop_time=trials[tidx,1], samp=trials[tidx,4],
                      test=trials[tidx,5],delay=trials[tidx,7],lick=trials[tidx,6],
                      is_WT=trials[tidx,8],outcome=trials[tidx,9])



print(nwbfile.trials.to_dataframe())

from pynwb import NWBHDF5IO

io = NWBHDF5IO('example_file_path.nwb', mode='w')
io.write(nwbfile)
io.close()  


io = NWBHDF5IO('example_file_path.nwb', 'r')
nwbfile_in = io.read()