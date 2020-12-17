# README - T. A. C. Cross Assembler

## Introduction 

The TAC cross assembler consumes a modified T.A.C. assembler and python with assembler markup. It produces an absolute binary image in PTM format. 

This is a low level assembler. It's meant to consume code in the documented programming format found in "Programming Manual for T.A.C., Type S3301", The Marconi Company, 1965.  However, it introduces symbolic addressing to simplify program construction.

The cross aseembler can read code written in:

- original format (as specified in the Programming Manual)
- original format + Symbols (see the user guide)
- original format embedded in Python source comments (see the user guide)

The TAC cross assembler can be executed on most modern compute platforms as it's written in pure Python.  A Python v3 interpreter is required. 

PTM is an annotated, archivally targetted human readable description of a paper tape.   It feeds a utility that drives a paper tape punch to create the actual, loadable paper tape. The tape is produced in an absolute binary format, suitable for the TAC's native tape loading instructions.

## Files

- [TAC-XAssembler.py](TAC-XAssembler.py)

## Documentation

- [Users Guide](UsersGuide.md)
- [Copyright Statement)](COPYRIGHT)
- [License](LICENSE)

## Release History

- **0.0.0 - 17 Dec. 2020** is the first completed release of software. Minimal bounds, and error checking is available in the first source release.

## Known Issues

1. Python Decompilation feature ( -P ) for listings is incomplete and experimental.  Its purpose is to make visual comparison betwee original Python-based markup ( -p ) easier complete. This should aid in debugging. 
2. User's Guide is a work in progress.