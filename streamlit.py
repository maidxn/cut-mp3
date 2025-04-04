import streamlit as st
import librosa
import matplotlib.pyplot as plt
import io
import soundfile as sf

# Upload file
uploaded_file = st.file_uploader("Tải file muốn cắt")

if uploaded_file is not None:
    # Load audio using librosa
    audio, sr = librosa.load(uploaded_file)
    
    # Calculate the duration in seconds and convert to minutes
    duration_sec = len(audio) / sr
    max_time = round(duration_sec / 60, 2)


    if "start_time_input" not in st.session_state:
        st.session_state.start_time_input = 0
    if "end_time_input" not in st.session_state:
        st.session_state.end_time_input = max_time


    # Slider for selecting time range
    duration = st.slider(
        "Chọn đoạn thời gian muốn cắt",
        0.0, max_time,
        value=(0.0, max_time),
    )

    start_time_input = st.number_input(
        "Điểm bắt đầu",
        min_value=0.0,
        max_value=max_time,
        value=duration[0]
    )

    end_time_input = st.number_input(
        "Điểm dừng",
        min_value=0.0,
        max_value=max_time,
        value=duration[1]
    )


    start_sample = int(start_time_input * 60 * sr)
    end_sample = int(end_time_input * 60 * sr)

    # Slice the audio to get the selected part
    sliced_audio = audio[start_sample:end_sample]

    st.session_state.start_time_input = start_sample
    st.session_state.end_time_input = end_sample

    
    # Plot waveform
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the waveform
    librosa.display.waveshow(audio, sr=sr, ax=ax)
    ax.axvline(x=st.session_state.start_time_input // sr, color='red', linestyle='--', linewidth=2)
    ax.axvline(x=st.session_state.end_time_input // sr, color='red', linestyle='--', linewidth=2)

    # Labels and title
    ax.set_xlabel("Thời gian (s)")
    ax.set_yticks([])

    # Display the figure in Streamlit
    st.pyplot(fig)


    st.write("Nghe thử bản cắt:")

    st.audio(sliced_audio, sample_rate=sr)
    buffer = io.BytesIO()
    sf.write(buffer, sliced_audio, sr, format='mp3')
    buffer.seek(0)

    # Show download button
    downloaded = st.download_button(
        label="Tải bản cắt",
        data=buffer,
        file_name="cut_audio.mp3",
        mime="audio/mp3"
    )

    # Notify user after download button is clicked
    if downloaded:
        st.success("✅ Tải xuống thành công!")
