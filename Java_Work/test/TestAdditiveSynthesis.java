public class TestAdditiveSynthesis {
    public static void main(String[] args) {
        Patch patch = new Patch("AdditiveSynthesis");

        // Def des constantes :
        double fundamentalFreq = 442.0;
        double[] harmonic = {1.0, 2.0, 3.0, 4.0};
        int nbHarm = harmonic.length;

        // Modules
        Mixer mix = new Mixer("mix", nbHarm);
        ADSREnvelop envelop = new ADSREnvelop("envelop", 0.1, 0.1, 10., 3.5, 1.0, 0.7);
        Multiplier mult = new Multiplier("mult", 2);
        AudioDataReceiver receiver = new AudioDataReceiver("Output", 0, 0);

        // Ajout des modules au patch
        patch.addModule(mix);
        patch.addModule(mult);
        patch.addModule(envelop);
        patch.addModule(receiver);

        for (int i = 1; i < nbHarm+1; i++) {
            // Fréquence = multiple de la fondamentale
            double freq = fundamentalFreq * i;

            // Module à la freq de l'harmonique
            GenSine sine = new GenSine("H" + i, freq, 1.0);
            Multiplier ampMod = new Multiplier("AmpMod"+i,1,harmonic[i-1]);

            // Ajout des modules au patch
            patch.addModule(sine);
            patch.addModule(ampMod);

            // Connexion pour exécution
            patch.connect("H" + i, 0, "AmpMod"+i, 0);
            patch.connect("AmpMod" + i, 0, "mix", i - 1);
        }

        // Mixer & Enveloppe → mult → Receiver
        patch.connect("mix", 0, "mult", 0);
        patch.connect("envelop", 0, "mult", 1);
        patch.connect("mult", 0, "Output", 0);
        
        // Exécution
        int totalSamples = (int) (ModuleAbstract.SAMPLE_FREQ * 8.0); // 8 secondes Bruit attroce mais ça fonctionne
        patch.exec(totalSamples);

        receiver.playAudioData();
        receiver.displayAudioDataWaveform();
    }
}
