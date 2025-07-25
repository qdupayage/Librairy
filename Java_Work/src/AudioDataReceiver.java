import java.io.IOException;
import phelmaaudio.WavFileException;
import phelmaaudio.AudioData;

public class AudioDataReceiver extends ModuleAbstract implements ModulePlayable {
    private final AudioData audioData;

    public AudioDataReceiver(String name, int InPortNb, int OutPortNb) {
        super(name, 1, 1); // Un port d'entrée, un port de sortie
        this.audioData = new AudioData();
    }
    
    // Constructeur de copie
    public AudioDataReceiver(AudioDataReceiver other) {
        super(other); // Appelle le constructeur de copie de ModuleAbstract
        this.audioData = other.audioData;
    }

    @Override
    public void exec() {
        double sample = getInputPortValue(0); // Récupérer l'échantillon depuis l'entrée
        audioData.addSample(sample); // Ajouter l'échantillon au conteneur AudioData
        setAndSendOutputPortValue(0, sample); // Copier l'échantillon à la sortie
    }

    // Enregistre les échantillons dans un fichier WAV
    public void saveAudioDataToWavFile(String audioFileName) {
        try {
            System.out.println("Sauvegarde de l'audio dans " + audioFileName);
            audioData.saveAudioDataToWavFileNormalized(audioFileName);
        }
        catch (IOException | WavFileException e) {
            System.err.println("Erreur lors de la sauvegarde du fichier audio : " + e.getMessage());
        }
    }

    // Affiche la forme d'onde du signal
    public void displayAudioDataWaveform() {
        System.out.println("Affichage de la forme d'onde du signal");
        audioData.display();
    }

    // Joue le signal sur la carte son
    public void playAudioData() {
        System.out.println("Lecture du signal audio...");
        audioData.play();
    }

    public AudioData getAudioData() {
        return this.audioData;
    }

    @Override
    protected ModuleAbstract copier(){
        return new AudioDataReceiver(this);
    }

    @Override
    protected void setPatch(Patch p){
        super.setPatch(p);
        p.registerToPatch(this);
    }

    // Méthode pour reset
    @Override
    protected void reset() {
        // Réinitialiser les ports comme dans la classe mère
        resetPorts();
        
        // Supprimer les données audio stockées
        if (audioData != null){
            audioData.reset();
        }
    }

}
