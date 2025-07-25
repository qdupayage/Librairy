public class Delay extends ModuleAbstract {
    private final double[] circularBuffer;
    private int head;

    // Constructeur avec délai en secondes
    public Delay(String name, double delayInSeconds) {
        super(name, 1, 1); // 1 entrée, 1 sortie
        int bufferSize = (int) Math.ceil(delayInSeconds * SAMPLE_FREQ);
        if (bufferSize < 1) {
            throw new IllegalArgumentException("Le délai doit correspondre à au moins 1 échantillon.");
        }
        this.circularBuffer = new double[bufferSize];
        this.head = 0;
    }

    @Override
    public void exec() {
        // 1. Stocker l’échantillon d’entrée dans le buffer
        circularBuffer[head] = getInputPortValue(0);

        // 2. Calculer l’index de lecture (échantillon retardé)
        int readIndex = (head + 1) % circularBuffer.length;
        double outputSample = circularBuffer[readIndex];

        // 3. Envoyer l’échantillon de sortie
        setAndSendOutputPortValue(0, outputSample);

        // 4. Avancer le pointeur de tête
        head = (head + 1) % circularBuffer.length;
    }

    @Override
    public void exec(int n) {
        for (int i = 0; i < n; i++) {
            exec();
        }
    }

    @Override
    public ModuleAbstract copier() {
        // Copie sans historique du buffer
        return new Delay(this.name, (double) circularBuffer.length / SAMPLE_FREQ);
    }

    @Override
    protected void reset() {
        head = 0;
        for (int i = 0; i < circularBuffer.length; i++) {
            circularBuffer[i] = 0.0;
        }
    }
}
