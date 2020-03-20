from numpy import pi
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import sys
# from matplotlib import interactive
# from matplotlib.widgets import Slider, Button, RadioButtons
# import matplotlib.ticker as ticker
# import os
# import seaborn as sns
from spinfunctions import SpinFunctions

# rmi_red = 1  # 0.8

# def sigmaEB06(U, A=A, a=a, E1=E1):
#     # cut-off parameters of EB06
#     sigma2 = np.sqrt(rmi_red) * 0.0146*A**(5./3.) * ( 1. + np.sqrt(1. + 4.*a*(U-E1)) ) / (2.*a)
#     return np.sqrt(sigma2)

# # def sigmaEB06(U, A=A, a=a, E1=E1):
# #     sig2 = (0.98*(A**(0.29)))**2
# #     return np.sqrt(sigma2)


# def sigma(U):
#     return sigmaEB06(U)


# def g(J, E=Sn):
#     # Spin distribution of Gilbert and Cameron
#     g = (2.*J+1.)/(2.*sigma(U=E)**2.) * \
#             np.exp(-(J+1./2.)**2. / (2.*(sigma(U=E))**2.))
#     return g


# def g_arr(J, E=Sn):
#     return np.array([g(j,E=E) for j in J])

def pwrite(fout, array):
    for row in array:
        head = str(int(row[0]))
        tail = " ".join(map(str, row[1:].tolist()))
        sout = head + " " +  tail + "\n"
        # print sout
        fout.write(sout)


def WriteRAINIERTotPar():
    ##############################################
    # Some test -- write files to use with RAINIER
    # print population distribution for RAINIER
    # bin    Ex    Popul.    J= 0.0    J= 1.0  [...] J=9.0
    nJs = 10
    Jstart = 0
    Js = np.array(range(nJs)) + Jstart
    nRowsOffset = 0 # cut away the first x Rows
    nRows = len(spinpar_hist)
    nCollumsExtra = 3 # 3 rows with "bin  Ex  Popul." added extra"
    nCollums = nJs + nCollumsExtra
    nStartbin = 54-nRowsOffset # ust for easy copying to RAINIER file

    # arr_JsStructure =  [(("J= " + "{0:.1f}".format(J)),"f4") for J in Js]
    # arr_structure = [('bin', 'i4'),('Ex', 'f4'), ('Popul.', 'f4')]
    # arr_structure += arr_JsStructure
    # spins_RAINIER = np.zeros((nRows,nCollums),dtype=arr_structure)

    spins_RAINIER = np.zeros((nRows,nCollums))
    # copying spinpar histogram into the historgram that shall be printed
    nRowsArrOrg = len(spinpar_hist[0]) # number of arrays in the histogram that shall be copied over
    spins_RAINIER[:,0] =  np.array(range(nRows)) + nStartbin # copy bins
    spins_RAINIER[:,1] = Ex # copy excitation energyies
    spins_RAINIER[:,2] = xs # set population to the cross-sections cal. by Greg
    spins_RAINIER[:,nCollumsExtra:] = spinpar_hist[:,:nJs-len(spinpar_hist[0])]  # copy spins
        # spins_RAINIER[:,2] = 10. # set population to 1 (assumeing all excitations energies equally populated(?))
    # spins_RAINIER[:,nCollumsExtra:] = (spins_RAINIER[:,nCollumsExtra:].transpose()*spins_RAINIER[:,2]/np.sum(spins_RAINIER[:,nCollumsExtra:],axis=1)).transpose() # normalize (per bin) to given population
    spins_array_print = spins_RAINIER[nRowsOffset:,:]

    class prettyfloat(float):
        def __repr__(self):
            return "%0.2f" % self

    # # print "\n"
    # for i in range(len(spins_RAINIER)):
    #   print  "{0:.0f}\t{1:.2f}\t{2:.2f}\t{l[0]:.4f}".format(spins_RAINIER[i,0],spins_RAINIER[i,1], spins_RAINIER[i,2], l=spins_RAINIER[i,3:])
    # #     # for pop in spins_RAINIER[i,3:]:
    # #     #   print "\t{0:.0f}".format(pop)
    # #     x = map(prettyfloat, spins_RAINIER[i,3:])
    # #     print x
    # # # for i in range(len(spins_RAINIER)):
    # # #   print  "{0:.2f}".format(spins_RAINIER[i,1])
    # print spins_RAINIER[0,:]

    arr_Js_print =  [("J= " + "{0:.1f}".format(J)) for J in Js]
    arr_header = [("bin"),("Ex"),("Popul.")]
    arr_header += arr_Js_print

    # Write spin distribution from Greg
    fout = open("Js2RAINER_Greg.txt","w")
    fout.write(" ".join(map(str, arr_header)))
    fout.write("\n")
    pwrite(fout, spins_array_print)
    fout.close()

    # #####################################
    # repeat for EB06
    # nJs = 23
    # Jstart = 0
    # Js = np.array(range(nJs)) + Jstart
    # nRowsOffset = 18 # cut away the first x Rows
    # nRows = len(spinpar_hist)
    # nCollumsExtra = 3 # 3 rows with "bin  Ex  Popul." added extra"
    # nCollums = nJs + nCollumsExtra
    # nStartbin = 54-nRowsOffset # ust for easy copying to RAINIER file

    # spins_RAINIER = np.zeros((nRows,nCollums))
    # spins_RAINIER[:,0] =  np.array(range(nRows)) + nStartbin # copy bins
    # spins_RAINIER[:,1] = Ex # copy excitation energyies
    # spins_RAINIER[:,2] = 10. # set population to 1 (assumeing all excitations energies equally populated(?))

    # # Write spin distribution from EB06
    # EB06_mat = []
    # for E in Ex:
    #     EB06_mat.append(np.array([g(i,E=E) for i in Js]))
    # EB06_mat = np.array(EB06_mat)
    # spins_RAINIER[:,nCollumsExtra:] = EB06_mat  # copy spins
    # spins_RAINIER[:,nCollumsExtra:] = (spins_RAINIER[:,nCollumsExtra:].transpose()*spins_RAINIER[:,2]/np.sum(spins_RAINIER[:,nCollumsExtra:],axis=1)).transpose() # normalize (per bin) to given population
    # spins_array_print = spins_RAINIER[nRowsOffset:,:]

    # fout = open("Js2RAINER_EB06.txt","w")
    # fout.write(" ".join(map(str, arr_header)))
    # fout.write("\n")
    # pwrite(fout, spins_array_print)
    # fout.close()

def WriteRAINIERPerPar(nJs, nStartbin, h_negPar, h_posPar, popNorm=None,
                       fname = "Js2RAINER_perParity.txt",
                       decimals=4):
    ##############################################
    # Some test -- write files to use with RAINIER
    # print population distribution for RAINIER
    # bin    Ex    Popul.    J= 0.0    J= 1.0  [...] J=9.0
    Jstart = 0
    Js = np.array(range(nJs)) + Jstart
    nRowsOffset = 0  # cut away the first x Rows
    nRows = len(h_negPar)
    nCollumsExtra = 3  # 3 rows with "bin  Ex  Popul." added extra"
    nCollums = 2*nJs + nCollumsExtra
    nStartbin = nStartbin-nRowsOffset  # ust for easy copying to RAINIER file

    bothParities = np.dstack((h_negPar, h_posPar))
    bothParities = bothParities.reshape(len(h_negPar), 2*len(h_negPar[0]))

    def FormPrintArray(matrix):
        assert(matrix.shape[1] == nJs*2), "Need to revise print function {}".format(matrix.shape)
        out = np.zeros((nRows, nCollums))
        # copying spinpar histogram into the historgram that shall be printed
        out[:, 0] = np.array(range(nRows)) + nStartbin  # copy bins
        out[:, 1] = Exs  # copy excitation energyies
        out[:, nCollumsExtra:] = \
            matrix  # copy spins
        # matrix[:, :2*nJs-len(matrix[0])]  # copy spins
        if popNorm is not None:
            out[:, 2] = popNorm  # set population to popNorm
            out[:, nCollumsExtra:] = \
                (out[:, nCollumsExtra:].transpose()
                 * out[:, 2]
                 / np.sum(out[:, nCollumsExtra:], axis=1)).transpose() # normalize (per bin) to given population
        else:
            out[:, 2] = out[:, nCollumsExtra:].sum(axis=1)
        spins_array_print = out[nRowsOffset:, :]
        out[:, nCollumsExtra:] = np.around(out[:, nCollumsExtra:], decimals=decimals)
        out[:, 1] = np.around(out[:, 1], decimals=decimals)
        print(out)
        return spins_array_print

    arrayPrint = FormPrintArray(bothParities)
    arr_Js_print = [("J= " + "-{0:.1f}".format(J) + ", J= " + "+{0:.1f}".format(J)) for J in Js]
    arr_header = [("bin"),("Ex"),("Popul.")]
    arr_header += arr_Js_print

    # Write spin distribution from Greg
    fout = open(fname, "w")
    fout.write(" ".join(map(str, arr_header)))
    fout.write("\n\n")
    pwrite(fout, arrayPrint)
    fout.close()

# WriteRAINIERPerPar(nJs=10, nStartbin=24, h_negPar=spinparNeg, h_posPar=spinparPos, popNorm=10.)
# WriteRAINIERPerPar(nJs=10, nStartbin=24, h_negPar=spinparNeg, h_posPar=spinparPos, popNorm=xs)


def g_beta_oslo1(Ex, center_spin, J):
    dist = np.zeros_like(Js, dtype=np.float)
    Jint_center = int(center_spin)
    fill_list = [Jint_center-1, Jint_center, Jint_center+1]
    for i in fill_list:
        dist[i] = 1/3.
    return dist


def cross_section(Ex, Emax):
    # triangle
    x = [0, Emax+1]
    y = [1., 0.1]
    f = interpolate.interp1d(x, y)
    return f(Ex)


if __name__ == "__main__":
    # some constants
    # 70Ni
    # Sn = 9.43
    Emax = 6.8  # Sn (Due to q value)
    Emax_xs = Emax + 1
    A = 76
    Emin = 2.624
    nStartbin = 14 # level number to Emin
    center_spin = 2 # for beta oslo decay

    # # other parameters
    Nspins = 10
    Exs = np.linspace(Emin, Emax, num=70)
    plot = False

    matrix = np.zeros((len(Exs), Nspins))
    Js = np.arange(10)
    for i, Ex in enumerate(Exs):
        matrix[i, :] = (g_beta_oslo1(Ex, center_spin=center_spin, J=Js)
                        * cross_section(Ex, Emax_xs))

    # matrix[5:8, 0:10] = 10
    # matrix = np.array(matrix)
    # print(matrix)
    # matrix = np.flipud(matrix)  # Get ascending order of Ex

    if plot is True:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.imshow(matrix, interpolation="none",
                   origin="lower", cmap='jet'
                   #extent=[xmin, xmax, ymin, ymax]
                   )
        ax.set_xlabel("Spin")
        ax.set_ylabel("Ex")
        plt.colorbar()
        plt.show()

    # NOTE: CHANGE THIS FOR POS / NEG PARITY!!!
    WriteRAINIERPerPar(nJs=10, nStartbin=nStartbin,
                       h_negPar=np.zeros_like(matrix),
                       h_posPar=matrix,
                       popNorm=None,
                       fname="Js2RAINER_perParity.txt")
    # WriteRAINIERPerPar(nJs=10, nStartbin=nStartbin,
    #                h_negPar=matrix,
    #                h_posPar=np.zeros_like(matrix),
    #                popNorm=None,
    #                fname="Js2RAINER_perParity.txt")
