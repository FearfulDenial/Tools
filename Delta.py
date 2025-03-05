import logging
import numpy as np

HumanReadable = False
logging.basicConfig(
    filename="UpsilonRho.log",
    level=logging.INFO,
    format="%(message)s",
)

def Round(Zeta, Delta=3):
    Rho = complex(round(Zeta.real, Delta), round(Zeta.imag, Delta))
    return Rho

def Describe(Zeta):
    Mag,Ang = abs(Zeta),np.angle(Zeta, deg=True)
    MagDesc,AngDesc = "Unknown","Unknown"
    if Mag > 0.9: 
        MagDesc = "HIGH"
    elif Mag > 0.5:
        MagDesc = "MED"
    else:
        MagDesc = "LOW"

    if -15 <= Ang <= 15 or 165 <= Ang <= 195:
        AngDesc = "MR"
    elif 75 <= Ang <= 105 or -105 <= Ang <= -75:
        AngDesc = "MI"
    else:
        AngDesc = "UNK"

    return f"[{MagDesc}:{AngDesc} | {round(Mag,3)}@{round(Ang,1)}°]"

if __name__ == "__main__":
    try:
        while True:
            Sigma = int(input(""))
            Mu = np.random.uniform(-1, 1, (Sigma, Sigma)) + 1j * np.random.uniform(-1, 1, (Sigma, Sigma))

            Beta = np.linalg.norm(Mu, axis=0)
            UpsilonMu = Mu / Beta
            UpsilonTheta = np.conj(UpsilonMu.T)
            IotaChar = np.dot(UpsilonTheta, UpsilonMu)

            for Nu, Upsilon in [("Μ9", UpsilonMu), ("Θ9", UpsilonTheta), ("Ι9", IotaChar)]:
                Omega = f"\nUnitary {Nu}"
                logging.info(Omega)
                print(Omega)

                for Rho in Upsilon:
                    Alpha = [Round(Zeta) for Zeta in Rho]
                    if HumanReadable:
                        Epsilon = " | ".join(Describe(Zeta) for Zeta in Alpha)
                    else:
                        Epsilon = " ".join(f"({Zeta.real}{'+' if Zeta.imag >= 0 else ''}{Zeta.imag}j)" for Zeta in Alpha)
                    logging.info(Epsilon)
                    print(Epsilon)
    except KeyboardInterrupt:
        logging.info("Interrupted by user.")
        pass