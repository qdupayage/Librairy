public class CommunicationPort {
    private ModuleAbstract ownerModule;
    public int portNumber;
    private Connexion connection;
    protected double value;

    // Constructeur
    public CommunicationPort(ModuleAbstract ownerModule, int portNumber) {
        this.ownerModule = ownerModule;
        this.portNumber = portNumber;
        this.connection = null; // Pas connecté à la création
        this.value = 0.0; // Valeur initiale
    }

    // Setter pour la valeur du port
    public void setValue(double v) {
        this.value = v;
    }

    // Getter pour la valeur du port
    public double getValue() {
        return this.value;
    }

    // Vérifie si le port est connecté
    public boolean isConnected() {
        return this.connection != null;
    }

    // Accesseur pour la connexion
    public Connexion getConnection() {
        return this.connection;
    }

    // Modificateur pour la connexion
    protected void setConnection(Connexion connection) {
        this.connection = connection;
    }

    // Accesseur pour le module propriétaire
    public ModuleAbstract getOwnerModule() {
        return ownerModule;
    }

    // Accesseur pour le numéro de port
    public int getPortNumber() {
        return portNumber;
    }
}
