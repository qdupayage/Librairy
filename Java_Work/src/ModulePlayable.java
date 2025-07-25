import phelmaaudio.AudioData;

public interface ModulePlayable {
    void playAudioData();
    void displayAudioDataWaveform();
    void saveAudioDataToWavFile(String fileName);
    AudioData getAudioData();
}
