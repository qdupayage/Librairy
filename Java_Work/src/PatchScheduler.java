import java.util.List;
import java.util.ArrayList;

public class PatchScheduler {
    private class ScheduledPatch {
        Patch patch;
        double duration; // en secondes

        public ScheduledPatch(Patch patch, double duration) {
            this.patch = patch;
            this.duration = duration;
        }
    }

    private List<ScheduledPatch> patchList = new ArrayList<>();

    public void schedulePatch(Patch patchTemplate, double durationSeconds) {
        Patch newPatch = new Patch(patchTemplate); // deep copy
        patchList.add(new ScheduledPatch(newPatch, durationSeconds));
    }

    public void runAllPatchesSequentially() {
        while (!patchList.isEmpty()) {
            ScheduledPatch current = patchList.remove(0); // on prend le premier
            int totalSamples = (int) (ModuleAbstract.SAMPLE_FREQ * current.duration);

            current.patch.exec(totalSamples);

            for( AudioDataReceiver ADR :current.patch.getAudioReceivers()){
                ADR.playAudioData();
            }
            try {
                Thread.sleep((long)(current.duration * 1000)); // Attendre la durée réelle
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
