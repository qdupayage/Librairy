public class Spliter extends ModuleAbstract {

    // Constructeur : au moins 2 sorties
    public Spliter(String name, int numOutputs) {
        super(name, 1, numOutputs);
        if (numOutputs < 2) {
            throw new IllegalArgumentException("Un Splitter doit avoir au moins 2 sorties.");
        }
    }

    @Override
    public void exec() {
        // Lire la valeur du port d'entrée unique
        double inputValue = getInputPortValue(0);

        // Répliquer cette valeur sur tous les ports de sortie
        for (int i = 0; i < outputPorts.size(); i++) {
            setAndSendOutputPortValue(i, inputValue);
        }
    }

    @Override
    public void exec(int n) {
        for (int i = 0; i < n; i++) {
            exec();
        }
    }

    @Override
    public ModuleAbstract copier() {
        return new Spliter(this.name, outputPorts.size());
    }

    @Override
    protected void reset() {
        // Ne fait rien
    }
}
