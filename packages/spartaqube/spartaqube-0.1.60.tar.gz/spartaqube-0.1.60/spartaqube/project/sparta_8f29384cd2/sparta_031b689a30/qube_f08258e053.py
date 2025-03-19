def sparta_8304abec60(s):
	if isinstance(s,str):
		s=s.strip().lower()
		if s in['true','1','yes','y']:return True
		elif s in['false','0','no','n']:return False
	raise ValueError(f"Cannot convert '{s}' to a boolean.")
def sparta_a75fcac5d0(assign_dict):
	A=assign_dict;C=A['guiType'];B=A['value']
	if C=='boolean':
		if not isinstance(B,bool):B=sparta_8304abec60(B)
	D=f"import json\n{A['variableState']} = json.loads({A['interactiveVarDict']})";E=f"{A['variable']} = {B}";return{'assign_code':E,'assign_state_variable':D}