public abstract class FIRAbstract extends ModuleAbstract {
    protected double[] coeffArray;
    private double[] inputSamples;
    private int pointer;

    public FIRAbstract(String name, int order, int nbInputs) {
        super(name, nbInputs, 1);
        if (order % 2 != 0) {
            throw new IllegalArgumentException("L'ordre N doit être pair.");
        }
        coeffArray = new double[order + 1];
        inputSamples = new double[order + 1];
        pointer = 0;
    }

    @Override
    public void reset() {
        for (int i = 0; i < inputSamples.length; i++) {
            inputSamples[i] = 0.0;
        }
    }

    @Override
    public void exec() {
        double input = getInputPortValue(0);
        inputSamples[pointer] = input;

        double output = 0.0;
        int index = pointer;

        for (int i = 0; i < coeffArray.length; i++) {
            output += coeffArray[i] * inputSamples[index];
            index = (index - 1 + inputSamples.length) % inputSamples.length;
        }

        pointer = (pointer + 1) % inputSamples.length;

        setAndSendOutputPortValue(0, output);
    }
}
