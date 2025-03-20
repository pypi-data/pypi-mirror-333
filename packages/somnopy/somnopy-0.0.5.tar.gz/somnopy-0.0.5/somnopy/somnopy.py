import math
import os

import pandas as pd
from mne.io import Raw

from somnopy.event_detection import SO_detection, SP_detection
from somnopy.metrics import pac
from somnopy.preprocessing import load_raw, hypnogram_segment
from somnopy.utils import event_lock, set_up_raw

#  TODO: add method for saving files on the notebook
#   TODO: Add custom method for spindle detection

# TODO: can compare with Melissa's data

# TODO: Can we look at the spindle frequency


def get_sosp(raw: Raw, stage, interest_stage=('N2', 'SWS'),
             sp_method='Hahn2020',
             so_method='Staresina', coupling=False,
             filter_freq=None, duration=None, filter_type: str = 'fir', l_freq: float = None,
             h_freq: float = None, dur_lower: float = None, dur_upper: float = None,
             baseline: bool = True, verbose: bool = True):
    _, so_candidate, so_summary = SO_detection(raw, stage, target_stage=interest_stage, method=so_method,
                                               baseline=baseline, verbose=verbose, filter_freq=filter_freq,
                                               duration=duration, filter_type=filter_type)
    _, sp_candidate, sp_summary = SP_detection(raw, stage, target_stage=interest_stage, method=sp_method,
                                               l_freq=l_freq, h_freq=h_freq, dur_lower=dur_lower,
                                               dur_upper=dur_upper, baseline=baseline, verbose=verbose)
    event_summary = pd.merge(so_summary, sp_summary, on=['stage'], how='outer')

    cp_event = None
    so_waveform = None

    if coupling:
        cp_event, event_summary = event_lock(raw, so_candidate, sp_candidate, event_summary, verbose=verbose)
        cp_event.insert(0, 'subject', id)
        event_summary, so_waveform = pac(raw, cp_event, event_summary, verbose=verbose)
    return event_summary, cp_event, so_waveform


def get_sosp_for_folder(raw_folder: str, stage_folder: str, interest_stage=('N2', 'SWS'),
                        sp_method='Hahn2020',
                        so_method='Staresina', coupling=True, scoring_dur=30, rerefer=False, chan_limit=None,
                        ch_drop=(),
                        montage_temp="standard_1005", is_montage=True,
                        filter_freq=None, duration=None, filter_type: str = 'fir', l_freq: float = None,
                        h_freq: float = None, dur_lower: float = 0.5, dur_upper: float = math.inf,
                        baseline: bool = True, verbose: bool = True):
    file_paths = [os.path.join(raw_folder, f) for f in os.listdir(raw_folder) if
                  f.endswith(('.vhdr', '.edf', '.fif', '.set', '.fdt', '.bdf', '.cnt'))]
    coupling_event_all = {}
    event_summary_all = {}
    so_waveform_all = {}

    for file_path in file_paths:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        print(f"\033[1mStart event detection for subject {file_name}.\033[0m")
        raw = load_raw(file_path)
        raw = set_up_raw(raw, rerefer=rerefer, chan_limit=chan_limit, drop_chan=ch_drop,
                         montage_temp=montage_temp, is_montage=is_montage)

        stage = None
        if os.path.isfile(os.path.join(stage_folder, f"{file_name}.mat")):
            stage = hypnogram_segment(raw=raw, interval=scoring_dur,
                                      file_paths=os.path.join(stage_folder, f"{file_name}.mat"))
        elif os.path.isfile(os.path.join(stage_folder, f"{file_name}.txt")):
            stage = hypnogram_segment(raw=raw, interval=scoring_dur,
                                      file_paths=os.path.join(stage_folder, f"{file_name}.txt"))
        else:
            print(f"Neither {file_name}.mat nor {file_name}.txt exists in the folder.")

        event_summary, coupling_event, so_waveform = get_sosp(raw, stage,
                                                              interest_stage=interest_stage, sp_method=sp_method,
                                                              so_method=so_method, coupling=coupling,
                                                              filter_freq=filter_freq, duration=duration,
                                                              filter_type=filter_type, l_freq=l_freq,
                                                              h_freq=h_freq, dur_lower=dur_lower, dur_upper=dur_upper,
                                                              baseline=baseline, verbose=verbose)

        event_summary_all[file_name] = event_summary
        coupling_event_all[file_name] = coupling_event
        so_waveform_all[file_name] = so_waveform
    return event_summary_all, coupling_event_all, so_waveform_all
