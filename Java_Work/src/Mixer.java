import exceptions.ModuleException;

public class Mixer extends ModuleAbstract {
    // Constructeur
    public Mixer(String name, int numInputs) {
        super(name, numInputs, 1);
    }

    @Override
    public void exec() {
        // Vérification que toutes les entrées sont disponibles
        if (inputPorts.size() == 0 || outputPorts.size() == 0) {
            throw new ModuleException("Erreur : le mixeur doit avoir au moins une entrée et une sortie !");
        }

        // Calcul du mixage : somme des entrées divisée par le nombre d'entrées
        double mixValue = 0;
        for (CommunicationPort inputPort : inputPorts) {
            mixValue += inputPort.value;
        }
        mixValue /= inputPorts.size(); // Normalisation pour éviter la saturation

        // Affecter le résultat au port de sortie
        setAndSendOutputPortValue(0, mixValue);
    }

    @Override
    public void exec(int n) {
        for (int i = 0; i < n; i++) {
            exec(); // Exécuter `exec()` pour chaque échantillon
        }
    }

    @Override
    public ModuleAbstract copier() {
        return new Mixer(this.name, inputPorts.size());
    }

    // Méthode pour reset
    @Override
    protected void reset() {
        // Réinitialiser les ports comme dans la classe mère
        resetPorts();}
}
