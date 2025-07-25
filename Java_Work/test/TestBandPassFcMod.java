public class TestBandPassFcMod {
    public static void main(String[] args) {
        Patch patch = new Patch("BandPassDynamic");

        // Modules de base
        GenSine g1 = new GenSine("g1",2000.0,0.5);
        BandPassFIR bandpass = new BandPassFIR("Filter",100,128); // On controlle la fréquence
        AudioDataReceiver receiver = new AudioDataReceiver("Output", 0, 0); // Receiver

        // Module pour créer la fr modulé
        GenSine freqMod = new GenSine("FreqModulator", 0.7, 600.0); // sinus à 0.7 Hz, amplitude = 600 Hz
        Constant baseFreq = new Constant("BaseFreq", 1000.0); // fréquence centrale fixe 1000 hz
        Mixer resonanceCtrl = new Mixer("FreqCtrl", 2); // somme freqMod + baseFreq, fr oscillant entre 400 et 1600 Hz

        // Ajout au patch
        patch.addModule(g1);
        patch.addModule(freqMod);
        patch.addModule(baseFreq);
        patch.addModule(resonanceCtrl);
        patch.addModule(bandpass);
        patch.addModule(receiver);

        // Connexions
        patch.connect("FreqModulator", 0, "FreqCtrl", 0); // sinus => resoCTRL
        patch.connect("BaseFreq", 0, "FreqCtrl", 1); // constante => resoCTRL
        patch.connect("g1", 0, "Filter", 0); // sinus => filtre (entrée signal)
        patch.connect("FreqCtrl", 0, "Filter", 1); // sortie du mixerfreq => fréquence du filtre
        patch.connect("Filter", 0, "Output", 0); // sortie du filtre => audio

        // Exécution
        int durationInSeconds = 3;
        int totalSamples = (int) (ModuleAbstract.SAMPLE_FREQ * durationInSeconds);;
        patch.exec(totalSamples);

        // Lecture audio et visualisation
        receiver.playAudioData();
        receiver.displayAudioDataWaveform();
    }
}
