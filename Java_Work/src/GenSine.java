public class GenSine extends ModuleAbstract {

    private double phase = 0.0;         // Phase du signal sinus
    private double fixedFreq = 0.0;     // Fréquence fixe (si utilisée)
    private double fixedAmp = 0.0;      // Amplitude fixe (si utilisée)

    // ========== Constructeur 1 : fréquence et amplitude fixées ==========
    public GenSine(String name, double f, double amp) {
        super(name, 0, 1); // 0 entrée, 1 sortie
        this.fixedFreq = f;
        this.fixedAmp = amp;
    }

    // ========== Constructeur 2 : amplitude fixe, fréquence variable ==========
    public GenSine(String name, double amp) {
        super(name, 1, 1); // 1 entrée (freq), 1 sortie
        this.fixedAmp = amp;
    }

    // ========== Constructeur 3 : amplitude et fréquence variables ==========
    public GenSine(String name) {
        super(name, 2, 1); // 2 entrées (freq et amp), 1 sortie
    }

    // Constructeur de copie
    public GenSine(GenSine other) {
        super(other); // Appelle le constructeur de copie de ModuleAbstract
        this.phase = other.phase;
        this.fixedFreq = other.fixedFreq;
        this.fixedAmp = other.fixedAmp;
    }

    @Override
    public void exec() {
        double freq;
        double amp;

        // === Lecture des paramètres dynamiques ou utilisation des valeurs fixes ===
        if (getNbInputPorts() == 2) {
            freq = inputPorts.get(0).getValue();
            amp = inputPorts.get(1).getValue();
        } else if (getNbInputPorts() == 1) {
            freq = inputPorts.get(0).getValue();
            amp = fixedAmp;
        } else {
            freq = fixedFreq;
            amp = fixedAmp;
        }

        // === Mise à jour de la phase ===
        phase += 2 * Math.PI * freq / SAMPLE_FREQ;

        // === Calcul du signal sinus ===
        double e = amp * Math.sin(phase);

        // === Écriture sur le port de sortie ===
        setAndSendOutputPortValue(0, e);
    }

    @Override
    protected ModuleAbstract copier() {
        return new GenSine(this);
    }

    @Override
    public void reset() {
        this.phase = 0.0;

        // === Lecture des paramètres dynamiques ou utilisation des valeurs fixes ===
        if (getNbInputPorts() == 0) {
            this.fixedFreq = 0.0;
            this.fixedAmp = 0.0;
        } else if (getNbInputPorts() == 1) {
            inputPorts.get(0).setValue(0.0);
            this.fixedAmp = 0.0;
        } else {
            inputPorts.get(0).setValue(0.0);
            inputPorts.get(1).setValue(0.0);
        }
    }
}
