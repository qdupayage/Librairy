public class TestBandPassFcBandMod {
    public static void main(String[] args) {
        Patch patch = new Patch("BandPassDynamic");

        // Modules de base
        GenSine g1 = new GenSine("g1",1500.0,0.5);
        BandPassFIR bandpass = new BandPassFIR("Filter",128); // On controlle tout
        AudioDataReceiver receiver = new AudioDataReceiver("Output", 0, 0); // Receiver

        // Module pour créer la fr modulé
        GenSine freqMod = new GenSine("FreqModulator", 30, 600.0); // sinus à 0.7 Hz, amplitude = 600 Hz
        Constant baseFreq = new Constant("BaseFreq", 1000.0); // fréquence centrale fixe 1000 hz
        Mixer resonanceCtrl = new Mixer("FreqCtrl", 2); // somme freqMod + baseFreq, fr oscillant entre 400 et 1600 Hz
        
        // Module pour créer la Bande passante modulé
        GenSine bandMod = new GenSine("bandModulator", 50, 500.0); // sinus à 1.5 Hz, amplitude = 50 Hz
        Constant baseBand = new Constant("BaseBand", 600.0); // Band Passante min 20 Hz
        Mixer bandCtrl = new Mixer("bandCtrl", 2); // somme bandMod + baseBand, largeur oscillant entre 10 et 110 Hz

        // Ajout au patch
        patch.addModule(g1);
        patch.addModule(freqMod);
        patch.addModule(baseFreq);
        patch.addModule(resonanceCtrl);
        patch.addModule(bandMod);
        patch.addModule(baseBand);
        patch.addModule(bandCtrl);
        patch.addModule(bandpass);
        patch.addModule(receiver);

        // Connexions
        patch.connect("FreqModulator", 0, "FreqCtrl", 0); // sinus => resoCTRL
        patch.connect("BaseFreq", 0, "FreqCtrl", 1); // constante => resoCTRL
        patch.connect("bandModulator", 0, "bandCtrl", 0); // sinus => bandCTRL
        patch.connect("BaseBand", 0, "bandCtrl", 1); // constante => bandCTRL
        patch.connect("g1", 0, "Filter", 0); // sinus => filtre (entrée signal)
        patch.connect("FreqCtrl", 0, "Filter", 1); // sortie du mixerfreq => fréquence du filtre
        patch.connect("bandCtrl", 0, "Filter", 2); // sortie du mixerband => largeur du filtre
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
