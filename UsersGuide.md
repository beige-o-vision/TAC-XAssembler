# T. A. C. Cross Assembler User's Guide

## Introduction 

The TAC cross assembler consumes a modified T.A.C. assembler and python with assembler markup. It produces an absolute binary image in PTM format. 

The TAC cross assembler can be executed on most modern compute platforms as it's written in pure Python.  A Python v3 interpreter is required. 

PMR is an annotated, archivally targetted human readable description of a paper tape.   It feeds a utility that drives a paper tape punch to create the actual, loadable paper tape. The tape is produced in an absolute binary format, suitable for the TAC's native tape loading instructions.

This is a low level assembler. It's meant to consume code in the documented programming format found in "Programming Manual for T.A.C., Type S3301", The Marconi Company, 1965.  However, it introduces symbolic addressing to simplify program construction.

## Usage

<pre>TAC-XAssembler.py -i <input-file> [ -t <tape-file> ] [ -l <listing-file> ] [ -p [ -P ] ] 
<p>     <b>-i</b> InputFile to read
<p>     <b>-l</b> Output listing file
<p>     <b>-t</b> Output PMR tape file
<p>     <b>-p</b> Read input as a marked up Python source file. 
<p>     <b>-P</b> Include experimental decompiled output.
</pre>

## About the T. A. C.

The T. A. C. is an early transitorised computer.  It was designed by Marconi as their first computer in the late 1950s.  It's original purpose was to supplement analogue, military radar equipment with information overlays. 

Process automation became its second use case.  Two systems were used to monitor and optionally managed the Wylfa nuclear power plant.   

Twelve were built. Two are known to survive. One is in the collection of the National Museum of Computing.  The second is in the private collection of Jim Austin. Only the machine at the National Museum of Computing is currently operable (as of 2020).

## TAC Fundamentals

The T. A. C. is very simple architecture. It's a Von Neumann style computer (unified data and instcution memory). It is not a memory mapped machine.  There's no native stack concept. There's no indirection. All IO uses dedicated instructions.  While it is microprogrammed, it supports only 64 possible instructions. The system at TNMoC doesn't use all those possible instruction codes.

### Memory

All memory access on T.A.C. is direct.  The system has no indirect address regime.  It accepts addresses in the range from 0-7777. 

## Syntax

The basic syntax of this assembler is:

ORG *n*
-or-
[ <LABEL>: ] [ <INSTUCTION WORD> | <DATA WORD>] [ ;<COMMENT> ]

ex. 
<pre>
ORG 50              ; This is a special statement at the start of the source
                    ;   indicating the absolute addressing start of the programme.
VAR1:  1            ; This is a subroutine or symbol definition 
                    ;   Used as a symbol (variable) definition, it consists
                    ;   a label and value.  References in an instruction later
                    ;   its address will be substituted for the symbol.
START: 0            ; This is subroutine entry point or symbol definition
                    ;   Used as a subroutine entry point, it consists of a 
                    ;   label and a data word to hold the
                    ;   subroutine return instruction. A link instruction with 
                    ;   this symbol will jump to this location, and overwrite
                    ;   the data with a jump instuction to it's last programme
                    ;   counter value.
       0 30 VAR1    ; This an **instruction word** which references the memory location
                    ;   of the symbol VAR1
       3777777      ; This is a **data word** holding the maximum 20 - bit value
</pre>

### Input File Types

#### Original (with or without symbols) in UTF-8 Text

A text file including:

- 1 ORG line at the top
- Up to 4094 program statement as defined below
- Any number of comment statements

#### Python Source with Comment Embedded Assembler in UTF-8 Text

When indicated by command flag **-p**, the system will treat python code from columns 1-38 as a special comment field. It will read the rest of the file as if it were in original format (see above). 

To be valid Python, the should always be either a comment charcter(#) after a Python statement at column 37, or if the line is blank, then a comment charchater (#) at the curren Python indent level

This feature allows a custom emulation of the TAC's behaviour is Python to be written side by side with assembler. If commenting is done as required, the Python script remains executable and debuggable.

### Data Representation

All values must be in Octal integer notation from   -2000000 < n < 2000000  (-524288 [10] < n <  524288 [10])

### ORG statement

Each programme source file may define on ORG statement.  It tells the assembler what address to start when assigning labels. It must be in the format of 'ORG' + white space + 0-7777 (octal)

### Labels

A label is a text string of up to six characters, followed by a colon.  It may be prepended to either a code statement, or data statement.  The symbol may be defined anywhere after the ORG statement. It may be referenced as a data statement, or in the address argument of code statement.

### Programme Statements

#### Data Statement

A data statement consists of a data item, either as a data representation or a reference to a label (symbol).  It may optionally be pre-pended by a label. It may also be followed by a comment. 

#### Code Statement

A code statement has three fields, as defined by the Programming Guide.  

- 2-bit Stop or Check flag (indicator)
- 6-bit Operation 
- 12-bit Address or argument 

These should be separated by white space.  A label can proceed them.  A comment may follow them.

### Comments

A comment is any text following a semi-colon, up to the end of the current line. The cross-compiler stores and outpus this content where relevant in listings and PMR files.







