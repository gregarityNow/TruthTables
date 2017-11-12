symbols = ["\\land","\land","\\lor","\lor","\leftrightarrow","\\leftrightarrow","\to","\\to"];
negList = ["\\neg","\neg"];
openParen = "(";
closeParen = ")";
landList = ["\\land","\land"];
lorList = ["\\lor","\lor"];
leftrightarrowList = ["\leftrightarrow","\\leftrightarrow"];
toList = ["\to","\\to"];


class Tree:
	def __init__(self,root):
		self.root=root;
		self.height = 1-(root == None);
		self.size=1-(root == None);
		

	def isEmpty(self):
		return not (self.size > 0);


	def setRoot(self,node):
		if self.root == None:
			self.root = node;
			self.size = 1;
		else:
			self.root = node;

	def getRoot(self):
		return self.root;

	def grow(self,amount = 1):
		self.size += amount;

	def getSize(self):
		return self.size;

	def fillNodesDictionary(self,varDict,variables):

		
		def recurse(inter):
			if inter.getLeft() != None:
				recurse(inter.getLeft());
			if inter.getValue() in variables:
				varDict[inter.getValue()].append(inter);
			if inter.getRight() != None:
				recurse(inter.getRight());

		recurse(self.getRoot());
		return varDict;
		

	def getHeight(self):
	
		def recurse(node,i):

	
			if self.height < i:
				self.height = i;
			if node.getLeft() != None:
				recurse(node.getLeft(),i+1);
			if node.getRight() != None:
				recurse(node.getRight(),i+1);

		recurse(self.root,0);

		if self.getRoot() != None:
			self.height += 1;
		return self.height;

	def getAssignmentByID(self,ID):
		# print("getting id, for id = ",ID);
		
		def recurse(inter):
			# print("checking inter for id = ",inter.getID());
			if inter.getID() == ID:
				# print("yep found it and assignment is: ",inter.getAssignment());
				retID.append(inter.getAssignment());
				# print("retid after appending: ",retID);
				return;
			if inter.getLeft() != None:
				recurse(inter.getLeft());
			
			if inter.getRight() != None:
				recurse(inter.getRight());
		retID = [];
		recurse(self.getRoot());
		return retID[0];

	def flushAssignments(self):

		def recurse(inter):
			if inter.getLeft() != None:
				recurse(inter.getLeft());
			inter.setAssignment(None);
			if inter.getRight() != None:
				recurse(inter.getRight());

		recurse(self.getRoot());
	
		

	def evaluate(self):
		def getAssignmentOfNode(inter):
			# print("here's what we got: ", str(inter));
			if inter.getLeft() != None:
				getAssignmentOfNode(inter.getLeft());
				leftAssignment = inter.getLeft().getAssignment();
				# print("done and leftassignment is: ",leftAssignment);
			else:
				leftAssignment = None;
			if inter.getRight() != None:
				getAssignmentOfNode(inter.getRight());
				rightAssignment = inter.getRight().getAssignment();
			else:
				rightAssignment = None;
			if rightAssignment == None and leftAssignment == None:
				# print("returning");
				return;
			


			#the good stuff
			if inter.getValue() in negList:
				
				if rightAssignment != None:
					inter.setAssignment(1-rightAssignment);
				else:
					inter.setAssignment(1-leftAssignment);
					# print("just set and assignment is: ",inter.getAssignment());
			elif inter.getValue() in symbols:
				if inter.getValue() in landList:
					# print("we've got a land on our hadns");

					inter.setAssignment(rightAssignment*leftAssignment);

				elif inter.getValue() in lorList:
					assignment = int(rightAssignment == 1 or leftAssignment == 1);
					inter.setAssignment(assignment);

				elif inter.getValue() in leftrightarrowList:
					assignment = int(rightAssignment == leftAssignment);
					inter.setAssignment(assignment);
					# return assignment;

				elif inter.getValue() in toList:
					if leftAssignment == 1 and rightAssignment == 0:
						inter.setAssignment(0);
						# return 0;
					else:
						inter.setAssignment(1);
						# return 1;
			



			

		getAssignmentOfNode(self.getRoot());
		


	def __str__(self):
		# def recurse(node, ret):
		# 	#bla bla bla
		# 	recurse(node.getLeft(),ret);
		# 	ret += node.getValue();
		# 	ret += ", ";
		# 	recurse(node.getRight());
		ret = "\n";

		def allNone(l):
			for x in l:
				if l != None:
					return False
			return True;

		currentLevel = [self.root];
		counter = self.getHeight();


		while counter > 0:
			nextLevel = [];
			for node in currentLevel:
				if node == None:
					ret += "   " * (counter-1) * (counter-1) + " {   } ";
					for _ in range(2):
						nextLevel.append(None);
				else:
					ret += "   " * (counter-1) * (counter-1) + " { "+node.getValue()+" } ";
					nextLevel.append(node.getLeft());
					nextLevel.append(node.getRight());
			ret += "\n\n";
			counter += -1;
			currentLevel = [];
			for x in nextLevel:
				currentLevel.append(x);


		
		return ret;
		


class Node:
	def __init__(self,value, left, right, parent,idParam):
		self.value = value;
		self.left = left;
		self.right=right;
		self.parent=parent;
		self.id = idParam;
		self.assignment = None;

	def setParent(self,parent,tree):
		self.parent=parent;

		if self == tree.getRoot():
			tree.setRoot(parent);

		self.assignment=None;
	def getParent(self):
		return self.parent;
	def setLeft(self,left):
		if self.left == None:
			self.left=left;
		else:
			self.left.setLeft(left);


	def setAssignment(self,assignment):
		# print("previously, node: ",self," assignment was: ",self.assignment," and argument is: ",assignment)
		self.assignment = assignment;
		# print("afterwards, assginment was: ",self.assignment);
	def getAssignment(self):
		return self.assignment;

	def getLeft(self):
		return self.left;
	def setRight(self,right):
		if self.right == None:
			self.right=right;
		else:
			self.right.setRight(right);
	def getRight(self):
		return self.right;

	def getValue(self):
		return self.value;

	def getID(self):
		return self.id;

	def __str__(self):
		pv = "";
		if self.getParent() == None:
			pv = "None";
		else:
			pv = self.getParent().getValue();

		lv = "";
		if self.getLeft() == None:
			lv = "None";
		else:
			lv = self.getLeft().getValue();

		rv = "";
		if self.getRight() == None:
			rv = "None";
		else:
			rv = self.getRight().getValue();
		return "Node with value: " + self.value + " and id: " + str(self.id) + "and assignment : " + str(self.assignment) + " and parent: " + pv + " and left : " + lv + " and right: " + rv;



def opFoundNegged(l,tree,first,last,neg,op):
	if not first <= last:
		print("syntax error opfoundnegged");
		return;
	if l[first][0] not in symbols and not l[first][0] == openParen and l[first][0] not in negList:
		# new node var - store first char value in var;
		var = Node(l[first][0],None,None,None,l[first][1]);
		# var.parent = neg;
		var.setParent(neg,tree);
		neg.setLeft(var);
		tree.grow();
		firstVarFound(l,tree,first,last,op);
	# elif first char is paren:
	elif l[first][0] == openParen:
		newLast = scanClosingParen(l,first);
		kidTree = newTree(l,first+1,newLast);
		kidTree.getRoot().setParent(neg,tree);
		op.setRight(kidTree.getRoot());
		tree.grow(kidTree.getSize());
		firstVarFound(l,tree,first+1,last,op);
	# elif first char is neg:
	elif l[first][0] in negList:
		otherNeg = Node(l[first][0],None,None,None,l[first][1]);
		otherNeg.setParent(neg,tree);
		neg.setLeft(otherNeg);
		tree.grow();
		opFoundNegged(l,tree,first+1,last,otherNeg,op);


def opFound(l,tree,first,last,op):#theoretically finisehd
	if not first < last+1:
		print('syntax error methinks');
		return;
	# elif first char is paren:
	if l[first][0] == openParen:
		newLast = scanClosingParen(l,first);
		kidTree = newTree(l,first+1,newLast);
		kidTree.getRoot().setParent(op,tree);
		op.setRight(kidTree.getRoot());
		tree.grow(kidTree.getSize());
		firstVarFound(l,tree,first+1,last,op);
	# if first char is var:
	elif l[first][0] not in symbols and l[first][0] not in negList:
		# new node var - store first char value in var;
		var = Node(l[first][0],None,None,None,l[first][1]);
		# var.parent = op;
		var.setParent(op,tree);
		op.setRight(var);
		tree.grow();
		firstVarFound(l,tree,first+1,last,op);
	elif l[first][0] in negList:
		neg = Node(l[first][0],None,None,None,l[first][1]);
		# neg.parent = op;
		neg.setParent(op,tree);
		op.setRight(neg);
		tree.grow();
		opFoundNegged(l,tree,first+1,last,neg,op);
	



def firstVarFound(l,tree,first,last,var):#theoretically pythonized
	if not first < last:
		# print("first >= last");
		return;
	if l[first][0] in symbols:

		# new node op - store char value op in node;
		op = Node(l[first][0],None,None,None,l[first][1]);
		# op.leftChildchild = var;
		op.setLeft(var);
		var.setParent(op,tree);


		tree.grow();
		opFound(l,tree,first+1,last,op);
	else:
		print("syntax error firstVarFound");

		return;

def firstNegged(l,tree,first,last,neg):#theoretically finished

	# if first char is var:

	if l[first][0] == openParen:
		newLast = scanClosingParen(l,first);
		kidTree = newTree(l,first+1,newLast);
		kidTree.getRoot().setParent(neg,tree);
		neg.setLeft(kidTree.getRoot());
		#science
		tree.grow(kidTree.getSize());
		firstVarFound(l,tree,newLast+1,last,neg);

	elif l[first][0] not in negList and l[first][0] not in symbols:

		# new node var - store first char value in node;
		var = Node(l[first][0],None,None,None,l[first][1]);
		neg.setLeft(var);
		var.setParent(neg,tree);

		# will be infertile lol;
		# firstVarFound(l,tree,first+1,last,var);
		tree.grow();
		firstVarFound(l,tree,first+1,last,neg);
	elif l[first][0] in negList:
		otherNeg = Node(l[first][0],None,None,None,l[first][1]);
		otherNeg.setParent(neg,tree);
		neg.setLeft(otherNeg);
		firstNegged(l,tree,first+1,last,neg);

def charf(s):
    new = '';
    for x in s:
        if x == ")" or x == "(":
            pass
        else:
            new += x
    return new;



def scanClosingParen(l,first):#theoretically finished

	deficit = 1;
	newLast = first;
	while deficit > 0:
		newLast += 1;
		if l[newLast][0] == openParen:
			deficit +=1;
		elif l[newLast][0] == closeParen:
			deficit += -1;
		elif newLast +1 == first:
			print("syntax error scan closing paren");
			return -1;

	return newLast;


def newTree(l,first,last):#theoretically finished
	
	# print("newtree first, last",first,last);
	# new Tree();
	tree = Tree(None);
	# if first char is neg:
	if l[first][0] in negList:
		# new node neg - will have left child.
		neg = Node(l[first][0],None,None,None,l[first][1]);
		tree.setRoot(neg);
		tree.grow();
		firstNegged(l,tree,first+1,last,neg);

	# elif first char is paren:
	elif l[first][0][0] == openParen:
		newLast = scanClosingParen(l,first);
		kidTree = newTree(l,first+1,newLast);
		if tree.getSize() < 1:
			tree = kidTree;
		else:
			print("I don't know how it came to this tbh");
		first = newLast+1;
		# # if first char in negList:
		# # 	# new node neg - will have left child.
		# # 	neg = Node(l[first][0],N)
		# # 	neg left child is tree.root;
		# # 	firstNegged(l,tree,first+1,last,neg);
		# if l[first] in symbols:
		# 	print("good because otherwise it makes no sense");
		# 	op = 
		# elif first char is var: #wait this can't happen tho
		# 	new node var -= tore first char value in node;
		# 	firstVarFound(l,tree,first,last,var);
		firstVarFound(l,tree,first,last,kidTree.getRoot());

	# elif first char is var:
	elif l[first][0] not in negList and l[first][0] not in symbols: ## is var
		# new node var -= tore first char value in node;

		var = Node(l[first][0],None,None,None,l[first][1]);
		tree.setRoot(var);
		tree.grow();
		firstVarFound(l,tree,first+1,last,var);
	
	

	return tree;

		


def generateSyntaxTree(l,first,last):

	return newTree(l,first,last);





