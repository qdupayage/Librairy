import java.util.ArrayList;
import java.util.List;

import exceptions.PatchException;
//import exceptions.ConnectionException;
import exceptions.PortException;
import phelmaaudio.AudioData;


public abstract class ModuleAbstract {
    protected List<CommunicationPort> inputPorts;
    protected List<CommunicationPort> outputPorts;
    protected final String name;
    protected Patch patch;
    private List<ModulePlayable> playableModules = new ArrayList<>();
    public static final double SAMPLE_FREQ = 44100.0;

    // Constructeur
    public ModuleAbstract(String name, int numInputPorts, int numOutputPorts) {
        this.name = name;
        this.inputPorts = new ArrayList<>(numInputPorts);
        this.outputPorts = new ArrayList<>(numOutputPorts);
        this.patch = null;

        for (int i = 0; i < numInputPorts; i++) {
            inputPorts.add(new CommunicationPort(this, i));
        }
        for (int i = 0; i < numOutputPorts; i++) {
            outputPorts.add(new CommunicationPort(this, i));
        }
    }

    // Constructeur de copie
    protected ModuleAbstract(ModuleAbstract other) {
        this.name = other.name + "_copy"; // Pour différencier la copie
        this.patch = null; // La copie n'appartient à aucun patch
        this.inputPorts = new ArrayList<>(other.inputPorts.size());
        this.outputPorts = new ArrayList<>(other.outputPorts.size());

        for (int i = 0; i < other.inputPorts.size(); i++) {
            CommunicationPort newPort = new CommunicationPort(this, i);
            newPort.value = other.getInputPortValue(i);
            inputPorts.add(newPort); // Ports sans connexion
        }
        for (int i = 0; i < other.outputPorts.size(); i++) {
            CommunicationPort newPort =new CommunicationPort(this, i);
            newPort.value = other.getOutputPortValue(i);
            outputPorts.add(newPort);
        }

        //reset(); // Appel de reset()
    }

    protected abstract ModuleAbstract copier ();


    // Accesseur pour le nom du module
    public String getName() {
        return name;
    }

    // Accesseurs pour récupérer un port d'entrée, peut être mis en private aussi
    public CommunicationPort getInputPort(int index) {
        if (index >= 0 && index < inputPorts.size() && inputPorts.get(index) != null) {
            return inputPorts.get(index);
        }
        throw new PortException("InputPorts n'existe pas " + index);
    }

    // Accesseurs pour récupérer un port de sortie, peut être mis en private aussi
    public CommunicationPort getOutputPort(int index) {
        if (index >= 0 && index < outputPorts.size() && outputPorts.get(index) != null) {
            return outputPorts.get(index);
        }
        throw new PortException("OutputPorts n'existe pas: " + index);
    }

    // Méthode pour récupérer les modules jouables
    protected List<ModulePlayable> getPlayableModules() {
        return playableModules;
    }

    // Méthode pour afficher toutes les formes d'onde audio
    public void displayAudioDatas() {
        List<AudioData> audioDataList = new ArrayList<>();
        if (this.patch != null){
            Patch patch = this.patch;
            for (ModulePlayable module : patch.playableModules) {
                audioDataList.add(module.getAudioData());
            }}
        AudioData.displayMultipleAudioData(audioDataList);
    }

    // Méthode statique pour connecter deux modules, doit être mis en public obligatoirement
    public static Connexion connect(ModuleAbstract mOutput, int idOutputPort, ModuleAbstract mInput, int idInputPort) {
        if (idOutputPort >= mOutput.outputPorts.size() || idOutputPort <0){
            throw new PortException("Ce port de sortie n'est pas valide: "+ idOutputPort);
        }
        if (idInputPort >= mInput.inputPorts.size() || idInputPort <0){
            throw new PortException("Ce port d'entrée n'est pas valide: "+ idInputPort);
        }
        CommunicationPort outputPort = mOutput.getOutputPort(idOutputPort);
        CommunicationPort inputPort = mInput.getInputPort(idInputPort);
        
        Connexion connection = new Connexion(outputPort, inputPort);
        outputPort.setConnection(connection);
        inputPort.setConnection(connection);
        
        return connection;
    }

    // Méthode pour définir et envoyer une valeur sur un port de sortie, en protected pour éviter des intéractions avec d'autres class
    protected void setAndSendOutputPortValue(int idOutputPort, double sample) {
        if (this.outputPorts.size() < idOutputPort){
            throw new PortException("ce port n'est pas dans la liste des ports de sortie de ce module" + idOutputPort);
        }
        CommunicationPort outputPort = getOutputPort(idOutputPort);
        outputPort.setValue(sample);
        if (outputPort.isConnected()) {
            outputPort.getConnection().communicate();
        }
    }

    // Méthode pour récupérer la valeur d'un port d'entrée
    protected double getInputPortValue(int idInputPort) {
        if (this.inputPorts.size() < idInputPort){
            throw new PortException("ce port n'est pas dans la liste des ports d'entrées de ce module" + idInputPort);
        }
        return getInputPort(idInputPort).getValue();
    }

    // Méthode pour récupérer la valeur d'un port d'entrée
    protected double getOutputPortValue(int idOutputPort) {
        if (this.outputPorts.size() < idOutputPort){
            throw new PortException("ce port n'est pas dans la liste des ports de sorties de ce module" + idOutputPort);
        }
        return getOutputPort(idOutputPort).getValue();
    }

    // Méthode pour modifier la valeur d'un port d'entrée
    protected void setInputPortValue(int idInputPort, double value) {
        if (this.inputPorts.size() < idInputPort){
            throw new PortException("ce port n'est pas dans la liste des ports d'entrées de ce module" + idInputPort);
        }
        getInputPort(idInputPort).setValue(value);
    }

    // Méthode abstraite pour reset un module
    protected abstract void reset();

    // Méthode pour reset un module
    protected void resetPorts(){
        for (int i = 0; i < this.inputPorts.size(); i++) {
            inputPorts.get(i).setValue(0.0);
        }
        for (int i = 0; i < this.outputPorts.size(); i++) {
            outputPorts.get(i).setValue(0.0);
        }
    } 


    // Méthode pour avoir le nombre de ports d'entrée
    public int getNbInputPorts(){
        return inputPorts.size();
    }

    // Méthode pour avoir le nombre de ports de sortie
    public int getNbOutputPorts(){
        return outputPorts.size();
    }

    // Méthode pour attribuer un patch au module
    protected void setPatch (Patch p){
        if (this.patch != null){
            throw new PatchException("Ce module est déjà relié à un patch");
        }
        this.patch = p;
    }

    // Méthode pour vérifier si le module est lié à un patch
    public boolean isInPatch(){
        if (this.patch != null){
            return true;
        }
        return false;
    }

    // Méthode pour savoir si le port est connecté
    public boolean isConnectedInputPort(int inputPortId){
        if (this.inputPorts.size() < inputPortId){
            throw new PortException("ce port n'est pas dans la liste des ports d'entrées de ce module" + inputPortId);
        }
        return inputPorts.get(inputPortId).isConnected();
    }

    // Méthode pour savoir si le port est connecté
    public boolean isConnectedOutputPort(int outputPortId){
        if (this.outputPorts.size() < outputPortId){
            throw new PortException("ce port n'est pas dans la liste des ports de sortie de ce module" + outputPortId);
        }
        return outputPorts.get(outputPortId).isConnected();
    }

    // Méthode qui renvoie la liste des ports d'entrées non connectés
    protected List<CommunicationPort> getUnconnectedInputPorts() {
        List<CommunicationPort> unconnectedPorts = new ArrayList<>(); // Créer une liste vide
    
        for (CommunicationPort port : inputPorts) { // Parcourir tous les ports d'entrée
            if (!port.isConnected()) { // Si le port N'EST PAS connecté
                unconnectedPorts.add(port); // L'ajouter à la liste
            }
        }
        
        return unconnectedPorts; // Retourner la liste des ports non connectés
    }

    // Méthode qui renvoie la liste des ports de sorties non connectés
    protected List<CommunicationPort> getUnconnectedOutputPorts() {
        List<CommunicationPort> unconnectedPorts = new ArrayList<>(); // Créer une liste vide
    
        for (CommunicationPort port : outputPorts) { // Parcourir tous les ports d'entrée
            if (!port.isConnected()) { // Si le port N'EST PAS connecté
                unconnectedPorts.add(port); // L'ajouter à la liste
            }
        }
        
        return unconnectedPorts; // Retourner la liste des ports non connectés
    }

    // Méthode d'exécution du module ?
    protected abstract void exec();

    // Méthode d'éxécution de nbStep modules
    public void exec(int nbStep) {
        for (int i = 0; i < nbStep; i++) {
            exec();
        }
    }
}