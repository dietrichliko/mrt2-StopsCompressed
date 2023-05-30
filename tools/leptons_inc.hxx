#ifndef LEPTONS_INC_HXX
#define LEPTONS_INC_HXX

#include "ROOT/RVec.hxx"
#include <algorithm>
#include <cmath>

ROOT::RVecB ECalGap(const ROOT::RVecF &eta, const ROOT::RVecF &deltaEtaSC)
{
    return abs(eta + deltaEtaSC) < 1.4442 || abs(eta + deltaEtaSC) > 1.566;
};

namespace ElectronVid
{
    const unsigned long GsfEleMissingHitsCut = 07000000000;
    const unsigned long GsfEleConversionVetoCut = 00700000000;
    const unsigned long GsfEleRelPFIsoScaledCut = 00070000000;
    const unsigned long GsfEleEInverseMinusPInverseCut = 00007000000;
    const unsigned long GsfEleHadronicOverEMEnergyScaledCut = 00000700000;
    const unsigned long GsfEleFull5x5SigmaIEtaIEtaCut = 00000070000;
    const unsigned long GsfEleDPhiInCut = 00000007000;
    const unsigned long GsfEleDEtaInSeedCut = 00000000700;
    const unsigned long GsfEleSCEtaMultiRangeCut = 00000000070;
    const unsigned long MinPtCut = 00000000007;

    ROOT::RVecB Eval(const ROOT::RVecU &vid, int level, unsigned int mask = 0)
    {
        ROOT::RVecB result;
        result.reserve(vid.size());

        auto vid1 = vid | mask;
        std::transform(
            vid1.begin(),
            vid1.end(),
            std::back_inserter(result),
            [level](unsigned int v)
            {
                unsigned int v1 = v;
                bool flag = true;
                for (unsigned int i = 0; i < 10; ++i)
                {
                    flag &= (v & 07) >= level;
                    v >>= 3;
                }
                return flag;
            });
        return result;
    };
};

float square(float x) { return x * x; };

ROOT::RVecB HybridIso(const ROOT::RVecF &pt, ROOT::RVecF &iso, float f1 = 5.0, float f2 = 0.2, bool miniIsolation = false)
{
    ROOT::RVecB result;
    result.reserve(iso.size());

    std::transform(
        iso.begin(),
        iso.end(),
        pt.begin(),
        std::back_inserter(result),
        [f1, f2, miniIsolation](float iso, float pt)
        {
            float isolationWeight = 1.;
            if (miniIsolation)
            {
                if (pt < 50.)
                {
                    isolationWeight = 0.42942652;
                }
                else if (pt < 200.)
                {
                    isolationWeight = square(tan(10.0 / pt) / tan(0.3));
                }
                else
                {
                    isolationWeight = 0.02616993;
                }
            }
            if (pt <= 25.)
            {
                return (iso * pt) < f1 * isolationWeight;
            }
            else
            {
                return iso < f2 * isolationWeight;
            }
        });
    return result;
}

ROOT::RVecI ElectronMerge(const ROOT::RVecF &eta1, const ROOT::RVecF &phi1, const ROOT::RVecF &eta2, const ROOT::RVecF &phi2)
{
    unsigned int n1 = eta1.size();
    unsigned int n2 = eta2.size();
    std::vector<bool> ok2(n2, true);
    for (unsigned int i2 = 0; i2 < n2; ++i2)
    {
        for (unsigned int i1 = 0; i1 < n1; ++i1)
        {
            float dphi = phi1[i1] - phi2[i2];
            if (abs(dphi) > M_PI)
            {
                dphi -= std::copysign(2 * M_PI, dphi);
            }
            float deta = eta1[i1] - eta2[i2];
            float sqr_dr = dphi * dphi + deta * deta;
            if (sqr_dr < 0.1 * 0.1)
            {
                ok2[i2] = false;
                break;
            }
        }
    }
    ROOT::RVecI idx;
    idx.reserve(n1 + n2);
    for (unsigned i1 = 0; i1 < n1; ++i1)
    {
        idx.emplace_back(i1);
    }
    for (unsigned i2 = 0; i2 < n2; ++i2)
    {
        if (ok2[i2])
        {
            idx.emplace_back(i2 ^ 0xFFFFFFFF);
        }
    }
    return idx;
}

ROOT::RVecI LeptonMerge(const ROOT::RVecF &pt1, const ROOT::RVecF &pt2)
{
    unsigned int l1 = pt1.size();
    unsigned int l2 = pt2.size();
    ROOT::RVecI idx;
    idx.reserve(l1 + l2);

    unsigned int i1 = 0;
    unsigned int i2 = 0;

    while (i1 < l1 && i2 < l2)
    {
        if (pt1[i1] > pt2[i2])
        {
            idx.emplace_back(i1);
            ++i1;
        }
        else
        {
            idx.emplace_back(i2 ^ 0xFFFFFFFF);
            ++i2;
        }
    }
    while (i1 < l1)
    {
        idx.emplace_back(i1);
        ++i1;
    }
    while (i2 < l2)
    {
        idx.emplace_back(i2);
        ++i2;
    }

    return idx;
}

template <class T>
ROOT::RVec<T> MergeCopy(const ROOT::RVecI &idx, const ROOT::RVec<T> &v1, const ROOT::RVec<T> v2)
{
    ROOT::RVec<T> r;
    r.reserve(idx.size());
    for (auto i : idx)
    {
        if (i < 0)
        {
            r.emplace_back(v2[i ^ 0xFFFFFFFF]);
        }
        else
        {
            r.emplace_back(v1[i]);
        };
    };
    return r;
}

template <class T>
ROOT::RVec<T> ElectronMergeCopy(const ROOT::RVecI &idx, const ROOT::RVec<T> &v1, const T v2)
{
    ROOT::RVec<T> r;
    r.reserve(idx.size());
    for (auto i : idx)
    {
        if (i < 0)
        {
            r.emplace_back(v2);
        }
        else
        {
            r.emplace_back(v1[i]);
        };
    };
    return r;
}

template <class T>
ROOT::RVec<T> ElectronMergeCopy(const ROOT::RVecI &idx, const T v1, const ROOT::RVec<T> v2)
{
    ROOT::RVec<T> r;
    r.reserve(idx.size());
    for (auto i : idx)
    {
        if (i < 0)
        {
            r.emplace_back(v2[i ^ 0xFFFFFFFF]);
        }
        else
        {
            r.emplace_back(v1);
        };
    };
    return r;
}

template <class T>
ROOT::RVec<T> ElectronMergeCopy(const ROOT::RVecI &idx, const T v1, const T v2)
{
    ROOT::RVec<T> r;
    r.reserve(idx.size());
    for (auto i : idx)
    {
        if (i < 0)
        {
            r.emplace_back(v2);
        }
        else
        {
            r.emplace_back(v1);
        };
    };
    return r;
}
#endif
