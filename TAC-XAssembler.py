import sys, getopt, os, re

org = 0
operations = {
                0o03 : "IOWrite( {0} )",
                0o04 : ["A = IORead()", "D = IORead()"],
                0o05 : ["IOWrite( A )", "IOWrite( D )"],
                0o10 : "A = {0}",
                0o11 : "A = A + {0}",
                0o12 : "A = A - {0}",
                0o13 : "A = A & {0}",
                0o14 : "{0} = A",
                0o15 : "A = {0}\nB = {1}",
                0o17 : "{0} = 0",
                0o20 : "B = {0}",
                0o21 : "B = B + {0}",
                0o22 : "B = B - {0}",
                0o23 : "B = B & {0}",
                0o24 : "{0} = B",
                0o25 : [ "D = A", "A = D" ],
                0o26 : [ "A = ~A\nB = ~B", "D = ~D"],
                0o27 : [ "A = 0\nB = 0", "D = 0"],
                0o30 : "D = {0}",
                0o31 : "D = D + {0}",
                0o32 : "D = D - {0}",
                0o33 : "D = D & {0}",
                0o34 : "{0} = D",
                0o50 : "if ((A << 20) & B) == 0: {0}()",
                0o51 : "if ((A << 20) & B) != 0: {0}()",
                0o52 : "if ((A << 20) & B) > 0: {0}()",
                0o53 : "if ((A << 20) & B) < 0: {0}()",
                0o57 : "{0}()",
                0o60 : "if D == 0: {0}()",
                0o61 : "if D != 0: {0}()",
                0o62 : "if D > 0: {0}()",
                0o63 : "if D < 0: {0}()",
                0o67 : "{0}()",
                0o72 : "increment N to {0}",               
                0o76 : "setIO({0})"

            }

def getPunch( word):
    wordLines = []
    #print(word)
    #print("{0:o}".format(word))
    #print('{0:b}'.format(word))
    #print(len('{0:b}'.format(word)))
    character = ""
    for i in range (15,20):
        if i == 17: 
            character = "." + character
        if ((1 << i)) & word:
            character = "o" + character 
        else:
            character =  "-" + character 
    wordLines.append(character)
    character1 = ""
    for i in range (10,15):
        if i == 12: 
            character1 = "." + character1
        if ((1 << i)) & word:
            character1 = "o" + character1 
        else:
            character1 =  "-" + character1 
    wordLines.append(character1)
    character2 = ""
    for i in range (5,10):
        if i == 7: 
            character2 = "." + character2
        if ((1 << i)) & word:
            character2 = "o" + character2 
        else:
            character2 =  "-" + character2 
    wordLines.append(character2)    
    character3 = ""
    for i in range (0,5):
        if i == 2: 
            character3 = "." + character3
        if ((1 << i)) & word:
            character3 = "o" + character3 
        else:
            character3 =  "-" + character3 
    wordLines.append(character3)    
    #print(wordLines)
    return wordLines

def secondPass (listing, lines, symbols, outputPython):
    if listing is not None: listingFile = open(listing,"w")
    address = org
    lastAddress = None
    for l in lines:
        labelField = ""
        opField = ""
        flagField = ""
        addressField = ""
        dataField = ""
        commentField = ""
        statement = ""
        python = ""
        if "label" in l:
            labelField = l["label"] + ":"
            symbols[l["label"] ] = address
        if "operation" in l:
            opField = '{0:2o}'.format(l["operation"])
            
        if "flags" in l:
            flagField = '{0:1o}'.format(l["flags"])
        if "comment" in l:
            commentField = "; " + l["comment"]
        if "address" in l:       
            try:
                addressField = '{0:7o}'.format(l["address"])
            except Exception:
                addressField = l["address"]
        if "python" in l:       
            python = l["python"]
        if (( "data" in l and len(l['data']) > 0 ) or 'operation' in l ):
            if "data" in l:
                try:
                    dataField = '{0:0>7o}'.format(int(l["data"],8))
                except Exception:
                    dataField = '{0:>7}'.format(l["data"])
                if listing is not None:  
                    listingFile.write( 
                    '{0:0>7o}{1:>8s} {2}                                           {3}\n'.format( 
                        address,
                        labelField,
                        dataField,
                        commentField ))
                    #l["binary"] = int(l["data"])
                    #punch = getPunch(l["binary"])
                    #print(punch)
                pass
            else: 
                _address = l["address"]
                if lastAddress != None:
                    _address = lastAddress
                    lastAddress = None
                if l["operation"] == 0o71:
                    lastAddress = _address
                else:
                    try:
                        statement = disassembleToPython( getWord( l["flags"], l["operation"], symbols[_address] ), symbols)
                    except Exception :
                       
                        try:
                            statement = disassembleToPython( getWord( l["flags"], l["operation"], int(_address,8) ), symbols)
                        except: 
                            if listing is not None: listingFile.write("E " + str(l['lineNumber']) + " symbol definition error in address for " + str(_address) + "\n" )  
                if statement == None: statement = ""
                if outputPython and listing is not None:
                    listingFile.write( 
                        '{0:0>7o}{1:>8s} {2:0>1}{3:>3} {4:<8} {5:<35} | {6:>4}. {7:<36} {8}\n'.format( 
                        address,
                        labelField,
                        flagField,
                        opField,
                        addressField,
                        statement,
                        l["lineNumber"],
                        python,
                        commentField))
                elif listing is not None:
                    listingFile.write( 
                        '{0:0>7o}{1:>8s} {2:0>1}{3:>3} {4:<8} {5:<35} {6}\n'.format( 
                        address,
                        labelField,
                        flagField,
                        opField,
                        addressField,
                        statement,
                        commentField))
            l['absAddress'] = address
            address = address+1
        elif listing is not None:
            listingFile.write(
                '                                                                  {0}\n'.format(commentField)
            )

    for l in lines:
        if 'address' in l:
            try:
                l['addressResolved'] = int(l['address'],8)
            except Exception:
                try:
                    symbolAddress = symbols[l['address']]
                    if symbolAddress != None:
                        l['addressResolved'] = symbolAddress
                except Exception :
                    if listing is not None: listingFile.write( "E " + str(l['lineNumber']) + " symbol definition error in address for " + str(l['address']) + "\n")
        if 'data' in l:
            try:
                l['dataResolved'] = int(l["data"],8)
            except Exception:
                try:
                    l['dataResolved'] = symbols[l['data']]
                except Exception:
                    pass #listingFile.write( "E " + str( +l['lineNumber']) + " symbol definition error in data for " + str(l['data']) + "\n")  
            
    if listing is not None:
        listingFile.write("\n\nSymbols\n")

        for s in symbols:
            listingFile.write(
                '{0:<8s}{1:>8o}\n'.format(s,symbols[s])
                )
        listingFile.flush()
        listingFile.close()           




def disassembleToPython(word, symbols):
    #print("{0:o}".format(word))
    #flags = ((3 << 18) & word)>>18
    #print("{0:o}".format(flags))
    operation = ( (0o77 << 12) & word ) >> 12
    #print("{0:o}".format(operation))
    op = operations[operation]
    address = 0o7777 & word
    #print("{0:o}".format(address))
    if op is not None and \
        len(op) == 2 and \
        (address == 0 or address == 1):
            op = op[address]
    statement = None
    for s in symbols:
        if symbols[s] == address:
            symbol = s
            statement = op.format(symbol)
    return statement
    

def getWord( flags, operation, address):
    return (flags << 18) | (operation << 12) | address

def outputPTM(lines, symbols, ptmFileName):
    ptmFile = open(ptmFileName,"w")
    ptmFile.write( "ooo.oo ;                    37 start character\n")
    for l in lines:
        punch = None
        if "dataResolved" in l:
            punch = getPunch(l['dataResolved'])
        elif "addressResolved" in l: 
            punch = getPunch( getWord( l['flags'], l['operation'], l['addressResolved']))
        if punch is not None:
            #try:
                ptmFile.write(punch[0])
                if "label" in l:
                    ptmFile.write(" ; {0:<7}".format(l['label']))
                else:
                    ptmFile.write(" ;        ")
                ptmFile.write("{0:>4o} {1:>5o} ".format( l["lineNumber"], l['absAddress'] ))
                if "dataResolved" in l:
                    ptmFile.write( ' {0:0>8o}\n'.format( l["dataResolved"]  )) 
                elif "address" in l:
                    ptmFile.write(' {0:<1o} {1:0>2o} {2:<6} ({3:0>4o})\n'.format( l['flags'], l['operation'], l['address'], l['addressResolved'] ))
                else: 
                    ptmFile.write("\n")
                if "comment" in l:
                    ptmFile.write(punch[1] + " ; " + '                   {0:s}\n'.format(  l['comment']))
                else:
                    ptmFile.write(punch[1] + " ; \n")
                ptmFile.write(punch[2] + " ; \n"  + punch[3] + " ; \n" )
            #except Exception:
            #    pass
    ptmFile.flush()
    ptmFile.close()


def readSource(inputFile, pythonInput):
    global org
    sourceFile = open(inputFile,"r")
    lines = []
    lineNo = 0
    for sourceLine in sourceFile:
        lineNo = lineNo + 1
        line = {}
        try:
            if "ORG" in sourceLine:
                org = int(sourceLine[37:].replace("ORG","").strip(),8)
                lineNo = lineNo + 1
                sourceLine = next(sourceFile)
            if len(sourceLine) != 0 \
                or sourceLine.strip() != "" \
                or len(sourceLine) > 38:
                if (pythonInput):
                    line["python"] = sourceLine[0:36]
                    sourceLine = sourceLine[37:]   
    
                if len(sourceLine.strip()) != 0:
                    if ";" in sourceLine:
                        commentSplit = sourceLine.strip().split(";")
                        if len(commentSplit) > 1 :
                            line["comment"] = commentSplit[1].strip()
                            sourceLine = commentSplit[0]
                        else: 
                            line["comment"] = commentSplit[0].strip()
                            lineNo = lineNo + 1
                            lines.append(line)
                            line = {}
                            sourceLine = next(sourceFile)
                            sourceLine = sourceLine[38:]
                    if ":" in sourceLine:
                        labelSplit = sourceLine.split(":")
                        line["label"] = labelSplit[0].strip()
                        sourceLine = labelSplit[1].strip()
                    if len(sourceLine.strip().split(" ")) == 1:
                        line["data"] = sourceLine.strip()
                    #if re.match("\s*[0-7]{7}\s*", sourceLine):
                    #    line["data"] = sourceLine.strip().split(" ")[0]
                    else:
                        if ( not re.match("\s*", sourceLine)) or (sourceLine != "") :
                            tuples = sourceLine.strip().split(" ")
                            if len(tuples)==1 and tuples[0].strip() != "":
                                if re.match("[0-7]{1,7}",tuples[0]):
                                    line["operation"] = int(tuples[0],8)
                                else:
                                    line["address"] = tuples[0]
                            if len(tuples)==2:
                                line["flags"] = int(tuples[0],8)
                                line["operation"] = int(tuples[1],8)
                            if len(tuples) > 2:
                                line["flags"] = int(tuples[0],8)
                                line["operation"] = int(tuples[1],8)
                                line["address"] = tuples[2]
                    line["lineNumber"] = lineNo
                    lines.append(line)
                else:
                    pass
        except Exception as e: 
            print("Error on line " + str(lineNo) + "\n" + str(e))
    sourceFile.close()
    lineNo = 0
    symbols = {}
    for line in lines:
        if "label" in line:
            symbols[line["label"]] = lineNo
        lineNo += 1
    return lines, symbols

def main(argv):
    listing = None
    tape = None
    inputFile = None
    pythonOutput = False
    pythonInput = True
    try:
       opts, __ = getopt.getopt(argv,"i:l:t:pP?h")
    except getopt.GetoptError as e:
       print (str(e))
       print ('TAC-XAssembler.py -i <input> [-l <listing>] [-t <tape>] [-p] [-h|-?]')
       sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-i':
            inputFile = arg
        elif opt == "-l":
            listing = arg  
        elif opt == '-t':
            tape = arg
        elif opt == '-P':
            pythonOutput = True
        elif opt == '-p':
            pythonInput = True
        elif opt == "-?" or opt == "-h":
            print ('TAC-XAssembler.py -i <input> [-l <listing>] [-t <tape>] [-p] [-h|-?]')
            sys.exit(0)
    if inputFile is None:
        print("Input file required.")
        print ('TAC-XAssembler.py -i <input> [-l <listing>] [-t <tape>] [-p] [-h|-?]')
        sys.exit(-1)
    if listing is not None:
        lines, symbols = readSource(inputFile, pythonInput)
        secondPass(listing, lines, symbols, pythonOutput)
        outputPTM(lines, symbols, tape)
    sys.exit(0)


 
if __name__ == "__main__":
   main(sys.argv[1:])