
#include "ROOT/RVec.hxx"
#include <iostream>
#include <fstream>
#include <string>

class PrintAsCsv
{
private:
    std::ofstream *out_;

public:
    void operator()(const unsigned long long event, const ROOT::RVecF &pt, const ROOT::RVecF &eta, const ROOT::RVecF &phi)
    {
        for (unsigned int i = 0; i < pt.size(); ++i)
        {
            *out_ << event << ", " << i << ", " << std::fixed << std::setw(7) << std::setprecision(3) << pt[i] << ", " << eta[i] << ", " << phi[i] << std::endl;
        }
    }

    void open(const std::string &name)
    {
        out_ = new std::ofstream(name);
        *out_ << "event, index, pt, eta, phi" << std::endl;
    }
    void close()
    {
        out_->close();
        delete out_;
    }
};

class PrintAsCsv1
{
private:
    std::ofstream *out_;

public:
    void operator()(const unsigned long long event, const ROOT::RVecF &pt, const ROOT::RVecF &eta, const ROOT::RVecF &phi, const ROOT::RVecI &idx)
    {
        for (unsigned int i = 0; i < pt.size(); ++i)
        {
            *out_ << event << ", " << i << ", " << std::fixed << std::setw(7) << std::setprecision(3) << pt[i]
                  << ", " << eta[i] << ", " << phi[i] << ", " << (idx[i] < 0) << std::endl;
        }
    }

    void open(const std::string &name)
    {
        out_ = new std::ofstream(name);
        *out_ << "event, index, pt, eta, phi, type" << std::endl;
    }
    void close()
    {
        out_->close();
        delete out_;
    }
};