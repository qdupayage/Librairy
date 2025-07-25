import streamlit as st
import numpy as np
import Functions as fct
import os
from scipy.signal import welch

@st.cache_data

def reset_page_states():
    """Reset states specific to pages to avoid sharing between tabs."""
    for key in list(st.session_state.keys()):
        if key not in ["active_tab", "pages"]:
            del st.session_state[key]

def loading_information(uploaded_file, plot_original) :
    original_data, original_sample_rate, original_data_sample = fct.readwavfile(uploaded_file)
    st.session_state["current_data"] = original_data
    st.session_state["current_sample_rate"] = original_sample_rate
    st.session_state["original_sample"] = original_data_sample
    st.write(f"Fréquence d'échantillonnage : {original_sample_rate} Hz")
    st.write(f"Nombre d'échantillons : {len(original_data)}")

    # Affichage du signal original
    if plot_original:
        original_plot = fct.plot_scatter(np.arange(len(st.session_state["current_data"])) / st.session_state["current_sample_rate"], st.session_state["current_data"], "Original Waveform", x_title="Time (s)", y_title="Amplitude", ind= 2)
        st.session_state["original_plot_AD"] = original_plot
        st.plotly_chart(st.session_state["original_plot_AD"])
    return original_data, original_sample_rate, original_data_sample

def analyse_data_page():
    # Dictionary to translate usuals windows' names into welsh argument
    dico = {'Hamming' : 'hamming', 'Hanning' : 'hann', 'Blackman' : 'blackman', 'Rectangle' : 'boxcar'}

    st.title("Analyse Data")
    st.write("You choose to analyse your data, please upload and process a wav file.")

    # St.session_state initialisation
    if "original_data" not in st.session_state:
        st.session_state["original_data"] = None
        st.session_state["original_sample_rate"] = None 

    # Loading .wav file
    uploaded_file = st.file_uploader("Upload a WAV file", type="wav")

    if uploaded_file:
        try:
            # Load file data if a new file is upload
            if uploaded_file != st.session_state.get("last_uploaded_file"):
                st.session_state["last_uploaded_file"] = uploaded_file
                st.session_state["original_data"], st.session_state["original_sample_rate"], st.session_state["original_sample_number"] = fct.loading_information(uploaded_file, False)
                st.session_state["plot_shown"] = False  # Réinitialiser l'état du plot  
                st.write(f"Fréquence d'échantillonnage : {st.session_state['original_sample_rate']} Hz")
                st.write(f"Nombre d'échantillons : {st.session_state['original_sample_number']}") 

            # Option for original waveform plot
            plot_original = st.checkbox("Plot Original Waveform_AD", key= 'plot_original_button')
            if plot_original:
                st.session_state['original_plot'] = fct.plot_scatter(np.arange(st.session_state["original_sample_number"]) / st.session_state["original_sample_rate"],
                                                st.session_state["original_data"], "Original Waveform",
                                                x_title="Time (s)",
                                                y_title="Amplitude"
                                                )
                
                if st.button("Show graphic", key='show_button_1'):
                    # Generate the figure and plotlly_chart(fig)
                    st.plotly_chart(st.session_state['original_plot'])
                    st.write("Plot of the original data.")
            # Window choice selection
            window_choice = st.selectbox(
                "Choose a window (window_choice):",
                ["Hamming", "Hanning", "Blackman", "Rectangular"],
                key="Window Choice"
            )
            st.session_state["window_choice"] = window_choice

            # Plot scale selection
            plot_scale = st.selectbox(
                "Choose the plot scale:",
                ["dB", "linear"],
                key="Plot scale"
            )
            st.session_state["plot_scale"] = plot_scale

            # Overlap percentage selection
            overlap_percent = float(st.slider(
                "Choose the overlap percentage:",
                min_value=10, max_value=90, step=10, value=50,
                key="Overlap percentage"
            ))
            st.session_state["overlap_percent"] = overlap_percent

            # Zero-padding factor and size in samples for the window
            zp = int(st.number_input(
                "Enter zero-padding value (zp):",
                min_value=1, step=1, value=1, key="Zero padding factor"
            ))
            st.session_state["zp"] = zp

            N = int(st.number_input(
                "Enter the number of samples per window:",
                min_value=1, step=1, value=st.session_state["current_sample_rate"],
                key="Number of samples in window"
            ))
            st.session_state["N"] = N

            folder_path = st.text_input("Enter the folder to save the processed data:", "Saved_Data")

            # Allow user to shrink the time axis for analysis
            if st.checkbox("Do you want to shrink the time period ?", key="shrink_checkbox"):
                # Slider or number inputs for x-axis limits
                st.write("Set the Times-axis display range (in seconds):")
                x_min = st.number_input("Min time:", value=60, step=1)
                x_max = st.number_input("Max time:", value=360, step=1)

                # Validate user input
                if x_min < x_max:
                    start_sample = int(x_min * st.session_state["current_sample_rate"])
                    st.session_state["start_sample"] = start_sample
                    end_sample = int(x_max * st.session_state["current_sample_rate"])
                    st.session_state["selected_data"] = st.session_state["current_data"][start_sample:end_sample]
                else:
                    st.warning("Invalid range: Ensure X-axis min is less than max.")
                    x_lim = None

            # If there is no selected_data, take the original one
            if "selected_data" not in st.session_state:
                st.session_state["selected_data"] = st.session_state["original_data"]

            # To have a matching time representation
            if "start_sample" not in st.session_state:
                st.session_state["start_sample"] = 0

            # Welch PSD Calculation
            if st.checkbox("Calculate the PSD using Welch", key="Calculate_PSD"):
                # Welch method parameters 
                fs = st.session_state["original_sample_rate"]
                nperseg = st.session_state["N"]
                noverlap = int(st.session_state["overlap_percent"] / 100 * nperseg)

                freq_psd, psd = welch(
                    st.session_state["selected_data"],
                    fs=fs,
                    window=dico[st.session_state["window_choice"]],
                    nperseg=nperseg,
                    noverlap=noverlap,
                    nfft=nperseg * st.session_state["zp"]
                )
                st.session_state["freq_psd"] = freq_psd
                st.session_state["psd"] = psd

                if st.session_state["plot_scale"] == 'dB':
                    psd_dB = 10 * np.log10(psd)  # dB scale conversion
                    psd_data = psd_dB
                    y_title = "Power Spectral Density [dB]"
                else:
                    psd_data = psd  # Linear scale
                    y_title = "Power Spectral Density [linear]"

                st.session_state['psd_plot'] = fct.plot_scatter(
                    freq_psd,
                    psd_data,
                    name="Power Spectral Density (Welch)",
                    x_title="Frequency [Hz]",
                    y_title=y_title
                )
            input_PSD_name = st.text_input('Enter a name for the PSD file :', 'PSD_data', key='PSD_input_name')
            save_PSD = st.button("Do you want to save the PSD Data?", key = 'Save_PSD')
            if save_PSD:
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)  # Create folder if it doesn't exist
                
                # Define the full file path
                full_path = os.path.join(folder_path, input_PSD_name)

                try:
                    fct.save_1D_to_csv(freq_psd , psd_data ,full_path)
                    st.success(f"Spectrogram saved as '{input_PSD_name}' in '{folder_path}' folder.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

            # Plot the PSD if selected
            plot_psd = st.button("Do you want to plot the PSD?", key="PSD_Plot")
            if plot_psd:
                st.plotly_chart(st.session_state['psd_plot'])
                st.write("PSD plotted successfully.")

            # Spectrogram Calculation
            if st.checkbox("Calculate the spectrogram", key="Calculate_spectrogram"):
                st.session_state["Spgx"], st.session_state["freq"],st.session_state['time_window'], st.session_state["wd_s"], st.session_state["od_s"] = fct.Spectrogram(
                    st.session_state["selected_data"],
                    st.session_state["current_sample_rate"],
                    st.session_state["window_choice"],
                    st.session_state["overlap_percent"],
                    st.session_state["zp"],
                    st.session_state["N"],
                    st.session_state['start_sample'],
                    st.session_state["plot_scale"],
                    False
                )

                if st.session_state["plot_scale"] == 'dB':
                    SpgxdB = 10 * np.log10(st.session_state["Spgx"])  # dB scale conversion
                    plot_data = SpgxdB
                    colorbar_title = '[dB]'
                else:
                    plot_data = st.session_state["Spgx"]  # Linear scale
                    colorbar_title = '[linear]'
                
                st.session_state['spectro_plot'] = fct.plot_heatmap(
                    st.session_state["time_window"],
                    st.session_state["freq"],
                    plot_data,
                    title="Spectrogram",
                    x_title="Time [s]",
                    y_title="Frequency [Hz]",
                    colorbar_title=colorbar_title,
                    colorscale='Jet',
                    height=400
                )

            input_SF_name = st.text_input('Enter a filename :', 'spectrogram_data', key= 'Input_SF_name')
            save_spectro = st.button("Do you want to save the spectrogram Data?", key = 'Save_spectro')
            if save_spectro:
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)  # Create folder if it doesn't exist
                
                # Define the full file path
                full_path = os.path.join(folder_path, input_SF_name)

                try:
                    fct.save_spectrogram_to_csv(plot_data, st.session_state['time_window'], st.session_state['freq'],full_path)
                    st.success(f"Spectrogram saved as '{input_SF_name}' in '{folder_path}' folder.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

            # Plot the spectrogram if selected
            plot = st.button("Do you want to plot the spectrogram?", key="Spectro_Plot")
            if plot:
                st.plotly_chart(st.session_state['spectro_plot'])
                st.write("Spectrogram plotted successfully.")

            # Number of selected bands to study
            num_bands = int(st.number_input("Number of bands to study:", min_value=1, step=1, value=1, key = 'Numbers of studied bands'))
            st.session_state['num_bands'] = num_bands
            frequency_bands = []
            for i in range(num_bands):
                f_central = float(st.number_input(f"Central frequency for Band {i + 1} (Hz):", min_value=50.0, step=10.0,value=150.0, key = f"central frequency of band {i+1}"))
                half_width = float(st.number_input(f"Half-width for Band {i + 1} (Hz):", min_value=0.0, step=5.0,value=10.0, key = f"Width of studied {i+1} band"))
                f_min = f_central - half_width
                f_max = f_central + half_width
                frequency_bands.append((f_min, f_max))

            if 'Spgx' in st.session_state:
                # To save the energy indicator and the plot
                st.session_state['ei'], st.session_state['ei_plot'] = fct.band_energy_over_time(st.session_state["Spgx"],st.session_state["freq"],st.session_state["time_window"], frequency_bands,False)

            # Option to plot the energy_indicators
            plot_ei = st.button("Do you want to plot the energy band?", key = 'Plot_band')
            if plot_ei:
                st.plotly_chart( st.session_state['ei_plot'])

            input_EI_name = st.text_input('Enter a filename :', 'band_energies_data', key= 'Input_EI_name')
            save_ei = st.button("Do you want to save the energy band?", key = 'Save_band')
            if save_ei:
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)  # Create folder if it doesn't exist
                
                # Define the full file path
                full_path = os.path.join(folder_path, input_EI_name)

                try:
                    fct.save_EI_to_csv(st.session_state['ei'], st.session_state['time_window'],full_path)
                    st.success(f"Band-Energies saved as '{input_EI_name}' in '{folder_path}' folder.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        except Exception as e:
            st.error(f"An error occurred during processing: {e}")

def pre_processing ():
    st.title("Pre-process the Data")
    st.write("You chose the Pre-Processing function, please upload and process a WAV file.")

    # Chargement du fichier .wav
    uploaded_file = st.file_uploader("Upload a WAV file", type="wav")

    if uploaded_file:
        try:
            # Load original data
            plot_original = st.button("Plot Original Waveform_PP")
            original_data, original_sample_rate, original_data_sample = fct.loading_information(uploaded_file, plot_original)
            st.session_state["original_data"] = original_data
            st.session_state["original_sample_rate"] = original_sample_rate

            # Resampling
            apply_resample = st.checkbox("Resampling", key = "key_resampling")
            if apply_resample:
                up_ratio = st.number_input("Upsample Ratio", min_value=1, step=1, key="upsampling factor")
                down_ratio = st.number_input("Downsample Ratio", min_value=1, step=1, key="downsampling factor")
                resample_button_clicked = st.button("Apply Resampling", key = 'resample_button')  # Bouton pour valider les ratios
                st.session_state["down_ratio"] = down_ratio

                if resample_button_clicked:
                    resampled_data, resampled_sample_rate = fct.resampling_function(original_data, original_sample_rate, up_ratio, down_ratio)
                    st.session_state["current_data"] = resampled_data
                    st.session_state["resampled_data"] = resampled_data
                    st.session_state["current_sample_rate"] = resampled_sample_rate
                    st.session_state["resampling"] = True
                    if st.session_state["resampling"] == True:
                        # Plotting the resampled data
                        resampled_plot = fct.plot_scatter(np.arange(len(st.session_state["current_data"])) , st.session_state["current_data"], "Resampled Waveform", x_title="Time (s)", y_title="Amplitude",ind= 2)
                        st.session_state["resampled_plot"] = resampled_plot
                        st.plotly_chart(st.session_state["resampled_plot"], key="resampled_plot")
                    
            # Filtrage
            apply_filter = st.checkbox("Apply Filter", key = 'apply_filter')
            if apply_filter:
                filter_type = st.selectbox("Filter Type", ["low", "high", "band"], key = 'filter_type')
                if filter_type == "low":
                    fpass = st.number_input("Passband Edge Frequency", min_value=0.0, value=st.session_state["current_sample_rate"] / 8, key="fpassage_low")
                    fstop = st.number_input("Stopband Edge Frequency", min_value=0.0, value=3 * st.session_state["current_sample_rate"] / 8, key="fcoupure_low")
                elif filter_type == "high":
                    fpass = st.number_input("Passband Edge Frequency", min_value=0.0, value=3 * st.session_state["current_sample_rate"] / 8, key="fpassage_high")
                    fstop = st.number_input("Stopband Edge Frequency", min_value=0.0, value=st.session_state["current_sample_rate"] / 8, key="fcoupure_high")
                elif filter_type == "band":
                    fpass = [
                        st.number_input("Passband Edge Frequency 1", min_value=0.0, value=st.session_state["current_sample_rate"] / 8, key="fpassage_band1"),
                        st.number_input("Passband Edge Frequency 2", min_value=0.0, value=3 * st.session_state["current_sample_rate"] / 8, key="fpassage_band2")
                    ]
                    fstop = [
                        st.number_input("Stopband Edge Frequency 1", min_value=0.0, value=0.0, key="fcoupure_band1"),
                        st.number_input("Stopband Edge Frequency 2", min_value=0.0, value=st.session_state["current_sample_rate"] / 2, key="fcoupure_band2")
                    ]
                filtering_button_clicked = st.button("Filtering", key = 'filter_button')
                if filtering_button_clicked:
                    filtered_data, filter_coef = fct.filtering_function(st.session_state["current_data"], st.session_state["current_sample_rate"] , filter_type, fstop, fpass)
                    st.session_state["filtered_data"] = filtered_data
                    st.session_state["filter_coef"] = filter_coef
                    st.session_state["filtering"] = True

                    # Check if we have the filtered_data loaded
                    if st.session_state["filtering"]:

                        # Plot of the filter's response:
                        filter_plot = fct.plot_frequency_response(st.session_state["filter_coef"], st.session_state["current_sample_rate"])

                        # Plot of both the original and the filtered data
                        filtered_plot = fct.plot_waveforms(st.session_state["current_sample_rate"],st.session_state["original_data"], st.session_state["filtered_data"], st.session_state["down_ratio"])
                        st.session_state["filtered plot"] = filtered_plot
                        st.plotly_chart(st.session_state["filtered plot"], key="filtered_plot")
            # File saving
            if st.checkbox("Save the filtered .wav data", key="save_output"):
                output_file_name = st.text_input("Name of the output file", value="output_filtered.wav")
                if st.button("Save", key="save_button"):
                    fct.writewavfile(st.session_state["output_file_name"], st.session_state["current_data"], st.session_state["current_sample_rate"])
                    st.success(f" WAV file save as : {output_file_name}")

        except Exception as e:
            st.error(f"Error when loading or processing the file : {e}")

# def energy_indicator():
#     st.title("Energy Indicator")
#     st.write("You chose the Energy Indicator method, please upload and process a WAV file.")
#     for key in [
#     "resampled_data", "resampled_sample_rate", "filtered_data",
#     "current_data", "current_sample_rate", "original_sample","wd_s","od_s"
#     ]:
#         st.session_state[key] = None
#     st.write("You choose the Energy Analysis method, please upload and process a wav file.")

#     # Initialisation des variables dans `st.session_state`
#     if "current_data" not in st.session_state:
#         st.session_state["current_data"] = None
#     if "resampled_sample_rate" not in st.session_state:
#         st.session_state["current_sample_rate"] = None
#     if "filtered_data" not in st.session_state:
#         st.session_state["filtered_data"] = None

#     # Chargement du fichier .wav
#     uploaded_file = st.file_uploader("Upload a WAV file", type="wav")
    
#     if uploaded_file:
#         try:
#             # Load original data
#             plot_original = st.checkbox("Plot Original Waveform_EI")
#             original_data, original_sample_rate, original_data_sample = loading_information(uploaded_file, plot_original)

#             # Window_choice selection
#             window_choice = st.selectbox(
#                 "Choisissez une fenêtre (window_choice) :",
#                 ["Hamming", "Hanning", "Blackman", "Rectangular"], key = 'Window Choice'
#             )
#             st.session_state["window_choice"] = window_choice

#             # Plot_scale selection
#             plot_scale = st.selectbox(
#                 "Choose the plot_scale :",
#                 ["dB", "linear"], key = 'Plot scale'
#             )
#             st.session_state["plot_scale"] = plot_scale

#             # Overlap_percent selection
#             overlap_percent = float(st.slider(
#                 "Choose the overlap percentage :",
#                 min_value=50, max_value=90, step=10, value=50, key = 'Overlap percentage'
#             ))
#             st.session_state["overlap_percent"] = overlap_percent

#             # zero-padding factor and size in samples for the window
#             zp = int(st.number_input(
#                 "Enter zéro-padding value (zp) :",
#                 min_value=1, step=1, value=1, key = 'zero padding factor'
#             ))
#             st.session_state["zp"] = zp

#             N = int(st.number_input(
#                 "Enter the number of samples per window :",
#                 min_value=1, step=1, value=1000, key = 'Numbers of samples in windows'
#             ))
#             st.session_state["N"] = N
#             num_bands = int(st.number_input("Number of bands to study:", min_value=1, step=1, value=1, key = 'Numbers of studied bands'))
#             st.session_state['num_bands'] = num_bands
#             frequency_bands = []
#             for i in range(num_bands):
#                 f_central = float(st.number_input(f"Central frequency for Band {i + 1} (Hz):", min_value=50.0, step=10.0, key = f"central frequency of band {i+1}"))
#                 half_width = float(st.number_input(f"Half-width for Band {i + 1} (Hz):", min_value=0.0, step=5.0, key = f"Width of studied {i+1} band"))
#                 f_min = f_central - half_width
#                 f_max = f_central + half_width
#                 frequency_bands.append((f_min, f_max))

#             # Spectrogram Calculation 
#             if "Spgx" not in st.session_state or st.session_state.get("parameters_updated", True):
#                 Spgx, freq, wd_s, od_s = fct.Spectrogram(
#                     st.session_state["current_data"], 
#                     st.session_state["framerate"], 
#                     st.session_state["window_choice"], 
#                     st.session_state["overlap_percent"], 
#                     st.session_state["zp"], 
#                     st.session_state["N"], 
#                     st.session_state["plot_scale"], 
#                     False
#                 )
#                 st.session_state["Spgx"] = Spgx
#                 st.session_state["freq"] = freq
#                 st.session_state["wd_s"] = wd_s
#                 st.session_state["od_s"] = od_s
#                 st.session_state["parameters_updated"] = False 

#             # Ensure scalar conversion for overlap and window durations
#             wd_s = float(wd_s) if isinstance(wd_s, np.ndarray) and wd_s.size == 1 else wd_s
#             od_s = float(od_s) if isinstance(od_s, np.ndarray) and od_s.size == 1 else od_s

#             time_window = fct.get_sliding_window_temp(st.session_state['selected_file'], st.session_state['framerate'], st.session_state["wd_s"], st.session_state["od_s"])
#             st.session_state["time_window"] = time_window

#             # Optional plot
#             plot = st.checkbox("Do you want to plot?", key = 'Plot')
#             if plot:
#                 fct.band_energy_over_time(st.session_state["Spgx"], st.session_state["freq"], st.session_state["time_window"], frequency_bands, True)
#                 st.write("Energy band plot updated.")
#         except Exception as e:
#             st.error(f"Error during processing: {e}")

def Statistics ():
    for key in [
    "resampled_data", "resampled_sample_rate", "filtered_data",
    "current_data", "current_sample_rate", "original_sample","wd_s","od_s"
    ]:
        st.session_state[key] = None

    st.title("Statistics")
    st.write("You choose the statistics method, please upload and process a wav file.")

    # Chargement du fichier .wav
    uploaded_file = st.file_uploader("Upload a WAV file", type="wav")

    if uploaded_file:
        try:
            # All the .wav files
            selected_file, framerate, N_data = fct.readwavfile(uploaded_file)
            st.session_state["current_data"] = selected_file
            st.session_state["current_sample_rate"] = framerate

            # Define parameters for window size and overlap
            N = int(
                st.number_input(
                    "Enter the number of samples per window:",
                    min_value=1, step=1, value=framerate,
                    key="Number of sample in a window"
                )
            )

            overlap_percent = float(
                st.slider(
                    "Choose the overlap percentage:",
                    min_value=10, max_value=90, step=10, value=50,
                    key="Overlap Percentage"
                )
            )
            noverlap = int((overlap_percent / 100) * N)  # Calculate overlap in samples

            # Initialisation de l'état de session
            if "variance_values" not in st.session_state:
                st.session_state["variance_values"] = None
                st.session_state["variance_window_times"] = None

            if "kurtosis_values" not in st.session_state:
                st.session_state["kurtosis_values"] = None
                st.session_state["kurtosis_window_times"] = None

            # Affichage des informations de base
            st.write(f"Original Sampling Frequency: {framerate} Hz")
            st.write(f"Original Samples: {N_data}")

            # Calculate window and overlap durations in seconds
            wd_s = N / framerate
            od_s = noverlap / framerate
            

            if st.button("Analyse_variance", key= 'analyse_varaince'):
                variance_values= fct.sliding_window_variance(
                    selected_file,
                    N,
                    noverlap
                )
                st.session_state["variance_values"] = variance_values
                st.session_state["vartime"] = fct.get_sliding_window_temp(
                    selected_file,
                    st.session_state['current_sample_rate'],
                    wd_s,
                    od_s
                )
                st.success("Variance calculation complete.")

            if st.button("Kurtosis", key='Kurtosis_button'):
                # Kurtosis calculation
                kurtosis_values= fct.sliding_window_kurtosis(
                    st.session_state["current_data"],
                    st.session_state["current_sample_rate"],
                    wd_s,
                    od_s
                )
                window_times = fct.get_sliding_window_temp(
                    st.session_state["current_data"],
                    st.session_state["current_sample_rate"],
                    wd_s,
                    od_s
                )

                # Update session state
                st.session_state["kurtosis_kurtosis_values"] = kurtosis_values
                st.session_state["kurtosis_window_times"] = window_times

                st.write("Kurtosis calculation complete.")

            # Plot results if requested
            if st.button("Do you want to plot the variance results?", key="variance_plot_checkbox"):
                if st.session_state["variance_values"] is not None and st.session_state["vartime"] is not None:
                    var_plot = fct.plot_scatter(
                        st.session_state["vartime"],
                        np.abs(st.session_state["variance_values"]),
                        "Variance",
                        ind=2
                    )
                    st.session_state["variance_plot"] = var_plot
                    st.plotly_chart(st.session_state["variance_plot"], key= 'variance_plot_chart')
                    st.write("Variance plot displayed.")
                else:
                    st.warning("No Variance values available to plot. Please run the analysis first.")
            if st.button("Do you want to plot the kurtosis results?", key="kurtosis_plot_checkbox"):
                if st.session_state["kurtosis_kurtosis_values"] is not None and st.session_state["kurtosis_window_times"] is not None:
                    kurtosis_plot = fct.plot_scatter(
                        st.session_state["kurtosis_window_times"],
                        np.abs(st.session_state["kurtosis_kurtosis_values"]),
                        "Kurtosis",
                        ind=2
                    )
                    st.session_state["kurtosis_plot"] = kurtosis_plot
                    st.plotly_chart(st.session_state["kurtosis_plot"], key= 'variance_plot')
                    st.write("Kurtosis plot displayed.")
                else:
                    st.warning("No Kurtosis values available to plot. Please run the analysis first.")

            # Sauvegarde du fichier
            if st.checkbox("Save Data as CSV file", key="save_output"):
                folder_path = st.text_input("Enter the folder to save the processed data:", "Saved_Data")
                input_kurt_name = st.text_input('Enter a filename :', 'kurt_data', key= 'Input_kurt_name')
                save_kurt = st.button("Do you want to save the Kurthosis data?", key = 'Save_kurt')
                if save_kurt:
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)  # Create folder if it doesn't exist
                    
                    # Define the full file path
                    full_path = os.path.join(folder_path, input_kurt_name)

                    try:
                        fct.save_1D_to_csv(st.session_state["kurtosis_window_times"],st.session_state["kurtosis_kurtosis_values"],full_path,'Time [s]')
                        st.success(f"Kurtosis values saved as '{input_kurt_name}' in '{folder_path}' folder.")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                input_var_name = st.text_input('Enter a filename :', 'variance_data', key= 'Input_var_name')
                save_var = st.button("Do you want to save the variance data?", key = 'Save_var')
                if save_var:
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)  # Create folder if it doesn't exist
                    
                    # Define the full file path
                    full_path = os.path.join(folder_path, input_var_name)

                    try:
                        fct.save_1D_to_csv(st.session_state["kurtosis_window_times"],st.session_state["kurtosis_kurtosis_values"],full_path,'Time [s]')
                        st.success(f"Variance values saved as '{input_var_name}' in '{folder_path}' folder.")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

        except Exception as e:
            st.write(f"Error during kurthosis plot : {e}")
# API Tittle
st.title("Mon Application Streamlit")

# Initialize session state
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Analyse Data"

# Define pages
pages = {
    "Analyse Data": analyse_data_page,
    "Pre-processing": pre_processing,
    "Statistics": Statistics
}
st.session_state["pages"] = pages

# Display tabs
selected_tab = st.selectbox("Select a tab:", list(pages.keys()), index=list(pages.keys()).index(st.session_state["active_tab"]))

# Update active tab and reset states if switching
if selected_tab != st.session_state["active_tab"]:
    st.session_state["active_tab"] = selected_tab
    reset_page_states()

# Call the function for the selected tab
st.session_state["pages"][selected_tab]()

   