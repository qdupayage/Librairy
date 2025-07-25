import java.io.IOException;

import phelmaaudio.AudioData;
import phelmaaudio.WavFileException;

public class AudioDataProvider extends ModuleAbstract implements ModulePlayable{

    private final AudioData audioData; // Conteneur des échantillons
    private int nbStep; // Compteur de pas (indice d'échantillon courant)

    /**
     * Constructeur du module AudioDataProvider.
     * @param name Nom du module.
     * @param audioData Référence vers l'objet AudioData à lire.
     */
    public AudioDataProvider(String name, AudioData audioData) {
        super(name, 0, 1); // 0 entrée, 1 sortie
        this.audioData = audioData;
        this.nbStep = 0;
    }

   
    @Override
    public void exec() {
        // Récupère l'échantillon (évite IndexOutOfBounds en renvoyant 0 si fin)
        double value = (nbStep < audioData.getNbSamples()) 
                        ? audioData.getSample(nbStep) 
                        : 0.0;
        
        setAndSendOutputPortValue(0, value);
        nbStep++;
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
    protected void reset() {
        nbStep = 0;
    }

    /**
     * Création d'une copie du module (sans dupliquer les données audio).
     */
    @Override
    public ModuleAbstract copier() {
        return new AudioDataProvider(this.name, this.audioData);
    }
}
