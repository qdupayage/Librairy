package exceptions;

// Exception pour les connexions invalides entre modules
public class ConnectionException extends ModuleException {
    public ConnectionException(String message) {
        super(message);
    }
}
