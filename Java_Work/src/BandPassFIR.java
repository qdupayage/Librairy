public class BandPassFIR extends FIRAbstract {
    private static final double SAMPLEFREQ = 44100.0;

    private double fr;
    private double largeur;
    private boolean isControlledFR;
    private boolean isControlledLargeur;

    // Constructeur à 1 port d'entrée, potentiellement passer l'ordre en argument
    public BandPassFIR(String name, double fc, double largeur, int order) {
        super(name, order, 1); // 1 port d’entrée (signal seul)
        this.fr = fc;
        this.largeur = largeur;
        this.isControlledFR = false;
        this.isControlledLargeur = false;
        updateCoeffArray(fr, largeur);
    }

    // Constructeur à 2 ports d'entrée : signal + fc contrôlée
    public BandPassFIR(String name, double largeur, int order) {
        super(name, order, 2); // ports[0] = signal, ports[1] = fr
        this.largeur = largeur;
        this.isControlledFR = true;
        this.isControlledLargeur = false;
    }

    // Constructeur à 3 ports d'entrée : signal + fr + largeur contrôlés
    public BandPassFIR(String name,int order) {
        super(name, order, 3); // ports[0] = signal, ports[1] = fr, ports[2] = largeur
        this.isControlledFR = true;
        this.isControlledLargeur = true;
    }

    // Copieur
    public BandPassFIR(BandPassFIR other) {
        super(other.name, other.coeffArray.length-1, 1); // 1 port d’entrée (signal seul)
        this.fr = other.fr;
        this.largeur = other.largeur;
        this.isControlledFR = other.isControlledFR;
        this.isControlledLargeur = other.isControlledLargeur;
    }

    @Override
    public void exec() {
        if (isControlledFR) {
            fr = getInputPortValue(1);
        }
        if (isControlledLargeur) {
            largeur = getInputPortValue(2);
        }

        if (isControlledFR || isControlledLargeur) {
            updateCoeffArray(fr, largeur);
        }

        super.exec();
    }

    private void updateCoeffArray(double fr, double largeur) {
        fr = fr/SAMPLEFREQ;
        largeur = largeur/SAMPLEFREQ;

        double f_1 = fr-largeur; // freq coupure a gauche
        double f_2 = fr+largeur; // freq coupure a droite
        
        double omega_1 = 2*Math.PI*f_1;
        double omega_2 = 2*Math.PI*f_2;
        int middle = (coeffArray.length-1) / 2 ; //rappel : length impaire

        for ( int i=0 ; i< middle ; i++) {
            double val1 = Math.sin( omega_1 * (i-middle) ) / ( Math.PI * (i-middle) ) ;
            double val2 = Math.sin( omega_2 * (i-middle) ) / ( Math.PI* (i-middle) ) ;

            // hamming windowing
            double weight= 0.54- 0.46* Math.cos( ( 2. * Math.PI * i ) /coeffArray.length ) ;
            
            //weight= 1.0 ;
            coeffArray[i]= ( val2- val1 ) * weight ;
            coeffArray[coeffArray.length-i-1]= coeffArray[i] ;
            }
            coeffArray[middle]= 2.0 * ( f_2- f_1 ) ;
            
            //Scale filter to obtain an unity gain at center of passband
            double realSum= 0,imagSum= 0 ;
            for( int i = 0 ; i < coeffArray.length ; i ++ ) {
                double argExp=-2. * Math.PI * i * fr ;
                realSum+= Math.cos( argExp ) * coeffArray[i] ;
                imagSum+= Math.sin( argExp ) * coeffArray[i] ;
                }
            double sum= Math.sqrt( realSum * realSum + imagSum * imagSum ) ;
            for(int i = 0 ; i < coeffArray.length ; i ++) {
                coeffArray[i] = coeffArray[i] / sum ;
                }
    }

    public ModuleAbstract copier(){
        return new BandPassFIR(this.name, this.fr , this.largeur,this.coeffArray.length -1);
    }
}
