import java.util.Random;

public class GenWhiteNoise extends ModuleAbstract {
    private Random rand;
    private double amplitude;

    // Constructeur
    public GenWhiteNoise(String name, double amplitude) {
        super(name, 0, 1); // Pas d’entrée, une sortie
        this.amplitude = amplitude;
        this.rand = new Random();
    }

    // Constructeur
    public GenWhiteNoise(String name) {
        this(name, 1.0);
    }

    @Override
    public void exec() {
        // Valeur aléatoire entre -1 et 1
        double noise = amplitude * (2.0 * rand.nextDouble() - 1.0);
        setAndSendOutputPortValue(0, noise);
    }

    @Override
    public void reset() {
        // Rien à réinitialiser pour un générateur de bruit blanc
    }

    @Override
    public ModuleAbstract copier(){
        return new GenWhiteNoise(this.name, this.amplitude);
    }
}
