from TruthTablesTree import *;


#class 







def initTitle():
    title = str(input("title plz"));
    return title;

def initFile():
    file = str(input('Would you like to write (append) the output to a file? Press return for stdout, otherwise filename'));
    f = None;
    if len(file) > 0:
        f = open(file, 'a');
        if f == None:
            f = open(file,'w');
    return f;

def initGeneric():
    generic = str(input("would you like the expression to be evaluated or for there to be left blanks? b for both, e for empty, return for evaluate"));
    if len(generic) == 0:
        return False;
    if generic == "b":
        return generic;
    return True;


def initNumberOfColumns():
    numberOfColumns = -1;
    while numberOfColumns == -1:
        try:
            numberOfColumns = int(input("number of columns"));
        except:
            print("whoops!");
    return numberOfColumns;


def initVariableLists(variableList,variables,numberOfColumns):

    i=0;
    added = False;
    numVariables = 0;
    while i < numberOfColumns:
        nextVar = str(input("next var plz"));
        if not len(nextVar) > 0:
            print("whoomp (there it is) idthink tha'ts wot ya me8nt to print there h0n");
            continue;
        if nextVar=="q":
            try:
                inter = variableList.pop();
            except:
                print("was empty; continuing");
                continue;
            if added:
                variables.pop();
            
            if inter[1] == 1:
                numVariables += -1;
            i += -1;
            
            print("removed previous entry: ",inter);
            continue;
        added = False;

        # print("nextvar: {" + str(nextVar)+"}","charf(nextvar): {" + charf(nextVar)+"}","charf in neglist: {",charf(nextVar) in negList,"}");

        if charf(nextVar) in symbols or charf(nextVar) in negList:
            variableList.append((nextVar,0,None,i));
            
        else:
            
            if charf(nextVar) not in variables:
                numVariables += 1;
                variables.append(charf(nextVar));
                added = True;
            variableList.append((nextVar,1,None,i));
        
            
        
        i+= 1;

def initTreeVariableList(variableList,variableListParens):
    for x in variableList:
        # print("iterating thru variablelist; to be adding (x[0],x[3])",(x[0],x[3]));
        variableListParens.append((x[0],x[3]));
    i = 0;
    while i < len(variableListParens):
        curr = variableListParens[i][0]
        ID = variableListParens[i][1];
        count = 0;
        if curr[0] == "(":
            if ")" in curr:
                continue;
            count = 1;
            while curr[count] == "(":
                count += 1;
            suffix = curr[count:];
            for _ in range(count):
                variableListParens.insert(i,None);
            for x in range(count):
                variableListParens[i+x]=("(",None);
            variableListParens[i+count]=(suffix,ID);
            i += count;
        elif curr[len(curr)-1] == "(":
            count = 1;
            while curr[len(curr)-(1+count)] == "(":
                count += 1;
            prefix = curr[:-count];
            variableListParens[i]=(prefix,ID);
            for x in range(count):
                variableListParens.insert(i+1+x,("(",None));
            i += count;
        elif curr[len(curr)-1] == ")":
            count = 1;
            while curr[len(curr)-(1+count)] == ")":
                count += 1;
            prefix = curr[:-count];
            variableListParens[i]=(prefix,ID);
            for x in range(count):
                variableListParens.insert(i+1+x,(")",None));
            i += count;
        i += 1;

def generateLatexHeader(variableList,variables,title,file,tree=None,):
    string = "\n";
   

    string += "\n\\begin{tabular}{|";
    for x in range(len(variables)):
        string += "c ";
    string += "|";
    for x in variableList:
        if tree != None and tree.getRoot().getID() == x[3]:
            # print("root id: ",tree.getRoot().getID()," node id: ",x[3]);
            string += ">{\huge \\bfseries}c ";
        else:
            string += "c ";
    string += "|}";
    string += "\\hline";
    string += "\\multicolumn{"+str(len(variableList)+len(variables))+"}{|c|}{"+title+"}\\\\\n";
    string += "\\hline\n"
    handled = [];
    i=0;
    j = 0;
    while i <len(variables):

        if variableList[j][1] == 1:
            char = charf(variableList[j][0]);
            if char not in handled:
                handled.append(char);
                i += 1;
                string += char+" & ";

        j +=1;
            
    for i in range(len(variableList)):
        if variableList[i][1] == 1:
            string += variableList[i][0];
        else:
            string += "$"+variableList[i][0]+"$";
        if i < len(variableList)-1:
            string += " & ";
        else:
            string += "\\\\\n";

    string += "\\hline\n";

    if file == None:
        print(string);
    else:
        file.write(string);

def generateManipulatedLatex(variableList,variables,title,tree,generic,file):
    string = "";
    generateLatexHeader(variableList,variables,title,file,tree);

    numberOfRows = 2**len(variables);
    i = numberOfRows;
    varDict = {}
    for x in variables:
        varDict[x] = [];
    tree.fillNodesDictionary(varDict,variables);

    while i > 0:
        # print("aye aye aye\n");
        inter = i;
     #   row = parse(i);

        tree.flushAssignments();
        for j in range(len(variables)):
            string += str(inter%2)+ " & ";
            # for vl in range(len(variableList)):
            #     if charf(variableList[vl][0])==variables[x]:
            #         variableList[vl] = (variableList[vl][0],variableList[vl][1],inter % 2);
                    
            for x in varDict[variables[j]]:
                x.setAssignment(inter%2);


            inter = int(inter/2);

        if not generic:
            tree.evaluate();

        for y in range(len(variableList)):
            if not generic:
                assignment = tree.getAssignmentByID(variableList[y][3]);
                # print("This time id is: ",variableList[y][3], " and its assignment is: ",assignment);

                string += str(assignment);
            else:
                if variableList[y][1] == 1:
                    string += str(tree.getAssignmentByID(variableList[y][3]));
                else:
                    string += " ";
                
            if y < len(variableList)-1:
                string += " & ";
            else:
               string += "\\\\\n";
                
              
        
              
        i = i-1;
        string += "\\hline\n";

    string += "\\end{tabular}\n";

    if file == None:
        print(string);
    else:
        file.write(string);


def main():

    #general globalish declarations:

    variableList = []; ###format: (name,is a variable, generic belegung, unique number);
    variables = [];

    print("Welcome to Truth Tables, an app that generates Latex code for truth tables (shocker).\n")
    print("There are 2 guidelines for using this software:\n")
    print("\t1. Don't put parentheses on both sides of a character. That is semantically reckless and as such my compiler will recoil in disgust, evincing this in the form of a thrown error and a crash.\n")
    print("\t2. to use standard operators, use the their latex codes")
    print("\t\tlogical and = \land")
    print("\t\tlogical or = \lor")
    print("\t\timplication = \\to")
    print("\t\tbiimplication = \leftrightarrow");
    print("\t\tnegation = \\neg\n")
    print("If you follow the prompts, and don't make any syntax errors, you should be good to go.\n")
    print("That said, if you have any questions or would like to report a bug, please don't hesitate to write me up at felix.herron@gmail.com *dabs*\n");

    title = initTitle();

    f = initFile();
    generic = initGeneric();
    
    
    numberOfColumns = initNumberOfColumns();   

    initVariableLists(variableList,variables,numberOfColumns);

    # print("variablelist: ",variableList,"\n\nvariables: ",variables);

    variableListParens = [];
    initTreeVariableList(variableList,variableListParens);
    

    # print("variablelist: " ,variableList, " variableLlistParent: " ,variableListParens);

    tree = generateSyntaxTree(variableListParens,0,len(variableListParens)-1);
    print("here is ma tree: " + str(tree));

    # generateGenericLatex(variableList,variables,title);

    if generic == "b" or generic == "B":
        generateManipulatedLatex(variableList,variables,title,tree,True, f);
        generateManipulatedLatex(variableList,variables,title,tree,False, f);
    else:
        generateManipulatedLatex(variableList,variables,title,tree,generic, f);

    
    if f != None:
        f.close();

main();

