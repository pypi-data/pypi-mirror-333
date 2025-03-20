import matplotlib.pyplot as plt
import mne
import pandas as pd
from mne.io import Raw


def good_epoch_dur(raw, seg_start, seg_end, seg_len):
    """
    Calculate the valid duration of an epoch, excluding bad segments.

    Returns
    -------
    float
        Valid duration of the epoch.
    """

    bad_dur = sum(max(0, min(anno['onset'] + anno['duration'], seg_end) - max(anno['onset'], seg_start))
                  for anno in raw.annotations if 'Bad_epoch' in anno['description'])

    return max(0, seg_len - bad_dur)


def set_up_raw(raw: Raw, rerefer: bool = False, chan_limit=None,
               montage_temp: str = "standard_1005", is_montage: bool = False, drop_chan=()) -> Raw:
    ch_drop = [
        ch for ch in raw.ch_names
        if ch.startswith('M') or 'EMG' in ch or 'EOG' in ch or 'ECG' in ch or 'chin' in ch.lower() or ch.startswith('E')
    ]
    raw.drop_channels(ch_drop)
    raw.drop_channels(drop_chan, on_missing='warn')
    if chan_limit is not None:
        raw = raw.pick_channels(chan_limit, ordered=False, on_missing='warn')
    if rerefer:
        raw.set_eeg_reference(ref_channels=['M1', 'M2'])
    if is_montage:
        montage = mne.channels.make_standard_montage(montage_temp)
        raw.set_montage(montage, on_missing='warn')
    return raw


def event_lock(raw, SO_candidates, SP_candidates, event_summary, window=1.5, verbose=True):
    """
    Identify spindles occurring within ±1.5 s of each detected SO trough.

    Parameters:
    - raw (mne.io.Raw): EEG raw data.
    - SO_candidates (pd.DataFrame): DataFrame containing detected SO events.
    - SP_candidates (pd.DataFrame): DataFrame containing detected spindle events.
    - sfreq (float): Sampling frequency.
    - window (float): Time window (default: ±1.5s around SO trough).

    Returns:
    - pd.DataFrame: Coupled SO-Spindle events.
    """
    stage_mapping = {0: "Wake", 1: "N1", 2: "N2", 3: "SWS", 4: "REM"}
    sfreq = raw.info['sfreq']
    merged = SO_candidates.merge(SP_candidates, on=['ch_name', 'stage'])
    filtered = merged.query("peak_time >= trough_time - @window and peak_time <= trough_time + @window").copy()
    filtered['Time_diff'] = filtered['peak_time'] - filtered['trough_time']
    filtered['Abs_Time_diff'] = filtered['Time_diff'].abs()

    total_spindles = len(SP_candidates)
    total_SOs = len(SO_candidates)
    total_couplings = len(filtered)

    cp_percent = []
    SPcSO_all = (total_couplings / total_spindles) if total_spindles > 0 else 0
    SOcSP_all = (total_couplings / total_SOs) if total_SOs > 0 else 0
    cp_percent.append({'stage': 'all', 'SPcSO': SPcSO_all, 'SOcSP': SOcSP_all})

    for stage in filtered['stage'].unique():
        total_stage_spindles = len(SP_candidates[SP_candidates['stage'] == stage])
        total_stage_SOs = len(SO_candidates[SO_candidates['stage'] == stage])
        total_stage_couplings = len(filtered[filtered['stage'] == stage])

        SPcSO_stage = (total_stage_couplings / total_stage_spindles) if total_stage_spindles > 0 else 0
        SOcSP_stage = (total_stage_couplings / total_stage_SOs) if total_stage_SOs > 0 else 0

        stage_name = stage_mapping.get(stage, f"Unknown ({stage})")
        cp_percent.append({'stage': stage, 'SPcSO': SPcSO_stage, 'SOcSP': SOcSP_stage})
        if verbose:
            print(f"Spindles coupled with SOs in stage \033[1m{stage_name}\033[0m: {SPcSO_stage * 100:.2f}%")
            print(f"SOs coupled with spindles in stage \033[1m{stage_name}\033[0m: {SOcSP_stage * 100:.2f}%")

    cp_percent_df = pd.DataFrame(cp_percent)
    cp_percent_df['channel'] = 'all'

    cp_percent_channel_list = []
    # Group the filtered events by stage and channel
    for (stage, ch), group in filtered.groupby(['stage', 'ch_name']):
        couplings = group.shape[0]
        sp_channel_count = SP_candidates[(SP_candidates['stage'] == stage) & (SP_candidates['ch_name'] == ch)].shape[0]
        so_channel_count = SO_candidates[(SO_candidates['stage'] == stage) & (SO_candidates['ch_name'] == ch)].shape[0]
        SPcSO_channel = (couplings / sp_channel_count) if sp_channel_count > 0 else 0
        SOcSP_channel = (couplings / so_channel_count) if so_channel_count > 0 else 0
        cp_percent_channel_list.append({
            'stage': stage,
            'ch_name': ch,
            'SPcSO': SPcSO_channel,
            'SOcSP': SOcSP_channel
        })
    cp_percent_channel_df = pd.DataFrame(cp_percent_channel_list)
    # Rename 'ch_name' to 'channel' for consistency
    cp_percent_channel_df.rename(columns={'ch_name': 'channel'}, inplace=True)

    # Add channel-level coupling metrics for stage 'all'
    cp_percent_all_channel_list = []
    # Use filtered coupling counts for all channels regardless of stage
    for ch, couplings in filtered['ch_name'].value_counts().items():
        sp_channel_count = SP_candidates[SP_candidates['ch_name'] == ch].shape[0]
        so_channel_count = SO_candidates[SO_candidates['ch_name'] == ch].shape[0]
        SPcSO_channel = (couplings / sp_channel_count) if sp_channel_count > 0 else 0
        SOcSP_channel = (couplings / so_channel_count) if so_channel_count > 0 else 0
        cp_percent_all_channel_list.append({
            'stage': 'all',
            'channel': ch,
            'SPcSO': SPcSO_channel,
            'SOcSP': SOcSP_channel
        })
    cp_percent_all_channel_df = pd.DataFrame(cp_percent_all_channel_list)

    cp_percent_all = pd.concat([cp_percent_df, cp_percent_channel_df, cp_percent_all_channel_df], ignore_index=True)
    print('event_summary\n', event_summary)
    print('cp_percent_all\n', cp_percent_all)
    event_summary = pd.merge(event_summary, cp_percent_all, left_on=['stage', 'channel_y'],
                             right_on=['stage', 'channel'], how='outer')

    # ** Per-Channel Calculation using the same method **
    channel_counts = filtered['ch_name'].value_counts()
    total_spindles_per_channel = SP_candidates['ch_name'].value_counts()
    total_SOs_per_channel = SO_candidates['ch_name'].value_counts()

    spindle_ratio_per_channel = (channel_counts / total_spindles_per_channel * 100).reindex(
        raw.info['ch_names']).fillna(0)
    SO_ratio_per_channel = (channel_counts / total_SOs_per_channel * 100).reindex(raw.info['ch_names']).fillna(0)

    SO_measure = pd.DataFrame({
        'ch_name': raw.info['ch_names'],
        'Spindles_Coupled_with_SOs': spindle_ratio_per_channel.values
    })

    # Generate topomap
    picks = mne.pick_types(raw.info, eeg=True, exclude='bads')
    SO_measure = SO_measure.set_index('ch_name').reindex([raw.ch_names[pick] for pick in picks]).reset_index()

    if verbose:
        fig, ax = plt.subplots(figsize=(4.5, 4.5))
        im, _ = mne.viz.plot_topomap(SO_measure['Spindles_Coupled_with_SOs'].values, raw.info, axes=ax, show=False,
                                     cmap="Blues")

        im.set_clim(vmin=0, vmax=SO_measure['Spindles_Coupled_with_SOs'].max())
        plt.colorbar(im, ax=ax)
        ax.set_title('Spindles Coupled with SOs (%)')
        plt.show()

    return filtered[['ch_name', 'stage', 'trough_time', 'peak_time', 'amplitude', 'Time_diff']].rename(
        columns={'trough_time': 'SO_trough_time', 'peak_time': 'SP_peak_time',
                 'amplitude': 'SP_amplitude'}), event_summary
