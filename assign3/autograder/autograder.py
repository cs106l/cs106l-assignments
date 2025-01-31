from typing import Callable, List, Set, Tuple, TypeVar
from utils import Autograder, get_declarations, install_castxml
install_castxml()

import os
import re

from pygccxml import declarations
from colorama import Fore, Style, Back

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
AUTOGRADER_DIR = os.path.join(PATH, "autograder")

class_decl: declarations.class_t = None
definitions: Set[Tuple[str, str]] = None


def norm_path(path: os.PathLike) -> os.PathLike:
    return os.path.normpath(os.path.relpath(path, os.getcwd()))


def get_definitions(source_file: os.PathLike) -> Set[Tuple[str, str]]:
    if not os.path.exists(source_file):
        raise RuntimeError(f"Could not find source file: {source_file}")

    with open(source_file, "r") as file:
        content = file.read()

    comment_pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    regex = re.compile(comment_pattern, re.MULTILINE | re.DOTALL)
    content = regex.sub(
        lambda match: "" if match.group(2) is not None else match.group(1), content
    )

    string_pattern = r"\".*?\""
    regex = re.compile(string_pattern, re.MULTILINE | re.DOTALL)
    content = regex.sub("", content)

    def remove_nested_braces(content):
        result, stack = [], []
        for char in content:
            if char == "{":
                stack.append("{")
            elif char == "}":
                stack.pop() if stack else None
            elif not stack:
                result.append(char)
        return "".join(result)

    content = remove_nested_braces(content)

    definition_pattern = r"(\w+)(?:<.*>)?::(\w+)"
    regex = re.compile(definition_pattern)
    matches = regex.findall(content)

    return matches


def assert_defined(decl: declarations.declarated_t):
    class_name = class_decl.name
    class_name = re.sub(r"<.*>", "", class_name)

    decl_name: str = None
    if isinstance(decl, declarations.constructor_t):
        decl_name = decl.name
    elif isinstance(decl, declarations.member_function_t):
        decl_name = decl.name
    else:
        raise RuntimeError(
            f"Unhandled declaration type: {type(decl)}. Please reach out on Ed!"
        )

    decl_tuple = (class_name, decl_name)
    if decl_tuple not in definitions:
        raise RuntimeError(
            f"Found declaration for {decl}, but could not find a matching definition in class.cpp"
        )


def skip_decl(decl: declarations.declaration_t, reason: str):
    print(f"⏩ Disregarding {decl}, {reason}")


def find_decl(decl: declarations.declaration_t):
    print(f"🔍 Found {decl}!")


T = TypeVar("T")


def get_decls(getter: Callable[[], T], kind_plural: str, scope: str = "class") -> T:
    try:
        return getter()
    except RuntimeError as err:
        if "query returned 0 declarations" in str(err):
            raise RuntimeError(f"Could not find any {kind_plural} in {scope}")


def setup():
    sandbox_cpp_path = os.path.join(PATH, "sandbox.cpp")
    class_h_path = os.path.join(PATH, "class.h")
    class_cpp_path = os.path.join(PATH, "class.cpp")

    if not os.path.isfile(sandbox_cpp_path):
        raise RuntimeError(
            "Couldn't find '{main.cpp}'. Did you delete it from the starter code?"
        )
    
    decls = get_declarations(norm_path(sandbox_cpp_path))
    global_namespace = declarations.get_global_namespace(decls)

    # Try to find a class inside of class.h
    def find_class_decl() -> declarations.class_t:
        try:
            classes = global_namespace.classes()
        except:
            classes = []
        cls_decl: declarations.class_t
        for cls_decl in classes:
            location: declarations.location_t = cls_decl.location
            if norm_path(class_h_path) == norm_path(location.file_name):
                return cls_decl
        raise Exception(
            "Couldn't find a class inside of class.h. Possible reasons:\n"
            " - Did you define one?\n"
            ' - Did you #include "class.h" inside main.cpp?\n'
            " - Did you construct an instance of the class inside main.cpp?"
        )

    global class_decl
    class_decl = find_class_decl()
    print(
        f"{Fore.GREEN}Autograder found class {Back.LIGHTGREEN_EX}{class_decl.name}{Back.RESET} inside class.h!{Style.RESET_ALL}"
    )

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

    raise RuntimeError(
        "Could not find a public constructor taking one or more arguments"
    )


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
        if field.type_qualifiers.has_static:
            skip_decl(field, "marked static")
            continue
        if field.type_qualifiers.has_extern:
            skip_decl(field, "marked extern")
            continue
        if field.access_type == declarations.ACCESS_TYPES.PUBLIC:
            skip_decl(
                field,
                "not private. Note: In general, it is bad practice to define public fields!",
            )
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
        if function.has_static:
            skip_decl(function, "marked static")
            continue
        if function.has_extern:
            skip_decl(function, "marked extern")
            continue
        if function.access_type != declarations.ACCESS_TYPES.PRIVATE:
            skip_decl(function, "not private")
            continue

        find_decl(function)
        assert_defined(function)
        return

    raise RuntimeError("Could not find a private member function")


def get_private_fields() -> List[declarations.variable_t]:
    def is_private(field: declarations.variable_t) -> bool:
        if field.is_artificial:
            return False
        if field.type_qualifiers.has_static:
            return False
        if field.type_qualifiers.has_extern:
            return False
        return field.access_type == declarations.ACCESS_TYPES.PRIVATE

    fields = get_decls(class_decl.variables, "fields")
    return [field for field in fields if is_private(field)]


def get_prefix_functions(
    prefix: str,
) -> List[Tuple[declarations.member_function_t, str]]:
    name_regex = re.compile(rf"{prefix}_?([a-zA-Z]\w*)")

    funcs = []
    func: declarations.member_function_t
    for func in get_decls(class_decl.member_functions, "member functions"):
        if func.is_artificial:
            continue
        if func.has_static:
            continue
        if func.has_extern:
            continue
        if func.access_type != declarations.ACCESS_TYPES.PUBLIC:
            continue
        match = name_regex.match(func.name)
        if match is None:
            continue
        funcs.append((func, match.group(1)))
    return funcs


def find_matching_function(prefix: str, type: str):
    fields = get_private_fields()
    field_names = {f.name.lower().strip("_"): f for f in fields}
    funcs = get_prefix_functions(prefix)

    for func, field_name in funcs:
        field_name_lower = field_name.lower()
        if field_name_lower not in field_names:
            skip_decl(func, f"{field_name} did not match a private field")
            continue

        find_decl(func)
        return func, field_names[field_name_lower]

    raise RuntimeError(
        f"No {type} function found for a private field. "
        f"Options were:\n - {type.title()}s: [{', '.join(p[0].name for p in funcs)}]"
        f"\n - Private fields: [{', '.join(f.name for f in fields)}]"
    )


def test_getter_function():
    function, field = find_matching_function("get", "getter")
    assert len(function.arguments) == 0, "A getter function must have no arguments"
    assert (
        function.return_type == field.decl_type
    ), f"The return type of a getter function must match its field. Found {function.return_type} but expected {field.decl_type}"
    assert (
        function.has_const
    ), "A getter function should be marked as const (refer to Thursday's lecture on const correctness)"
    assert_defined(function)


def test_setter_function():
    function, field = find_matching_function("set", "setter")
    assert (
        len(function.arguments) == 1
    ), "A setter should have a single argument matching the type of its field"

    assert declarations.base_type(function.argument_types[0]) == declarations.base_type(
        field.decl_type
    ), (
        f"The argument of a setter should be the type of its field. "
        f"Found {function.argument_types[0]} but expected {field.decl_type}"
    )
    assert (
        function.return_type == declarations.void_t()
    ), "A setter should have a void return type"
    assert_defined(function)


if __name__ == "__main__":
    grader = Autograder()
    grader.setup = setup
    grader.add_part(
        "#1 / Public parameterized constructor", test_parameterized_constructor
    )
    grader.add_part(
        "#2 / Public parameterless constructor", test_parameterless_constructor
    )
    grader.add_part("#3 / Private field", test_private_member_fields)
    grader.add_part("#4 / Private member function", test_private_member_functions)
    grader.add_part("#5 / Public getter function", test_getter_function)
    grader.add_part("#6 / Public setter function", test_setter_function)
    grader.run()
