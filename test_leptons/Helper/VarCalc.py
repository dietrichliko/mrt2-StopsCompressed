import ROOT
from math import pi, sqrt, cos, sin, sinh, log, cosh
from ROOT import TLorentzVector
import textwrap

from Helper.CosmeticCode import vidNestedWPBitMapNamingList


def get_PU_ratio(nvtx_event):
    nvtx = [
        0.5,
        1.5,
        2.5,
        3.5,
        4.5,
        5.5,
        6.5,
        7.5,
        8.5,
        9.5,
        10.5,
        11.5,
        12.5,
        13.5,
        14.5,
        15.5,
        16.5,
        17.5,
        18.5,
        19.5,
        20.5,
        21.5,
        22.5,
        23.5,
        24.5,
        25.5,
        26.5,
        27.5,
        28.5,
        29.5,
        30.5,
        31.5,
        32.5,
        33.5,
        34.5,
        35.5,
        36.5,
        37.5,
        38.5,
        39.5,
        40.5,
        41.5,
        42.5,
        43.5,
        44.5,
        45.5,
        46.5,
        49.5,
    ]
    ratio_predividedunpre = [
        0.8683303266959563,
        1.37593636344608,
        1.7265580587850642,
        1.2809638015317606,
        1.4646757910559223,
        1.340448304219238,
        1.3665912658842108,
        1.3737253035404442,
        1.3297755633587736,
        1.2407420732540997,
        1.2421544913303268,
        1.1893485072081549,
        1.1623227392469146,
        1.1285816588710684,
        1.0837227206756426,
        1.0478683765230274,
        1.021529253582778,
        0.9830883575736463,
        0.9528349786875829,
        0.9005465534305057,
        0.882292738967126,
        0.8296311689191277,
        0.8218733449628237,
        0.7654836215067387,
        0.7596419539795178,
        0.7016574019455664,
        0.6978137346489405,
        0.685721138952357,
        0.6109357651345975,
        0.6101389825834709,
        0.6121093201052942,
        0.5657516119725,
        0.5808240788026761,
        0.6063532048910315,
        0.5481486358982481,
        0.4833242247976987,
        0.4532021997585584,
        0.5549177314841502,
        0.6849693111072471,
        0.4552480807451228,
        0.5423820872343952,
        0.3383726048768297,
        0.5269878221277862,
        0.5165268045273839,
        0.310978121123683,
        0.45788610770308297,
        0.6012243675057871,
        0.5667278874029961,
    ]
    idx = -99
    for i in range(len(nvtx) - 1):
        if nvtx_event >= nvtx[-1]:
            idx = len(nvtx) - 1
        elif nvtx_event >= nvtx[i] and nvtx_event < nvtx[i + 1]:
            idx = i
            break
        else:
            idx = -1
    return ratio_predividedunpre[idx]


def DeltaPhi(phi1, phi2):
    dphi = phi2 - phi1
    if dphi > pi:
        dphi -= 2.0 * pi
    if dphi <= -pi:
        dphi += 2.0 * pi
    return abs(dphi)


def DeltaR(eta1, phi1, eta2, phi2):
    return sqrt(DeltaPhi(phi1, phi2) ** 2 + (eta1 - eta2) ** 2)


def MinDeltaR(eta, phi, L):
    mindr = 99
    for l in L:
        dri = DeltaR(l["eta"], l["phi"], eta, phi)
        if dri < mindr:
            mindr = dri
    return mindr


def DeltaRMatched(eta, phi, L, thr):
    dr = 99
    for l in L:
        dri = DeltaR(l["eta"], l["phi"], eta, phi)
        if dri < dr:
            dr = dri
    return True if dr < thr else False


def DeltaRPtMatched(pt, eta, phi, L, thr, ptthr):
    dr = 99
    pT = 999
    for l in L:
        dri = DeltaR(l["eta"], l["phi"], eta, phi)
        if dri < dr:
            dr = dri
            pT = l["pt"]
    return True if dr < thr and abs(1 - pt / pT) < ptthr else False


def sortedlist(l, k="pt"):
    sl = sorted(l, key=lambda d: d[k], reverse=True)
    return sl


def MT(pt, phi, metpt, metphi):
    return sqrt(2 * pt * metpt * (1 - cos(phi - metphi)))


def CT1(met, HT):
    return min(met, HT - 100)


def CT2(met, ISRpt):
    return min(met, ISRpt - 25)


def AltMETCalc(MuonPt, MuonEta, MuonPhi, MuonMass, METPt, METPhi):
    Muon = TLorentzVector()
    MET = TLorentzVector()
    Muon.SetPtEtaPhiM(MuonPt, MuonEta, MuonPhi, MuonMass)
    MET.SetPtEtaPhiM(METPt, 0, METPhi, 0)
    return MET + Muon


def CIsovar(C, Pt0, Pt):
    return C * min(1, Pt / Pt0)


def GenFlagString(flag):
    s = "{0:15b}".format(flag)
    return s


"""
Comments on gen status flags:
According to the CMSSW GEN structure(), following bits are used for different status. 
So we need to check the correspoding element in the bit string returned by GenFlagString function
string index = 14-bit

"0 : isPrompt," : s[14] or s[-1] 
"1 : isDecayedLeptonHadron, "
"2 : isTauDecayProduct, "
"3 : isPromptTauDecayProduct, "
"4 : isDirectTauDecayProduct, "
"5 : isDirectPromptTauDecayProduct, "
"6 : isDirectHadronDecayProduct, "
"7 : isHardProcess, " 
"8 : fromHardProcess, " : s[6]
"9 : isHardProcessTauDecayProduct, "
"10 : isDirectHardProcessTauDecayProduct, "
"11 : fromHardProcessBeforeFSR, " : s[3]
"12 : isFirstCopy, " : s[2]
"13 : isLastCopy, "  : s[1]
"14 : isLastCopyBeforeFSR : s[0]

"""

# convert int of vidNestedWPBitMap ( e.g. val = 611099940 ) to bitmap ( e.g. "100100011011001010010100100100")
# split vidBitmap string (containing 3 bits per cut) in parts of 3 bits ( e.g. ["100","100","011","011","001","010","010","100","100","100"] )
# convert 3 bits to int ( e.g. [4, 4, 3, 3, 1, 2, 2, 4, 4, 4])


def vidNestedWPBitMapToDict(vid):
    idList = [int(x, 2) for x in textwrap.wrap("{0:030b}".format(vid), 3)]
    return dict(zip(vidNestedWPBitMapNamingList, idList))


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


def eleVID(vid, idVal, removedCuts=[]):
    vidDict = vidNestedWPBitMapToDict(vid)
    # print(f"VID: {vid:010o} : {vidDict}")
    if not removedCuts:
        return all([cut >= idVal for cut in vidDict.values()])

    if "pt" in removedCuts:
        vidDict = removekey(vidDict, "MinPtCut")
    if "sieie" in removedCuts:
        vidDict = removekey(vidDict, "GsfEleFull5x5SigmaIEtaIEtaCut")
    if "hoe" in removedCuts:
        vidDict = removekey(vidDict, "GsfEleHadronicOverEMEnergyScaledCut")
    if "pfRelIso03_all" in removedCuts:
        vidDict = removekey(vidDict, "GsfEleRelPFIsoScaledCut")
    if "SCEta" in removedCuts:
        vidDict = removekey(vidDict, "GsfEleSCEtaMultiRangeCut")
    if "dEtaSeed" in removedCuts:
        vidDict = removekey(vidDict, "GsfEleDEtaInSeedCut")
    if "dPhiInCut" in removedCuts:
        vidDict = removekey(vidDict, "GsfEleDPhiInCut")
    if "EinvMinusPinv" in removedCuts:
        vidDict = removekey(vidDict, "GsfEleEInverseMinusPInverseCut")
    if "convVeto" in removedCuts:
        vidDict = removekey(vidDict, "GsfEleConversionVetoCut")
    if "lostHits" in removedCuts:
        vidDict = removekey(vidDict, "GsfEleMissingHitsCut")

    return all([cut >= idVal for cut in vidDict.values()])


def Fill1D(h, a, w=1):
    nbin = h.GetNbinsX()
    low = h.GetBinLowEdge(nbin)
    high = h.GetBinLowEdge(nbin + 1)
    copy = a
    if copy >= high:
        copy = low
    h.Fill(copy, w)


def Fill2D(h, a, b, w=1):
    nbinx = h.GetNbinsX()
    lowx = h.GetXaxis().GetBinLowEdge(nbinx)
    highx = h.GetXaxis().GetBinLowEdge(nbinx + 1)
    copyx = a
    if copyx >= highx:
        copyx = lowx
    nbiny = h.GetNbinsY()
    lowy = h.GetYaxis().GetBinLowEdge(nbiny)
    highy = h.GetYaxis().GetBinLowEdge(nbiny + 1)
    copyy = b
    if copyy >= highy:
        copyy = lowy
    h.Fill(copyx, copyy, w)
