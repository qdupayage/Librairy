public class TestDelay {
    public static void main (String[] args){
    // Patch Delay 
    Patch patch = new Patch("BaseChord");

    // Création des modules
    GenSine g1 = new GenSine("g1", 442.0, 1.0); 
    Delay delay = new Delay("delay", 1.5);
    AudioDataReceiver output = new AudioDataReceiver("output", 0, 0);

    // Ajout des modules au patch
    patch.addModule(g1);
    patch.addModule(delay);
    patch.addModule(output);

    // Connexion GenSine → Delay → Output
    patch.connect("g1", 0, "delay", 0);
    patch.connect("delay", 0, "output", 0);

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
