import exceptions.ConnectionException;

public class Connexion {
    private CommunicationPort upModulePort;
    private CommunicationPort downModulePort;

    // Constructeur
    protected Connexion(CommunicationPort UMP, CommunicationPort DMP){
        if(UMP != null && DMP != null) {
            this.upModulePort = UMP;
            this.downModulePort = DMP;
        }
        else{
            throw new ConnectionException("la connexion n'a pas pu être faite :" + UMP + DMP);
        }
    }

    // Méthode pour transmettre la valeur de upModulePort vers downModulePort
    public void communicate() {
        if (upModulePort != null && downModulePort != null) {
            downModulePort.setValue(upModulePort.getValue());
        }
    }

    // Accesseur pour le port en amont
    public CommunicationPort getUpModulePort() {
        return upModulePort;
    }

    // Accesseur pour le port en aval
    public CommunicationPort getDownModulePort() {
        return downModulePort;
    }
}
