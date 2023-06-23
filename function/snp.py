import skrf as rf
import numpy as np


def readsnp(filepath):
    my_Network = rf.Network(filepath)
    Sparameter = my_Network.s
    Frequency = my_Network.f
    Z0 = my_Network.z0

    return my_Network, Sparameter, Frequency, Z0


def S2MixedS(S, order="even_odd", port_begin=1):
    """
    S: S-parameter [f,N,N]
    order : "even_odd" or "seq",
            The default is "even-odd"
            "even_odd" mean paird even-odd
            "seq" mean  paired sequentially
    port_begin : the first port of your mixed mode network. The default = 1
    """
    port = (port_begin - 1, port_begin, port_begin + 1, port_begin + 2)
    S11 = S[:, port[0], port[0]]
    S12 = S[:, port[0], port[1]]
    S13 = S[:, port[0], port[2]]
    S14 = S[:, port[0], port[3]]

    S21 = S[:, port[1], port[0]]
    S22 = S[:, port[1], port[1]]
    S23 = S[:, port[1], port[2]]
    S24 = S[:, port[1], port[3]]

    S31 = S[:, port[2], port[0]]
    S32 = S[:, port[2], port[1]]
    S33 = S[:, port[2], port[2]]
    S34 = S[:, port[2], port[3]]

    S41 = S[:, port[3], port[0]]
    S42 = S[:, port[3], port[1]]
    S43 = S[:, port[3], port[2]]
    S44 = S[:, port[3], port[3]]
    (nb_f, col, row) = np.shape(S)

    S_mixed = np.empty((nb_f, 4, 4), dtype=np.complex64)
    Sdd = np.empty((nb_f, 2, 2), dtype=np.complex64)
    Sdc = np.empty((nb_f, 2, 2), dtype=np.complex64)
    Scd = np.empty((nb_f, 2, 2), dtype=np.complex64)
    Scc = np.empty((nb_f, 2, 2), dtype=np.complex64)
    if order == "even_odd":
        Sdd[:, 0, 0] = np.multiply(0.5, (S11 - S13 - S31 + S33)) # Sdd11
        Sdd[:, 1, 1] = np.multiply(0.5, (S22 - S24 - S42 + S44)) # Sdd22
        Sdd[:, 1, 0] = np.multiply(0.5, (S21 - S23 - S41 + S43)) # Sdd21
        Sdd[:, 0, 1] = np.multiply(0.5, (S13 - S14 - S32 + S34)) # Sdd12
        S_mixed[:, 0, 0] = Sdd[:, 0, 0]
        S_mixed[:, 1, 1] = Sdd[:, 1, 1]
        S_mixed[:, 1, 0] = Sdd[:, 1, 0]
        S_mixed[:, 0, 1] = Sdd[:, 0, 1]

        Sdc[:, 0, 0] = np.multiply(0.5, (S11 + S13 - S31 - S33)) # Sdc11
        Sdc[:, 1, 1] = np.multiply(0.5, (S22 + S24 - S42 - S44)) # Sdc22
        Sdc[:, 1, 0] = np.multiply(0.5, (S21 + S23 - S41 - S43)) # Sdc21
        Sdc[:, 0, 1] = np.multiply(0.5, (S12 + S14 - S32 - S34)) # Sdc12
        S_mixed[:, 0, 2] = Sdc[:, 0, 0]
        S_mixed[:, 1, 3] = Sdc[:, 1, 1]
        S_mixed[:, 1, 2] = Sdc[:, 1, 0]
        S_mixed[:, 0, 3] = Sdc[:, 0, 1]

        Scd[:, 0, 0] = np.multiply(0.5, (S11 - S13 + S31 - S33)) # Scd11
        Scd[:, 1, 1] = np.multiply(0.5, (S22 - S24 + S42 - S44)) # Scd22
        Scd[:, 1, 0] = np.multiply(0.5, (S21 - S23 + S41 - S43)) # Scd21
        Scd[:, 0, 1] = np.multiply(0.5, (S12 - S14 + S32 - S34)) # Scd12
        S_mixed[:, 2, 0] = Scd[:, 0, 0]
        S_mixed[:, 3, 1] = Scd[:, 1, 1]
        S_mixed[:, 3, 0] = Scd[:, 1, 0]
        S_mixed[:, 2, 1] = Scd[:, 0, 1]

        Scc[:, 0, 0] = np.multiply(0.5, (S11 + S13 + S31 + S33)) # Scc11
        Scc[:, 1, 1] = np.multiply(0.5, (S22 + S24 + S42 + S44)) # Scc22
        Scc[:, 1, 0] = np.multiply(0.5, (S21 + S23 + S41 + S43)) # Scc21
        Scc[:, 0, 1] = np.multiply(0.5, (S12 + S14 + S32 + S34)) # Scc12
        S_mixed[:, 2, 2] = Scc[:, 0, 0]
        S_mixed[:, 3, 3] = Scc[:, 1, 1]
        S_mixed[:, 3, 2] = Scc[:, 1, 0]
        S_mixed[:, 2, 3] = Scc[:, 0, 1]

        return S_mixed, Sdd, Sdc, Scd, Scc
    # ---------------end of even_odd------------------
    elif order == "seq" : 
        Sdd[:, 0, 0] = np.multiply(0.5, (S11 - S12 - S21 + S22)) # Sdd11
        Sdd[:, 1, 1] = np.multiply(0.5, (S33 - S34 - S43 + S44)) # Sdd22
        Sdd[:, 1, 0] = np.multiply(0.5, (S31 - S32 - S41 + S42)) # Sdd21
        Sdd[:, 0, 1] = np.multiply(0.5, (S12 - S14 - S23 + S24)) # Sdd12
        S_mixed[:, 0, 0] = Sdd[:, 0, 0]
        S_mixed[:, 1, 1] = Sdd[:, 1, 1]
        S_mixed[:, 1, 0] = Sdd[:, 1, 0]
        S_mixed[:, 0, 1] = Sdd[:, 0, 1]

        Sdc[:, 0, 0] = np.multiply(0.5, (S11 + S12 - S21 - S22)) # Sdc11
        Sdc[:, 1, 1] = np.multiply(0.5, (S33 + S34 - S43 - S44)) # Sdc22
        Sdc[:, 1, 0] = np.multiply(0.5, (S31 + S32 - S41 - S42)) # Sdc21
        Sdc[:, 0, 1] = np.multiply(0.5, (S12 + S14 - S23 - S24)) # Sdc12
        S_mixed[:, 0, 2] = Sdc[:, 0, 0]
        S_mixed[:, 1, 3] = Sdc[:, 1, 1]
        S_mixed[:, 1, 2] = Sdc[:, 1, 0]
        S_mixed[:, 0, 3] = Sdc[:, 0, 1]

        Scd[:, 0, 0] = np.multiply(0.5, (S11 - S12 + S21 - S22)) # Scd11
        Scd[:, 1, 1] = np.multiply(0.5, (S33 - S34 + S43 - S44)) # Scd22
        Scd[:, 1, 0] = np.multiply(0.5, (S31 - S32 + S41 - S42)) # Scd21
        Scd[:, 0, 1] = np.multiply(0.5, (S12 - S14 + S23 - S24)) # Scd12
        S_mixed[:, 2, 0] = Scd[:, 0, 0]
        S_mixed[:, 3, 1] = Scd[:, 1, 1]
        S_mixed[:, 3, 0] = Scd[:, 1, 0]
        S_mixed[:, 2, 1] = Scd[:, 0, 1]

        Scc[:, 0, 0] = np.multiply(0.5, (S11 + S12 + S21 + S22)) # Scc11
        Scc[:, 1, 1] = np.multiply(0.5, (S33 + S34 + S43 + S44)) # Scc22
        Scc[:, 1, 0] = np.multiply(0.5, (S31 + S32 + S41 + S42)) # Scc21
        Scc[:, 0, 1] = np.multiply(0.5, (S12 + S14 + S23 + S24)) # Scc12
        S_mixed[:, 2, 2] = Scc[:, 0, 0]
        S_mixed[:, 3, 3] = Scc[:, 1, 1]
        S_mixed[:, 3, 2] = Scc[:, 1, 0]
        S_mixed[:, 2, 3] = Scc[:, 0, 1]

        return S_mixed, Sdd, Sdc, Scd, Scc
    else:
        print("order must be even_odd or seq")
        return None






if __name__ == "__main__":
    print("test")
