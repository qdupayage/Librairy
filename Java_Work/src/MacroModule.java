import java.util.ArrayList;
import java.util.List;

public class MacroModule extends ModuleAbstract {
    protected Patch patchInterne;
    protected List<CommunicationPort> unconnectedInputPorts;
    protected List<CommunicationPort> unconnectedOutputPorts;

    public MacroModule(String name, Patch p) {
        // Appel du constructeur de la classe mère
        super(name, p.getUnconnectedInputPorts().size() ,p.getUnconnectedOutputPorts().size() );

        // Définition des attributs de la classe
        this.unconnectedInputPorts = p.getUnconnectedInputPorts();
        this.unconnectedOutputPorts = p.getUnconnectedOutputPorts();
        this.patchInterne = new Patch(p);

        // Initialiser les ports d'entrée/sortie du MacroModule
        this.inputPorts = new ArrayList<>(this.unconnectedInputPorts);
        this.outputPorts = new ArrayList<>(this.unconnectedOutputPorts);
    }

    public MacroModule (MacroModule other){
        super(other);
        this.patchInterne = other.patchInterne;
        this.unconnectedInputPorts = other.unconnectedInputPorts;
        this.unconnectedOutputPorts = other.unconnectedOutputPorts;
    }

    @Override
    public void exec() {
        // Copier les échantillons d'entrée dans les ports internes non connectés
        for (int i = 0; i < unconnectedInputPorts.size(); i++) {
            unconnectedInputPorts.get(i).value = this.inputPorts.get(i).value;
        }

        // Exécuter le patch interne
        patchInterne.exec();

        // Copier les résultats dans les ports de sortie du MacroModule
        for (int i = 0; i < unconnectedOutputPorts.size(); i++) {
            this.outputPorts.get(i).value = unconnectedOutputPorts.get(i).value;
        }
    }

    @Override
    public void exec(int n) {
        // Copier les échantillons d'entrée dans les ports internes non connectés
        for (int i = 0; i < unconnectedInputPorts.size(); i++) {
            unconnectedInputPorts.get(i).value = this.inputPorts.get(i).value;
        }

        // Exécuter le patch interne
        patchInterne.exec(n);

        // Copier les résultats dans les ports de sortie du MacroModule
        for (int i = 0; i < unconnectedOutputPorts.size(); i++) {
            this.outputPorts.get(i).value = unconnectedOutputPorts.get(i).value;
        }       
    }

    @Override
    public ModuleAbstract copier(){
        return new MacroModule(this);
    }
    
    @Override
    public void reset() {
        patchInterne.reset();
    }
}
