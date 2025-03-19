import ast
def sparta_83ab2cf3c6(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_ce8ba6bdcc(script_text):return sparta_83ab2cf3c6(script_text)