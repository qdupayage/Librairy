package exceptions;

// Exception pour les erreurs dans le Patch
public class PatchException extends RuntimeException {
    public PatchException(String message) {
        super(message);
    }
}
