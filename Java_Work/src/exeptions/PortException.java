package exceptions;

// Exception générale pour les erreurs liées aux modules
public class PortException extends RuntimeException {
    public PortException(String message) {
        super(message);
    }
}
