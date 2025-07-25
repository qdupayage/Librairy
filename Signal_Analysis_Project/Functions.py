# Signal 
import wave
import scipy.signal as signal
import scipy.signal.windows as windows
from scipy.stats import kurtosis

# Calculs
from math import log10, log, tan, ceil, pi, isclose
import numpy
import pandas as pd
from typing import List, Tuple

# Plotting 
import plotly.graph_objects as go
import plotly.subplots as sp

# Interface
import os
import streamlit as st

# Wav file function
def readwavfile(filename : str):
    """
    To write a wav file.
    
    Parameters:
    -----------
    filename : str
        Name of the selected data.
        
    Returns:
    --------
    The wav file and the sampling frequency
    """
    # read wave file content
    with wave.open(filename,'rb') as wav_file:
        wav_metadata = wav_file.getparams() #read wave file parameters
        wav_frames = wav_file.readframes(wav_metadata.nframes) #read buffer of frames
    # obtain important parameters
    #print(wav_metadata) #print all parameters
    sampling_frequency = wav_metadata.framerate #sampling frequency
    number_of_samples = wav_metadata.nframes #number of samples
    sample_width_in_bits = 8*wav_metadata.sampwidth #nbr of bits per sample
    print(f"Original sampling frequency: {sampling_frequency} Hz, number of samples: {number_of_samples}, sample width: {sample_width_in_bits} bits")
    # formatting data for processing
    max_data_value = 2**(sample_width_in_bits-1) #maximum value for the data
    data = numpy.frombuffer(wav_frames, dtype='<h') / max_data_value #convert to array + amplitude normalization
    time = numpy.arange(number_of_samples)/sampling_frequency #time base
    return data, sampling_frequency, number_of_samples

def writewavfile(filename : str, data  : numpy.ndarray , sampling_frequency : int):
    """
    To write a wav file.
    
    Parameters:
    -----------
    filename : str
        Name of the selected data.
    data : list of numpy.ndarray
        List of arrays to save
    sampling_frequency : int
        Frequency to write the file
        
    Returns:
    --------
    None, wav file writen.
    """
    # data parameters for saving
    number_of_channels = 1
    sample_width_in_bytes = 2
    # data formatting for wave file
    max_data_value = 2**(8*sample_width_in_bytes -1)
    data_normalized = data / max(abs(data)) #data normalization by max(abs(data))
    frames_wav = numpy.clip(numpy.round(data_normalized * (max_data_value-1)), -max_data_value, max_data_value-1).astype("<h") #int16 (signed)
    # wave file writing
    with wave.open(filename,'wb') as wav_file:
        wav_file.setnchannels(number_of_channels)
        wav_file.setsampwidth(sample_width_in_bytes)
        wav_file.setframerate(sampling_frequency)
        wav_file.writeframes(frames_wav)

def cot(x):
    return 1 / tan(x)

# PreProcessing Function
def resampling_function(data_original : numpy.ndarray, sampling_frq_original : int, upsampling : int = 1, downsampling : int = 1 ):
    """
    Resample an input signal using upsampling and downsampling factors.

    Parameters:
    -----------
    data_original : numpy.ndarray
        Original input signal.
    sampling_frq_original : int
        Original sampling frequency in Hz.
    upsampling : int, optional
        Upsampling factor (default: 1).
    downsampling : int, optional
        Downsampling factor (default: 1).

    Returns:
    --------
    data_resampled : numpy.ndarray
        Resampled signal data.
    sampling_frq_resampled : int
        Resampled sampling frequency in Hz.
    """
    data_resampled = signal.resample_poly(data_original, upsampling, downsampling)
    sampling_frq_resampled = sampling_frq_original * upsampling // downsampling
    Ndata_resampled = len(data_resampled)
    print(f"Resampled sampling frequency: {sampling_frq_resampled} Hz, number of samples: {Ndata_resampled}")
    return data_resampled, sampling_frq_resampled

def filtering_function (data_resampled : numpy.ndarray ,sampling_frq_resampled : int, filter_type : str = 'high', f_stop = 10, f_pass = 40):
    """
    Apply a digital filter to a resampled signal.

    Parameters:
    -----------
    data_resampled : numpy.ndarray
        Resampled input signal.
    sampling_frq_resampled : int
        Sampling frequency of the resampled signal in Hz.
    filter_type : str, optional
        Type of filter to apply ('high', 'low', or 'band', default: 'high').
    f_stop : float or List[float], optional
        Stopband frequency or frequencies in Hz (default: 10).
    f_pass : float or List[float], optional
        Passband frequency or frequencies in Hz (default: 40).

    Returns:
    --------
    data_resampled_filtered : numpy.ndarray
        Filtered signal data.
    filter_coeff : numpy.ndarray
        Filter coefficients.
    """
    # filtering data
    N_filter_min = 1 #no filtering
    N_filter_max = 10001 #filter order limit (for performance)

    # filter specifications
    delta_p = 1/1000

    # filter design
    nyquist_frq = 0.5 * sampling_frq_resampled
    if filter_type == 'high':
            bands = [0, f_stop, f_pass, nyquist_frq]
            desired = [0, 1]
            delta_l = abs(f_pass - f_stop) / sampling_frq_resampled
    elif filter_type == 'low':
            bands = [0, f_pass, f_stop, nyquist_frq]
            desired = [1, 0]
            delta_l = abs(f_pass - f_stop) / sampling_frq_resampled
    elif filter_type == 'band':
            bands = [0, f_stop[0], f_pass[0], f_pass[1], f_stop[1], nyquist_frq]
            desired = [0, 1, 0]
            delta_l = min(abs(f_pass[0] - f_stop[0]), abs(f_pass[1] - f_stop[1])) / sampling_frq_resampled #filter order depends on the smallest transition band
    else:
            N_filter = N_filter_min #default: no filtering
    bands = [min(max(b, 0), nyquist_frq) for b in bands]

    # filter order
    if isclose(delta_l, 0) or isclose(delta_l, 0.5):  #avoid undefined cotangent values
        N_filter = N_filter_min
    else:
        log_term = log10(1 / delta_p)
        try:
            N_filter = ceil((20 * log10(1 / (pi * delta_p)) - 10 * log10(log_term)) / (10 * log10(numpy.exp(1)) * log(cot((pi - 2 * pi * delta_l) / 4))))
        except ValueError:
            N_filter = N_filter_min
    N_filter = min(N_filter + 1 if N_filter % 2 == 0 else N_filter, N_filter_max)  #N_filter odd (for type I FIR filters) and limited to N_filter_max

    # filter coefficients + filtering
    if N_filter > N_filter_min:
        filter_coeff = signal.remez(N_filter, bands, desired, fs=sampling_frq_resampled)
        data_resampled_filtered = signal.lfilter(filter_coeff, [1], data_resampled)
    else:
        data_resampled_filtered = data_resampled #no filtering
    return data_resampled_filtered, filter_coeff

# Get array for analysis:
def get_window_function(window_choice : str, N : int) -> numpy.ndarray:
    """
    To get the window function.
    
    Parameters:
    -----------
    window_choice : str
        Name of the window.
    N : int
        Size our the selected window
        
    Returns:
    --------
    The window function.
    """
    if window_choice == 'Hanning':
        return windows.hann(N)
    elif window_choice == 'Hamming':
        return windows.hamming(N)
    elif window_choice == 'Rectangular':
        return numpy.ones(N)
    elif window_choice == 'Blackman':
        return windows.blackman(N)
    

def get_sliding_window_temp (signal : numpy.ndarray ,fs : int, window_duration : float, overlap_percent : float = 0.5, threshold : int = 0):
    """
    Return the time array to calculate window_functions such as kurthosis

    Parameters:
    -----------
    signal : numpy.ndarray
        Input signal.
    fs : int
        Signal Sample Rate (Hz).
    window_duration : float
        Window duration in seconds.
    overlap_percent : float
        Overlap percent between windows (en %, entre 0 et 1).
    threshold : int
        Start of the time Axis

    Returns:
    --------
    time_axis : numpy.ndarray
        Temporal Axis corresponding to the center of each windows.
    """
    # Taille de la fenêtre en nombre d'échantillons
    n_samples_window = int(window_duration * fs)
    
    # Pas entre les fenêtres (avec recouvrement)
    hop_size = int(n_samples_window * (1 - overlap_percent))
    
    # Initialisation
    time_axis = []

    # Sliding window
    for start in range(0, len(signal) - n_samples_window + 1, hop_size):

        # Window center
        time_axis.append((start + threshold + n_samples_window / 2) / fs)

    return numpy.array(time_axis)

def sliding_window_variance(signal, window_size, overlap):
    """
    Calculate variance of a signal using sliding windows.

    Args:
        signal (numpy.ndarray): Input signal array.
        window_size (int): Number of samples per window.
        overlap (int): Number of overlapping samples between consecutive windows.

    Returns:
        tuple: (variances, window_times) where:
            - variances is a numpy array of variances for each window.
            - window_times is a numpy array of time indices corresponding to the center of each window.
    """
    step = window_size - overlap  # Calculate the step size
    if step <= 0:
        raise ValueError("Step size must be greater than zero. Adjust window_size or overlap.")

    # Get sliding windows using numpy's stride tricks
    windows = numpy.lib.stride_tricks.sliding_window_view(signal, window_shape=window_size)[::step]

    # Calculate variance for each window
    variances = numpy.var(windows, axis=1)

    return variances


def sliding_window_kurtosis(signal: numpy.ndarray, fs: int, window_duration: float, overlap_percent: float = 0.5):
    """
    Applique une fenêtre glissante pour calculer la kurtosis du signal.

    Parameters:
    -----------
    signal : numpy.ndarray
        Le signal d'entrée.
    fs : int
        Fréquence d'échantillonnage du signal (Hz).
    window_duration : float
        Durée de la fenêtre en secondes.
    overlap_percent : float
        Taux de recouvrement entre les fenêtres (en %, entre 0 et 1).

    Returns:
    --------
    kurtosis_values : numpy.ndarray
        Liste des valeurs de kurtosis pour chaque fenêtre.
    time_axis : numpy.ndarray
        Axe temporel correspondant au centre de chaque fenêtre.
    """
    # Window size in samples
    n_samples_window = int(window_duration * fs)
    
    # Hop
    hop_size = int(n_samples_window * (1 - overlap_percent))
    
    # Initialisation
    kurtosis_values = []

    # Sliding window
    for start in range(0, len(signal) - n_samples_window + 1, hop_size):
        segment = signal[start:start + n_samples_window]

        # Kurtosis calculus
        kurt = kurtosis(segment, axis = 0, fisher = True, bias = False )
        kurtosis_values.append(kurt)

    return numpy.array(kurtosis_values)

# Plotting functions

def loading_information(uploaded_file , plot_original):
    """
    Load and display information from an uploaded audio file.
    
    Parameters:
    -----------
    uploaded_file : file-like object
        The uploaded .wav file.
    plot_original : bool
        Whether to display the original waveform plot.

    Returns:
    --------
    original_data : numpy.ndarray
        Audio signal data from the uploaded file.
    original_sample_rate : int
        Sampling rate of the uploaded audio file in Hz.
    original_data_sample : int
        Number of samples in the uploaded audio file.
    """
    original_data, original_sample_rate, original_data_sample = readwavfile(uploaded_file)
    st.session_state["current_data"] = original_data
    st.session_state["current_sample_rate"] = original_sample_rate
    st.session_state["original_sample"] = original_data_sample

    # Affichage du signal original
    if plot_original:
        original_plot =  plot_scatter(numpy.arange(len(st.session_state["current_data"])) / st.session_state["current_sample_rate"], st.session_state["current_data"], "Original Waveform", x_title="Time (s)", y_title="Amplitude", ind= 2)
        st.session_state["original_plot_AD"] = original_plot
        st.plotly_chart(st.session_state["original_plot_AD"])
    return original_data, original_sample_rate, original_data_sample

def plot_waveforms(sample_rate, resampled_data, filtered_data, downsample_factor):
    """
    Plot original and filtered waveforms with downsampled data for visualization.
    
    Parameters:
    -----------
    sample_rate : int
        Sampling rate of the audio signal in Hz.
    resampled_data : numpy.ndarray
        Resampled waveform data.
    filtered_data : numpy.ndarray
        Filtered waveform data.
    downsample_factor : int
        Factor by which the data is downsampled for plotting.

    Returns:
    --------
    fig_resampled_filtered : plotly.graph_objects.Figure
        Plotly figure showing original and filtered waveforms.
    """
    time_resampled = numpy.arange(len(resampled_data)) / sample_rate
    time_filtered = numpy.arange(len(filtered_data)) / sample_rate

    resampled_data_plot = resampled_data[::downsample_factor]
    filtered_data_plot = filtered_data[::downsample_factor]
    
    time_resampled_plot = time_resampled[::downsample_factor]
    time_filtered_plot = time_filtered[::downsample_factor]

    fig_resampled_filtered = go.Figure()
    fig_resampled_filtered.add_trace(go.Scatter(x=time_resampled_plot, y=resampled_data_plot, mode='lines', name='Original Waveform', line=dict(dash='dot')))
    fig_resampled_filtered.add_trace(go.Scatter(x=time_filtered_plot, y=filtered_data_plot, mode='lines', name='Filtered Waveform'))
    fig_resampled_filtered.update_layout(title=f'Original and Filtered Waveforms (Sample Rate: {sample_rate} Hz)', xaxis_title='Time [s]', yaxis_title='Amplitude')
    return(fig_resampled_filtered)

def plot_frequency_response(b, resampled_sample_rate):
    """
    Plot the frequency response of a filter in both dB and linear scales.
    
    Parameters:
    -----------
    b : numpy.ndarray
        Filter coefficients.
    resampled_sample_rate : int
        Sampling rate of the resampled signal in Hz.

    Returns:
    --------
    None
        Displays two Plotly figures in Streamlit:
        1. Frequency response in dB scale.
        2. Frequency response in linear scale.
    """
    w, h = signal.freqz(b, worN=8000)
    w = w / numpy.pi * (resampled_sample_rate / 2)

    fig_freq_response_db = go.Figure()
    fig_freq_response_db.add_trace(go.Scatter(x=w, y=20 * numpy.log10(abs(h)), mode='lines', name='Frequency Response (dB)'))
    fig_freq_response_db.update_layout(title=f'Frequency Response (dB Scale, Sample Rate: {resampled_sample_rate} Hz)', xaxis_title='Frequency [Hz]', yaxis_title='Amplitude (dB)')
    st.plotly_chart(fig_freq_response_db)

    fig_freq_response_linear = go.Figure()
    fig_freq_response_linear.add_trace(go.Scatter(x=w, y=abs(h), mode='lines', name='Frequency Response (Linear)'))
    fig_freq_response_linear.update_layout(title=f'Frequency Response (Linear Scale, Sample Rate: {resampled_sample_rate} Hz)', xaxis_title='Frequency [Hz]', yaxis_title='Amplitude')
    st.plotly_chart(fig_freq_response_linear)

def plot_scatter( x_arrays : numpy.ndarray, y_arrays : numpy.ndarray, name : str ,fig = None,mode : str = 'lines', x_title : str ="X-axis", y_title : str="Y-axis", X_lim : List[Tuple[int,int]] = [0,0] , Y_lim : List[Tuple[int,int]] = [0,0], ind :int = 1 ):
    """
    Plot a custom graph with Plotly.
    
    Parameters:
    -----------
    x_arrays : numpy.ndarray
        List of arrays for the X-axis.
    y_arrays : numpy.ndarray
        List of arrays for the Y-axis.
    name : tuple of str
        Name of the plots (must match the number of plots).
    fig : plotly figure
        If we want to add graph to an allready created figure
    mode : str
        Mode for Scatter: 'lines', 'markers',...
    x_title : str
        Label for the X-axis.
    y_title : str
        Label for the Y-axis.
    X_lim : int
        Limits for the X-axis plot
    Y_lim : int
        Limits for the Y-axis plot
    
    Returns:
    --------
    None (displays the graph).
    """
    if len(x_arrays) != len(y_arrays):
        raise ValueError("The lengths of x_arrays and y_arrays must be equal.")

    if fig == None:
        # Create the figure
        fig = go.Figure()
    
    # Add trace
    fig.add_trace(go.Scatter(
        x=x_arrays, y=y_arrays,
        mode=mode,
        name=name,
        line=dict(width=1)
    ))
    
    if X_lim == [0,0] and Y_lim == [0,0]:
        # Update layout with custom limits and labels
        fig.update_layout(
            title=name,
            title_font=dict(size=15),
            xaxis_title=x_title,
            yaxis_title=y_title,
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
            legend=dict(
                x=1, y=1, traceorder='normal',
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='Black', borderwidth=1
            )
        )

    else:
        if X_lim ==[0,0]:
            # Update layout with custom limits and labels
            fig.update_layout(
                title=name,
                title_font=dict(size=15),
                xaxis_title=x_title,
                yaxis_title=y_title,
                yaxis=dict(
                    title = y_title,
                    range = (Y_lim[0],Y_lim[1])
                ),
                legend=dict(
                    x=1, y=1, traceorder='normal',
                    bgcolor='rgba(255, 255, 255, 0)',
                    bordercolor='Black', borderwidth=1
                )
            )
        elif Y_lim ==[0,0] : 
            # Update layout with custom limits and labels
            fig.update_layout(
                title=name,
                title_font=dict(size=15),
                xaxis_title=x_title,
                yaxis_title=y_title,
                xaxis=dict(
                    title = x_title,
                    range = (X_lim[0],X_lim[1])
                ),
                legend=dict(
                    x=1, y=1, traceorder='normal',
                    bgcolor='rgba(255, 255, 255, 0)',
                    bordercolor='Black', borderwidth=1
                )
            )
        else:
            # Update layout with custom limits and labels
            fig.update_layout(
                title=name,
                title_font=dict(size=15),
                xaxis_title=x_title,
                yaxis_title=y_title,
                xaxis=dict(
                    title = x_title,
                    range = (X_lim[0],X_lim[1])
                ),
                yaxis=dict(
                    title = y_title,
                    range = (Y_lim[0],Y_lim[1])
                ),
                legend=dict(
                    x=1, y=1, traceorder='normal',
                    bgcolor='rgba(255, 255, 255, 0)',
                    bordercolor='Black', borderwidth=1
                )
            )
    if ind == 1:
        return fig
    else:
        return fig

def plot_heatmap(x : numpy.ndarray , y : numpy.ndarray, z : numpy.ndarray, title : str = "Heatmap", x_title : str ="X-axis", y_title : str ="Y-axis", colorbar_title : str ="Color Scale", colorscale : str ='Jet', height : int =400):
    """
    Plot a heatmap using Plotly.
    
    Parameters:
    -----------
    x : numpy.ndarray
        Array representing the X-axis.
    y : numpy.ndarray
        Array representing the Y-axis.
    z : numpy.ndarray
        2D array representing the heatmap values.
    title : str
        Title of the plot.
    x_title : str
        Label for the X-axis.
    y_title : str
        Label for the Y-axis.
    colorbar_title : str
        Title for the color bar.
    colorscale : str
        Colormap for the heatmap (default: 'Jet').
    height : int
        Height of the plot in pixels.
    
    Returns:
    --------
    Figure.
    """
    # Create the figure
    fig = go.Figure()
    
    # Add heatmap trace
    fig.add_trace(go.Heatmap(
        z=z,                # Heatmap data
        x=x,                # X-axis values
        y=y,                # Y-axis values
        colorscale=colorscale,
        colorbar=dict(title=colorbar_title)
    ))
    
    # Update layout with titles and axis labels
    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        height=height,
        template="plotly"
    )
    
    # Return the plot
    return fig

# Analysis functions
def Spectrogram(data: numpy.ndarray, frq: int, window_choice: str = 'Hanning', overlap_percent: int = 50, zp: int = 1, N: int = 1000,start : int =0, plot_scale: str = 'dB', want_to_show: bool = True):
    """
    Compute and optionally display the spectrogram of a signal.

    Parameters:
    -----------
    data : numpy.ndarray
        Input signal data.
    frq : int
        Sampling frequency of the input signal in Hz.
    window_choice : str, optional
        Type of window function to use (default: 'Hanning').
    overlap_percent : int, optional
        Percentage of overlap between adjacent windows (default: 50).
    zp : int, optional
        Zero-padding factor for FFT (default: 1).
    N : int, optional
        Window size in samples (default: 1000).
    plot_scale : str, optional
        Scale for the spectrogram plot ('dB' or 'linear', default: 'dB').
    want_to_show : bool, optional
        Whether to display the spectrogram plot (default: True).

    Returns:
    --------
    Spgx : numpy.ndarray
        Spectrogram data (Power Spectral Density).
    f : numpy.ndarray
        Frequency axis in Hz.
    wd_s : float
        Window duration in seconds.
    od_s : float
        Overlap duration in seconds.
    """
    # Define parameters for the Spectrogram
    nfft = zp * N                                                          # Applying zero-padding on the FFT
    noverlap = int((overlap_percent / 100) * N)                            # Numbers of chevauching points
    hop = N - noverlap                                                     # The increment in samples, by which the window is shifted in each step.

    # Calculate spectrogram and energy indicators using ShortTimeFFT
    stft_obj = signal.ShortTimeFFT(
        win= get_window_function(window_choice, N),                 # Window function as array
        hop=hop,                                                        # Hop size
        fs=frq,                                       # Sampling frequency
        fft_mode='onesided2X',                                          # Use one-sided FFT, to only calcul non-negative values
        mfft=nfft,                                                      # Zero-padded FFT length
        scale_to='psd'                                                  # Scale to power spectral density
    )

    # Spectrogram Data
    Spgx = stft_obj.spectrogram(data)                         # Spectrogram Data
    N_win = Spgx.shape[1]                                     # Number of windows needed for the spectro
    f = stft_obj.f                                            # Frequency
    delta_t = hop / frq                               # Temporal resolution of the spectrogram
    t_seconds = start/frq + numpy.arange(N_win) * delta_t # Time (in second) that correspond to the Spgx
    wd_s = N/frq                                      # Time (in second) that correspond to the window duration
    od_s = noverlap/frq                               # Time (in second) that correspond to the overlap duration

    # Convertion for plot_scale
    if plot_scale == 'dB':
        SpgxdB = 10 * numpy.log10(Spgx)                                    # dB scale convertion
        plot_data = SpgxdB
        colorbar_title = '[dB]'
    else:
        plot_data = Spgx                                                # linear scale
        colorbar_title = '[linear]'
    # Plotting the Spectrogram
    if want_to_show == True:

        plot_heatmap(t_seconds, f, plot_data, title="Spectrogram", x_title="Time [s]", y_title="Frequency [Hz]", colorbar_title=colorbar_title, colorscale='Jet', height=400)
    else: 
        pass

    return Spgx,f,t_seconds,wd_s,od_s

def band_energy_over_time( Spgx : numpy.ndarray, frequencies : numpy.ndarray, t_seconds : numpy.ndarray,  freq_bands : List[Tuple[float, float]] , plot : bool = False, L : List[int] = []):
    """
    Plot the energy contained in frequency bands over time.
    
    Parameters:
    -----------
    Spgx : numpy.ndarray
        Spectrogram data (PSD values).
    frequencies : numpy.ndarray
        Frequency axis in Hz.
    t_seconds : numpy.ndarray
        Time axis in seconds.
    freq_bands : List[Tuple[float, float]]
        List of frequency bands as (f_min, f_max) in Hz.
    plot : bool, optional
        Whether to generate and display the plot (default: False)
    L : List[int]
        To plot only the selected band
        
    Returns:
    --------
    Shows a Plotly graph.
    band_energies : list of numpy.ndarray
        List of band_energy.
    """
    # Prepare the figure
    fig = go.Figure()

    # Creating the List of ndarray
    band_energies = []
    
    # Frequency resolution
    delta_f = frequencies[1] - frequencies[0]
    
    # Loop through each frequency band
    if L == []:
        for band in freq_bands:
            f_min, f_max = band
            
            # Find the indices corresponding to the frequency band
            freq_indices = numpy.where((frequencies >= f_min) & (frequencies <= f_max))[0]

            # To ensure that frequencies are here
            if len(freq_indices) == 0:
                print(f"Warning: No frequencies found in the band {f_min}-{f_max} Hz!")
                continue
            
            # Calculate energy for each time point
            band_energy = numpy.sum(Spgx[freq_indices, :], axis=0) * delta_f
            band_energies.append(band_energy)
            
            # Add trace to the plot
            fig.add_trace(go.Scatter(
                x=t_seconds,
                y=band_energy,
                mode='lines',
                name=f"{f_min}-{f_max} Hz"
            ))

    else:
        for idx in L:
            f_min, f_max = freq_bands[idx]
            
            # Find the indices corresponding to the frequency band
            freq_indices = numpy.where((frequencies >= f_min) & (frequencies <= f_max))[0]

            # To ensure that frequencies are here
            if len(freq_indices) == 0:
                print(f"Warning: No frequencies found in the band {f_min}-{f_max} Hz!")
                continue
            
            # Calculate energy for each time point
            band_energy = numpy.sum(Spgx[freq_indices, :], axis=0) * delta_f
            band_energies.append(band_energy)
            
            # Add trace to the plot
            fig.add_trace(go.Scatter(
                x=t_seconds,
                y=band_energy,
                name=f"{f_min}-{f_max} Hz",
                mode = 'lines'
            ))

    # Update layout
    fig.update_layout(
        title="Energy in Frequency Bands Over Time",
        xaxis_title="Time [s]",
        yaxis_title="Energy [Units]",
        legend_title="Frequency Bands",
        template="plotly",
        height=500,
        width=800
    )

    if plot == True :       
        # Show the plot
        st.plotly_chart(fig)

    return band_energies, fig

# Saving functions
def save_1D_to_csv(freq_psd, psd, filepath, indexname : str = 'Frequency [Hz]'):
    """
    Save a 1 dimension vector to a CSV file with the argument str as the index and a single column for values. Made to save PSD values at first

    Args:
        freq_psd (np.ndarray): 1D array of frequency values.
        psd (np.ndarray): 1D array of PSD values corresponding to frequencies.
        filepath (str): Full path to the CSV file to save.

    Returns:
        None
    """
    # Validate input dimensions
    if len(freq_psd) != len(psd):
        raise ValueError(
            f"Dimension mismatch: Frequency axis {len(freq_psd)}, PSD values {len(psd)}"
        )
    
    # Create DataFrame
    df = pd.DataFrame({'Value': psd}, index=freq_psd)
    df.index.name = indexname
    
    # Save to CSV
    df.to_csv(filepath)

def save_spectrogram_to_csv(spectrogram, time_axis, freq_axis, filename):
    """
    Save a spectrogram to a CSV file with time and frequency labels.

    Args:
        spectrogram (np.ndarray): 2D array of spectrogram values (frequency x time).
        time_axis (np.ndarray): 1D array representing the time axis (columns).
        freq_axis (np.ndarray): 1D array representing the frequency axis (rows).
        filename (str): Path to the CSV file to save.

    Returns:
        None
    """
    # Dimension validation
    if spectrogram.shape[0] != len(freq_axis) or spectrogram.shape[1] != len(time_axis):
        raise ValueError(
            f"Dimension mismatch: Spectrogram shape {spectrogram.shape}, "
            f"Frequency axis {len(freq_axis)}, Time axis {len(time_axis)}"
        )
    
    # Create a DataFrame with frequency as the index and time as the columns
    df = pd.DataFrame(spectrogram, index=freq_axis, columns=time_axis)
    df.index.name = 'Frequency [Hz]'
    df.columns.name = 'Time [s]'

    # Save to CSV
    df.to_csv(filename)

def save_EI_to_csv(EI, time_axis, filename):
    """
    Save energie indicator to a CSV file.

    Args:
        EI (List[np.ndarray]): 1D array of energy_band values.
        time_axis (np.ndarray): 1D array representing the time axis (columns).
        filename (str): Path to the CSV file to save.

    Returns:
        None
    """
    # Validation de dimensions
    if any(len(band) != len(time_axis) for band in EI):
        raise ValueError(
            f"Dimension mismatch: Each energy band must have the same length as the time axis ({len(time_axis)})."
        )

    # Créer un DataFrame où chaque colonne représente une bande d'énergie
    columns = [f"Energy_Band_{i+1}" for i in range(len(EI))]
    df = pd.DataFrame(numpy.array(EI).T, index=time_axis, columns=columns)
    df.index.name = 'Time [s]'

    # Enregistrer en CSV
    df.to_csv(filename)

