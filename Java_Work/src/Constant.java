public class Constant extends ModuleAbstract {

    private final double cste;

    /**
     * Constructeur du module Constant
     * @param name Nom du module
     * @param cste Valeur constante à émettre à chaque appel
     */
    public Constant(String name, double cste) {
        super(name, 0, 1); // Aucun port d’entrée, 1 sortie
        this.cste = cste;
    }

    // Exec
    @Override
    public void exec() {
        setAndSendOutputPortValue(0, cste);
    }

    
    // Reset du module constant (ne fait rien).
    @Override
    protected void reset() {
        // Aucun état à réinitialiser
    }

    // Copie du module
    @Override
    public ModuleAbstract copier() {
        return new Constant(this.name, this.cste);
    }
}
