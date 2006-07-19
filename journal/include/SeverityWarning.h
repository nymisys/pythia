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

#if !defined(journal_SeverityWarning_h)
#define journal_SeverityWarning_h


// forward declarations
namespace journal {
    class Diagnostic;
    class SeverityWarning;
    class Index;
}


class journal::SeverityWarning : public journal::Diagnostic {

// types
public:
    typedef Index index_t;

// interface
public:
    string_t name() const { return  "warning." + facility(); }
    static state_t & lookup(string_t);

// meta-methods
public:
    virtual ~SeverityWarning();
    
    SeverityWarning(string_t name) :
        Diagnostic(name, "warning", lookup(name)) {}

// disable these
private:
    SeverityWarning(const SeverityWarning &);
    const SeverityWarning & operator=(const SeverityWarning &);

// data
private:
    static index_t * _index;
};


#endif
// version
// $Id: SeverityWarning.h,v 1.1.1.1 2005/03/08 16:13:56 aivazis Exp $

// End of file 
