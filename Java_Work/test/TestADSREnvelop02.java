public class TestADSREnvelop02 {
    public static void main(String[] args) {
        // Création du patch principal
        Patch patch = new Patch("Test ADSR");

        // Générateur sinusoïdal modulé en amplitude
        GenSine freqSource = new GenSine("freqSource", 440., 1.0);
        GenSine gen = new GenSine("SineModulated", 1.0); // amplitude sera modulée

        // Enveloppe ADSR (ici : attaque = 0.1s, decay = 0.1s, sustain = 1s, release = 0.5s)
        ADSREnvelop adsr = new ADSREnvelop("Envelope", 0.1, 0.1, 10., 3.5, 1.0, 0.7);
        Multiplier mult = new Multiplier("mult",2,0.9);

        // Récepteur audio
        AudioDataReceiver output = new AudioDataReceiver("output", 0, 0);

        // Ajout des modules au patch
        patch.addModule(freqSource);
        patch.addModule(gen);
        patch.addModule(adsr);
        patch.addModule(mult);
        patch.addModule(output);

        // Connexion : sortie fréqSource → entrée de fréquence du GenSine, sortie ADSR → entrée d’amplitude du GenSine
        patch.connect("freqSource", 0, "SineModulated", 0);
        patch.connect("SineModulated", 0, "mult", 0);
        patch.connect("Envelope", 0, "mult", 1);

        // Connexion : sortie sinusoïdale → sortie audio
        patch.connect("mult", 0, "output", 0);

        // Durée totale du test : 3 secondes
        int totalSamples = (int)(ModuleAbstract.SAMPLE_FREQ *3);

        // Exécution du patch
        patch.exec(totalSamples);

        // Lecture audio (à vérifier que le son évolue en attaque, decay, sustain, puis s’éteint)
        System.out.println(">> Lecture du son avec enveloppe ADSR");
        for (AudioDataReceiver recv : patch.getAudioReceivers()) {
            recv.playAudioData(); // PB ADSR
            recv.displayAudioDataWaveform();
        }
    }
}
