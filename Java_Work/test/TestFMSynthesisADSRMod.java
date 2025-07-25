public class TestFMSynthesisADSRMod {
    public static void main(String[] args) {
        Patch patch = new Patch("FMSynthesis");

        // Génération modules
        Constant baseFreq = new Constant("BaseFreq", 300.0);// 1. Constante de fréquence ((600,300,50) Hz)
        GenSine modulator = new GenSine("Modulator", 0.5, 300.0);// 2. Modulateur : couple essayé: ((0.5,300),(200,50),(440,300),(120,25))
        Mixer freqControl = new Mixer("FreqControl", 2);// 3. Mixer : somme du modulateur et de la constante
        GenSine carrier = new GenSine("Carrier", 1.0); // freq modifiée dynamiquement
        ADSREnvelop adsr = new ADSREnvelop("Envelope", 0.1, 0.1, 1., 2.5, 1.0, 0.7);
        Multiplier mult = new Multiplier("mult", 2, 0.95);
        AudioDataReceiver receiver = new AudioDataReceiver("Output", 0, 0);

        // Ajout modules au patch
        patch.addModule(baseFreq);
        patch.addModule(modulator);
        patch.addModule(freqControl);
        patch.addModule(carrier);
        patch.addModule(adsr);
        patch.addModule(mult);
        patch.addModule(receiver);

        // Connection entre les différents modules
        patch.connect("Modulator", 0, "FreqControl", 0);
        patch.connect("BaseFreq", 0, "FreqControl", 1); 
        patch.connect("FreqControl", 0, "Carrier", 0);  
        patch.connect("Carrier", 0,"mult", 0);
        patch.connect("Envelope", 0,"mult", 1);
        patch.connect("mult", 0,"Output", 0);

        // Exécution
        int durationInSeconds = 3;
        int totalSamples = (int) (ModuleAbstract.SAMPLE_FREQ * durationInSeconds);;
        patch.exec(totalSamples);

        // Lecture
        receiver.playAudioData();
        receiver.displayAudioDataWaveform();
    }
}
