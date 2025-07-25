public class TestEcho {
    public static void main (String[] args){
        // Patch BaseChord 
        Patch patch = new Patch("BaseChord");
        //AudioData audio = new AudioData("test1");

        // Création des modules
        GenSine g1 = new GenSine("g1", 139.0, 1.0); 
        GenSine g2 = new GenSine("g2", 265.0, 0.9);
        GenSine g3 = new GenSine("g3", 390.0, 0.7);
        GenSine g4 = new GenSine("g4", 505.0, 0.4);
        Mixer mix1 = new Mixer("mix1", 4);// Pour combiner les 4 sinus

        // Création de la chambre d'échos
        Delay delay = new Delay("delay", 0.15); // Delay fonctionne 
        Multiplier mult = new Multiplier("mult",1,0.45);
        Delay delay2 = new Delay("delay2", 0.3);
        Multiplier mult2 = new Multiplier("mult2",1,0.65);
        Delay delay3 = new Delay("delay3", 0.45);
        Multiplier mult3 = new Multiplier("mult3",1,0.8);
        Delay delay4 = new Delay("delay4", 0.6);
        Multiplier mult4 = new Multiplier("mult4",1,0.2);
        Delay delay5 = new Delay("delay5", 1.0);
        Multiplier mult5 = new Multiplier("mult5",1,1.2);
        Delay delay6 = new Delay("delay6", 1.15);
        Multiplier mult6 = new Multiplier("mult6",1,0.45);
        Delay delay7 = new Delay("delay7", 1.3);
        Multiplier mult7 = new Multiplier("mult7",1,0.9);
        Delay delay8 = new Delay("delay8", 1.45);
        Multiplier mult8 = new Multiplier("mult8",1,0.3);
        Delay delay9 = new Delay("delay9", 1.6);
        Multiplier mult9 = new Multiplier("mult9",1,1.0);
        Mixer mix = new Mixer("mix", 10);
        Spliter split = new Spliter("split",10);
        AudioDataReceiver output = new AudioDataReceiver("output", 0, 0);

        // Ajout des modules au patch
        patch.addModule(g1);
        patch.addModule(g2);
        patch.addModule(g3);
        patch.addModule(g4);
        patch.addModule(mix1);
        patch.addModule(delay);
        patch.addModule(delay2);
        patch.addModule(delay3);
        patch.addModule(delay4);
        patch.addModule(delay5);
        patch.addModule(delay6);
        patch.addModule(delay7);
        patch.addModule(delay8);
        patch.addModule(delay9);
        patch.addModule(mix);
        patch.addModule(split);
        patch.addModule(mult);
        patch.addModule(mult2);
        patch.addModule(mult3);
        patch.addModule(mult4);
        patch.addModule(mult5);
        patch.addModule(mult6);
        patch.addModule(mult7);
        patch.addModule(mult8);
        patch.addModule(mult9);
        patch.addModule(output);

        // Connexion pour créer le décalage l
        // Connexion GenSine → Mixer
        patch.connect("g1", 0, "mix1", 0);
        patch.connect("g2", 0, "mix1", 1);
        patch.connect("g3", 0, "mix1", 2);
        patch.connect("g4", 0, "mix1", 3);
        patch.connect("mix1", 0, "mix", 0);

        // Sortie Chambre d'échos avec gain
        patch.connect("mult", 0, "mix", 1);
        patch.connect("mult2", 0, "mix", 2);
        patch.connect("mult3", 0, "mix", 3);
        patch.connect("mult4", 0, "mix", 4);
        patch.connect("mult5", 0, "mix", 5);
        patch.connect("mult6", 0, "mix", 6);
        patch.connect("mult7", 0, "mix", 7);
        patch.connect("mult8", 0, "mix", 8);
        patch.connect("mult9", 0, "mix", 9);

        // Addition de l'échos et rentre dans le split
        patch.connect("mix", 0, "split", 0);

        // Retard de chaques échos: Chambre d'échos
        patch.connect("split", 1, "delay", 0);
        patch.connect("split", 2, "delay2", 0);
        patch.connect("split", 3, "delay3", 0);
        patch.connect("split", 4, "delay4", 0);
        patch.connect("split", 5, "delay5", 0);
        patch.connect("split", 6, "delay6", 0);
        patch.connect("split", 7, "delay7", 0);
        patch.connect("split", 8, "delay8", 0);
        patch.connect("split", 9, "delay9", 0);
        patch.connect("delay", 0, "mult", 0);
        patch.connect("delay2", 0, "mult2", 0);
        patch.connect("delay3", 0, "mult3", 0);
        patch.connect("delay4", 0, "mult4", 0);
        patch.connect("delay5", 0, "mult5", 0);
        patch.connect("delay6", 0, "mult6", 0);
        patch.connect("delay7", 0, "mult7", 0);
        patch.connect("delay8", 0, "mult8", 0);
        patch.connect("delay9", 0, "mult9", 0);

        // Connexion : Spliter → sortie audio
        patch.connect("split", 0, "output", 0);

        // Durée totale du test : 3 secondes
        int totalSamples = (int)(ModuleAbstract.SAMPLE_FREQ *3);

        // Exécution du patch
        patch.exec(totalSamples);

        // Lecture audio (à vérifier que le son évolue en attaque, decay, sustain, puis s’éteint)
        System.out.println(">> Lecture du son avec enveloppe ADSR");
        for (AudioDataReceiver recv : patch.getAudioReceivers()) {
            recv.playAudioData(); 
            recv.displayAudioDataWaveform();
        }
}
}
