package exceptions;

// Exception générale pour les erreurs liées aux modules
public class ModuleException extends RuntimeException {
    public ModuleException(String message) {
        super(message);
    }

}
