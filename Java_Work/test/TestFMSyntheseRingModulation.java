public class TestFMSyntheseRingModulation {
    public static void main(String[] args) {
        Patch patch = new Patch("FMSynthesis");

        // Génération modules
        Constant baseFreq = new Constant("BaseFreq", 300.0);// 1. Constante de fréquence ((600,300,50) Hz)
        GenSine modulator = new GenSine("Modulator", 440.0, 300.0);// 2. Modulateur : couple essayé: ((200,50),(440,300),(120,25))
        GenSine modulator2 = new GenSine("Modulator2", 560,200);
        Multiplier mult = new Multiplier("mult", 2,0.9);
        Mixer freqControl = new Mixer("FreqControl", 2);// 3. Mixer : somme du modulateur et de la constante
        Mixer freqControl2 = new Mixer("FreqControl2", 2);
        GenSine carrier = new GenSine("Carrier", 1.0); // freq modifiée dynamiquement
        GenSine carrier2 = new GenSine("Carrier2", 1.0); // freq modifiée dynamiquement
        AudioDataReceiver receiver = new AudioDataReceiver("Output", 0, 0);

        // Ajout modules au patch
        patch.addModule(baseFreq);
        patch.addModule(modulator);
        patch.addModule(modulator2);
        patch.addModule(mult);
        patch.addModule(freqControl);
        patch.addModule(freqControl2);
        patch.addModule(carrier);
        patch.addModule(carrier2);
        patch.addModule(receiver);

        // Connection entre les différents modules
        patch.connect("Modulator", 0, "FreqControl", 0);
        patch.connect("BaseFreq", 0, "FreqControl", 1);
        patch.connect("Modulator2", 0, "FreqControl2", 0);
        patch.connect("BaseFreq", 0, "FreqControl2", 1); 
        patch.connect("FreqControl", 0, "Carrier", 0);  
        patch.connect("FreqControl2", 0, "Carrier2", 0); 
        patch.connect("Carrier", 0, "mult", 0);
        patch.connect("Carrier2", 0, "mult", 1);
        patch.connect("mult", 0, "Output", 0);

        // 6. Exécution
        int durationInSeconds = 3;
        int totalSamples = (int) (ModuleAbstract.SAMPLE_FREQ * durationInSeconds);;
        patch.exec(totalSamples);

        // Lecture
        receiver.playAudioData();
        receiver.displayAudioDataWaveform();
    }
}
