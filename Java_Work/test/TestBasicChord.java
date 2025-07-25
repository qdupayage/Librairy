public class TestBasicChord {
    public static void main (String[] args){
        // Patch BaseChord 
        Patch patch = new Patch("BaseChord");

        // Création des modules
        GenSine g1 = new GenSine("g1", 139.0, 1.0); 
        GenSine g2 = new GenSine("g2", 165.0, 0.9);
        GenSine g3 = new GenSine("g3", 196.0, 0.7);
        GenSine g4 = new GenSine("g4", 233.0, 0.4);
        Mixer mix = new Mixer("mix", 4);
        AudioDataReceiver output = new AudioDataReceiver("output", 0, 0);

        // Ajout des modules au patch
        patch.addModule(g1);
        patch.addModule(g2);
        patch.addModule(g3);
        patch.addModule(g4);
        patch.addModule(mix);
        patch.addModule(output);

        // Connexion GenSine → Mixer
        patch.connect("g1", 0, "mix", 0);
        patch.connect("g2", 0, "mix", 1);
        patch.connect("g3", 0, "mix", 2);
        patch.connect("g4", 0, "mix", 3);

        // Connexion : Mixer → sortie audio
        patch.connect("mix", 0, "output", 0);

        // Durée totale du test : 3 secondes
        int totalSamples = (int)(ModuleAbstract.SAMPLE_FREQ *3);

        // Exécution du patch
        patch.exec(totalSamples);

        // Lecture audio 
        System.out.println(">> Lecture du son avec enveloppe ADSR");
        for (AudioDataReceiver recv : patch.getAudioReceivers()) {
            recv.playAudioData(); 
            recv.displayAudioDataWaveform();
        }
}
}
