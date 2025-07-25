public class TestBandPassBasic {
    public static void main(String[] args) {
        Patch patch = new Patch("BandPassDynamic");

        // Modules de base
        GenSine g1 = new GenSine("g1",3000.0,0.5);
        BandPassFIR bandpass = new BandPassFIR("Filter",600,50,100); // On fixe tout
        AudioDataReceiver receiver = new AudioDataReceiver("Output", 0, 0); // Receiver

        // Ajout au patch
        patch.addModule(g1);
        patch.addModule(bandpass);
        patch.addModule(receiver);

        // Connexions
        patch.connect("g1", 0, "Filter", 0); // sinus => filtre (entrée signal)
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
