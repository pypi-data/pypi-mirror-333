import mne
import numpy as np
import pandas as pd
from scipy.io import loadmat

from somnopy.utils import good_epoch_dur


def load_raw(file_path):
    if file_path.endswith('.vhdr'):
        return mne.io.read_raw_brainvision(file_path, preload=True, verbose='ERROR')
    elif file_path.endswith('.edf'):
        tbd = mne.io.read_raw_edf(file_path, preload=True, verbose='ERROR')
        return tbd
    elif file_path.endswith('.fif'):
        return mne.io.read_raw_fif(file_path, preload=True, verbose='ERROR')
    elif file_path.endswith('.set'):
        return mne.io.read_raw_eeglab(file_path, preload=True, verbose='ERROR')
    elif file_path.endswith('.bdf'):
        return mne.io.read_raw_bdf(file_path, preload=True, verbose='ERROR')
    elif file_path.endswith('.cnt'):
        return mne.io.read_raw_cnt(file_path, preload=True, verbose='ERROR')
    else:
        raise ValueError(f"Unsupported file format: {file_path}")


def load_hypnogram_data(file_path):
    """
    Load hypnogram data for a given subject.

    Parameters
    ----------
    file_path : str or None
        File path to the scoring file. If None, a default path is constructed.

    Returns
    -------
    numpy.ndarray
        Array of sleep stage values.
    """
    try:
        return load_hypnogram_data_mat(file_path)
    except:
        return load_hypnogram_data_txt(file_path)


def load_hypnogram_data_mat(file_path):
    """
    Load hypnogram data for a given subject.

    Parameters
    ----------
    file_path : str or None
        File path to the scoring file. If None, a default path is constructed.

    Returns
    -------
    numpy.ndarray
        Array of sleep stage values.
    """
    scoring = loadmat(file_path)
    stages = scoring['stageData']['stages']
    stages = np.concatenate([np.concatenate(stage) for stage in stages])
    stages_df = pd.DataFrame(stages, columns=['stages'])
    stages[stages == 5] = '4'
    stages[stages == 7] = '0'
    stages_df.iloc[-1] = 0
    stages_df['stages'] = stages_df['stages'].astype(int)

    return stages_df['stages'].values.flatten()


def load_hypnogram_data_txt(file_path):
    """
    Load hypnogram data for a given subject.

    Parameters
    ----------
    file_path : str or None
        File path to the scoring file. If None, a default path is constructed.

    Returns
    -------
    numpy.ndarray
        Array of sleep stage values.
    """
    scoring = np.genfromtxt(file_path, skip_header=True, dtype=None)
    stages = [stage[0] for stage in scoring]
    stages_df = pd.DataFrame(stages, columns=['stages'])
    stages[stages == 5] = '4'
    stages[stages == 7] = '0'
    stages_df.iloc[-1] = 0
    stages_df['stages'] = stages_df['stages'].astype(int)

    return stages_df['stages'].values.flatten()


def hypnogram_segment(raw, interval=30, bad_epoch=True, file_paths=None):
    """
    Segment hypnogram data into intervals corresponding to sleep stages.

    Parameters
    ----------
    raw: mne.io.Raw
        An instance of Raw EEG data from MNE Python.
    interval : int, optional
        Interval duration in seconds. Default is 30.
    bad_epoch : bool, optional
        Whether to mark stage 6 as bad epochs. Default is True.
    file_paths : str or None
        File path to the scoring file.

    Returns
    -------
    list of tuples
        List of tuples containing (stage, segment length, valid duration).
    """
    if not file_paths:
        print('Please provide a file path for your scoring file.')
    hypno = load_hypnogram_data(file_path=file_paths)
    stage_segments = []
    cur_stage, cnt, seg_start = hypno[0], 0, 0

    for i, stage in enumerate(hypno):
        if stage == cur_stage:
            cnt += 1
        else:
            seg_len = cnt * interval
            seg_end = seg_start + seg_len
            valid_dur = good_epoch_dur(raw, seg_start, seg_end, seg_len)
            stage_segments.append((cur_stage, seg_len, valid_dur))
            cur_stage, cnt, seg_start = stage, 1, seg_end

        if bad_epoch:
            if stage == 6:
                onset = i * interval
                bad_epoch = mne.Annotations(
                    onset=onset,
                    duration=interval,
                    description='Bad_epoch',
                    orig_time=None
                )
                raw.set_annotations(bad_epoch)

    seg_len = cnt * interval
    seg_end = min(seg_start + seg_len, raw.times[-1])  # Ensure segment end is not later than raw_end_time
    seg_len = seg_end - seg_start  # Recalculate the segment length if needed
    valid_dur = good_epoch_dur(raw, seg_start, seg_end, seg_len)
    stage_segments.append((cur_stage, seg_len, valid_dur))

    return stage_segments
