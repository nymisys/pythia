// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                             Michael A.G. Aivazis
//                      California Institute of Technology
//                      (C) 1998-2005  All Rights Reserved
//
// <LicenseText>
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#if !defined(journal_SeverityFirewall_h)
#define journal_SeverityFirewall_h


// forward declarations
namespace journal {
    class Diagnostic;
    class SeverityFirewall;
    class Index;
}


class journal::SeverityFirewall : public journal::Diagnostic {

// types
public:
    typedef Index index_t;

// interface
public:
    string_t name() const { return  "firewall." + facility(); }
    static state_t & lookup(string_t);

// meta-methods
public:
    virtual ~SeverityFirewall();
    
    SeverityFirewall(string_t name) :
        Diagnostic(name, "firewall", lookup(name)) {}

// disable these
private:
    SeverityFirewall(const SeverityFirewall &);
    const SeverityFirewall & operator=(const SeverityFirewall &);

// data
private:
    static index_t * _index;
};


#endif
// version
// $Id: SeverityFirewall.h,v 1.1.1.1 2005/03/08 16:13:55 aivazis Exp $

// End of file 
