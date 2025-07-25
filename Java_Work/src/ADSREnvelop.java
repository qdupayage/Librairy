public class ADSREnvelop extends ModuleAbstract {
    private double attackDuration;
    private double decayDuration;
    private double sustainDuration;
    private double releaseDuration;

    private double attackLevel;
    private double sustainLevel;

    private int sampleId = 0;

    // Premier constructeur : paramètres complets
    public ADSREnvelop(String name, double attackDuration, double decayDuration,
                       double sustainDuration, double releaseDuration,
                       double attackLevel, double sustainLevel) {
        super(name, 0, 1); // Aucun port d'entrée, un port de sortie
        this.attackDuration = attackDuration;
        this.decayDuration = decayDuration;
        this.sustainDuration = sustainDuration;
        this.releaseDuration = releaseDuration;
        this.attackLevel = attackLevel;
        this.sustainLevel = sustainLevel;
    }

    // Second constructeur : noteDuration avec phases par défaut
    public ADSREnvelop(String name, double noteDuration) {
        super(name, 0, 1);
        if (noteDuration < 0.1 + 0.05) {
            throw new IllegalArgumentException("noteDuration doit être ≥ 0.15s");
        }

        this.attackDuration = 0.1;
        this.decayDuration = 0.05;
        this.releaseDuration = 0.5;
        this.sustainDuration = noteDuration - (attackDuration + decayDuration + releaseDuration);

        this.attackLevel = 1.0;
        this.sustainLevel = 0.7;
    }

    // Copieur
    public ADSREnvelop(ADSREnvelop other){
        super(other);
        this.attackDuration = other.attackDuration;
        this.decayDuration = other.decayDuration;
        this.sustainDuration = other.sustainDuration;
        this.releaseDuration = other.releaseDuration;
        this.attackLevel = other.attackLevel;
        this.sustainLevel = other.sustainLevel;
    }

    @Override
    public void exec() {
        double timeSec = (double) sampleId / SAMPLE_FREQ;

        if (timeSec >= attackDuration + decayDuration + sustainDuration + releaseDuration) {
            setAndSendOutputPortValue(0, 0.0);
            return;
        }

        double y1, y0, x0, x1;
        if (timeSec < attackDuration) {
            // Attack phase
            x0 = 0;
            y0 = 0;
            x1 = attackDuration;
            y1 = attackLevel;
        } else if (timeSec < attackDuration + decayDuration) {
            // Decay phase
            x0 = attackDuration;
            y0 = attackLevel;
            x1 = attackDuration + decayDuration;
            y1 = sustainLevel;
        } else if (timeSec < attackDuration + decayDuration + sustainDuration) {
            // Sustain phase
            x0 = attackDuration + decayDuration;
            y0 = sustainLevel;
            x1 = x0 + sustainDuration;
            y1 = sustainLevel;
        } else {
            // Release phase
            x0 = attackDuration + decayDuration + sustainDuration;
            y0 = sustainLevel;
            x1 = x0 + releaseDuration;
            y1 = 0;
        }

        double output = ((y1 - y0) / (x1 - x0)) * (timeSec - x0) + y0;
        setAndSendOutputPortValue(0, output);
        sampleId++;
    }

    @Override
    protected ModuleAbstract copier() {
        return new ADSREnvelop(this);
    }

    @Override
    public void reset() {
        sampleId = 0;
        resetPorts(); // Réinitialise les ports d'entrée et de sortie à 0
    }
}
