from typing import Callable, List, Set, Tuple, TypeVar
from utils import Autograder

import os
import subprocess
import re

from pygccxml import utils as gccutils
from pygccxml import declarations
from pygccxml import parser

import logging
from colorama import Fore, init, Style, Back

# This should prevent pygccxml from outputting INFO messages
gccutils.loggers.set_level(logging.WARNING)

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
AUTOGRADER_DIR = os.path.join(PATH, "autograder")

class_decl: declarations.class_t = None
definitions: Set[Tuple[str, str]] = None

def get_definitions(source_file: os.PathLike) -> Set[Tuple[str, str]]:
  if not os.path.exists(source_file):
    raise RuntimeError(f"Could not find source file: {source_file}")

  with open(source_file, 'r') as file:
    content = file.read()
  
  comment_pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
  regex = re.compile(comment_pattern, re.MULTILINE|re.DOTALL)
  content = regex.sub(lambda match: "" if match.group(2) is not None else match.group(1), content)

  string_pattern = r"\".*\""
  regex = re.compile(string_pattern, re.MULTILINE|re.DOTALL)
  content = regex.sub("", content)

  block_pattern = r"\{.*\}"
  regex = re.compile(block_pattern, re.MULTILINE|re.DOTALL)
  content = regex.sub(block_pattern, content)

  content = content.replace("\n", "")

  definition_pattern = r"(\w+)(?:<\w+(?:,\w+)*>)?::(\w+)"
  regex = re.compile(definition_pattern)
  matches = regex.findall(content)

  return matches

def assert_defined(decl: declarations.declarated_t):
  class_name = class_decl.name
  decl_name: str = None
  if isinstance(decl, declarations.constructor_t):
    decl_name = decl.name
  elif isinstance(decl, declarations.member_function_t):
    decl_name = decl.name
  else:
    raise RuntimeError(f"Unhandled declaration type: {decl}. Please reach out on Ed!")
  
  decl_tuple = (class_name, decl_name)
  if decl_tuple not in definitions:
    raise RuntimeError(f"Found declaration for {decl}, but could not find a matching definition in class.cpp")

def skip_decl(decl: declarations.declaration_t, reason: str):
  print(f"⏩ Skipping {decl}, {reason}")

def find_decl(decl: declarations.declaration_t):
  print(f"🥇 Found {decl}!")

T = TypeVar("T")

def get_decls(getter: Callable[[], T], kind_plural: str) -> T:
  try:
    return getter()
  except RuntimeError as err:
    if "query returned 0 declarations" in str(err):
      raise RuntimeError(f"Could not find any {kind_plural} in class")



def setup():
  main_cpp_path = os.path.join(PATH, "main.cpp")
  class_h_path = os.path.join(PATH, "class.h")
  class_cpp_path = os.path.join(PATH, "class.cpp")

  if not os.path.isfile(main_cpp_path): raise RuntimeError("Couldn't find '{main.cpp}'. Did you delete it from the starter code?")

  # Grab the C++ parser
  generator_path, generator_name = gccutils.find_xml_generator()

  compiler_path = None
  if os.name == "nt":
    result = result = subprocess.run(['where', 'g++'], capture_output=True, text=True)
    if result.returncode != 0:
      raise RuntimeError("Couldn't find the path to g++. Did you follow the setup instructions?\n\nhttps://github.com/cs106l/cs106l-assignments")
    compiler_path = result.stdout.strip()
    compiler_path = f'"(" {compiler_path} -std=c++11 ")"'

  # Configure the C++ parser
  xml_generator_config = parser.xml_generator_configuration_t(
    xml_generator_path=generator_path,
    xml_generator=generator_name,
    compiler="g++",
    compiler_path=compiler_path,
    working_directory=PATH,
    ccflags="-std=c++11"
  )

  try:
    decls = parser.parse([main_cpp_path], xml_generator_config)
    global_namespace = declarations.get_global_namespace(decls)
    classes = global_namespace.classes()
  except Exception as e:
    print()
    print(e)
    print()
    print(f"{Fore.RED}{Back.YELLOW}Failed to parse main.cpp. Did you remember to recompile your code?{Style.RESET_ALL}")
    print(f"{Fore.LIGHTWHITE_EX}If your code is compiling correctly, please reach out on Ed with the error message above.{Fore.RESET}\n")
    raise Exception("Failed to parse C++ file")

  # Try to find a class inside of class.h
  def find_class_decl() -> declarations.class_t:
    cls_decl: declarations.class_t
    for cls_decl in classes:
      location: declarations.location_t = cls_decl.location
      if os.path.normpath(class_h_path) == os.path.normpath(location.file_name):
        return cls_decl
    raise Exception("Couldn't find a class inside of class.h. Did you define one?")

  global class_decl
  class_decl = find_class_decl()
  print(f"{Fore.GREEN}Autograder found class {Back.LIGHTGREEN_EX}{class_decl.name}{Back.RESET} inside class.h!{Style.RESET_ALL}")

  global definitions
  definitions = get_definitions(class_cpp_path)


def test_parameterized_constructor():
  constructors = get_decls(class_decl.constructors, "constructors")
  cons: declarations.constructor_t
  for cons in constructors:
    if cons.is_artificial:
      continue
    if cons.access_type != declarations.ACCESS_TYPES.PUBLIC:
      skip_decl(cons, "not public")
      continue
    if len(cons.arguments) == 0:
      skip_decl(cons, "has no arguments")
      continue
    
    assert_defined(cons)
    find_decl(cons)
    return

  raise RuntimeError("Could not find a public constructor taking one or more arguments")

def test_parameterless_constructor():
  constructors = get_decls(class_decl.constructors, "constructors")
  cons: declarations.constructor_t
  for cons in constructors:
    if cons.is_artificial:
      continue
    if cons.access_type != declarations.ACCESS_TYPES.PUBLIC:
      skip_decl(cons, "not public")
      continue
    if len(cons.arguments) > 0:
      skip_decl(cons, "has one or more parameters")
      continue

    assert_defined(cons)
    find_decl(cons)
    return
  
  raise RuntimeError("Could not find a public parameterless constructor")

def test_private_member_fields():
  fields = get_decls(class_decl.variables, "fields")
  field: declarations.variable_t
  for field in fields:
    if field.is_artificial:
      continue
    if field.access_type == declarations.ACCESS_TYPES.PUBLIC:
      skip_decl(field, "not private. Note: In general, it is bad practice to define public fields!")
      continue
    if field.access_type != declarations.ACCESS_TYPES.PRIVATE:
      skip_decl(field, "not private")
      continue

    find_decl(field)
    return

  raise RuntimeError("Could not find a private field")

def test_private_member_functions():
  functions = get_decls(class_decl.member_functions, "member functions")
  function: declarations.member_function_t
  for function in functions:
    if function.is_artificial:
      continue
    if function.access_type != declarations.ACCESS_TYPES.PRIVATE:
      skip_decl(function, "not private")
      continue

    find_decl(function)
    return

  raise RuntimeError("Could not find a private member function")

def get_private_fields() -> List[declarations.variable_t]:
  def is_private(field: declarations.variable_t) -> bool:
    if field.is_artificial:
      return False
    return field.access_type == declarations.ACCESS_TYPES.PRIVATE
  fields = get_decls(class_decl.variables, "fields")
  return [field for field in fields if is_private(field)]

def get_prefix_functions(prefix: str) -> List[Tuple[declarations.member_function_t, str]]:
  name_regex = re.compile(fr"{prefix}_?([a-zA-Z]\w*)")

  funcs = []
  func: declarations.member_function_t
  for func in get_decls(class_decl.member_functions, "member functions"):
    if func.is_artificial:
      continue
    if func.access_type != declarations.ACCESS_TYPES.PUBLIC:
      continue
    match = name_regex.match(func.name)
    if match is None:
      continue
    funcs.append((func, match.group(1)))
  return funcs

def find_matching_function(prefix: str):
  fields = get_private_fields()
  field_names = set(f.name for f in fields)
  funcs = get_prefix_functions("get")

  for func, field_name in funcs:
    if field_name.lower() not in field_names:
      skip_decl(func, f"{field_name} did not match a private field")
      continue

    find_decl(func)
    return func, next(f for f in fields if field_name.lower() == f.name)
  
  raise RuntimeError("No getter function found for a private field. "
    f"Options were:\n - Getters: {', '.join(p[0] for p in funcs)}"
    f"\n - Private fields: {', '.join(field_names)}")

def test_getter_function():
  function, field = find_matching_function("get")
  assert len(function.arguments) == 0, "A getter function must have no arguments"
  assert function.return_type == field.decl_type, \
    f"The return type of a getter function must match its field. Found {function.return_type} but expected {field.decl_type}"
  assert_defined(function)
  

if __name__ == "__main__":
  grader = Autograder()
  grader.setup = setup
  grader.add_part("Public parameterized constructor", test_parameterized_constructor)
  grader.add_part("Public parameterless constructor", test_parameterless_constructor)
  grader.add_part("Private field", test_private_member_fields)
  grader.add_part("Private member function", test_private_member_functions)
  grader.add_part("Public getter function", test_getter_function)
  grader.run()
