import ast

def liststringToList(listString):
  if not isinstance(listString, str):
    return
  return ast.literal_eval(listString)