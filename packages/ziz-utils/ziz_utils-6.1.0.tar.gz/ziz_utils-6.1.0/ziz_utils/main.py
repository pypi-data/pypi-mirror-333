from os import makedirs, path, system
from sys import platform
from collections.abc import Container
import json

def isInt(input: str) -> bool:
    """
    Check if input(of type str) an integer or not. Return True if yes, else return False.
    """
    if isinstance(input, int):
        raise ValueError("Already an int.")
    validate_param(input, "input", str)
    
    try:
        int(input)
        return True
    except ValueError:
        return False

def clear():
    """
    Clear the terminal, that's all.
    """
    if platform == "win32":
        system("cls")
    else:
        system("clear")

def num_to_roman(input: int) -> str:
    """
    Convert input (of type int), into Roman numerals.
    """
    validate_param(input, "input", int)

    roman: str = ""
    number_map: dict[str, int] = {
        1000: "M", 900: "CM", 500: "D", 400: "CD",
        100: "C", 90: "XC", 50: "L", 40: "XL", 
        10: "X", 9: "IX", 5: "V", 4: "IV", 1: "I"
    }

    for value in number_map:
        while input >= value:
            roman += number_map[value]
            input -= value
    return roman

def validate_param(param: object, name: str, expected_type: type) -> None:
    """
    Checking parameter's type and raise a generic error message if type is different from what expected.

    :type param: object
    :param param: The parameter, or rather its value.

    :type name: str:
    :param name: The name of the parameter.
    
    :type expected_type: type
    :param expected_type: The expected type of param, throw an error message if this doesn't match.
    """
    if not isinstance(name, str):
        raise TypeError(f"Parameter 'expected_type' expect type type, got {type(param).__name__} instead.")
    if not isinstance(expected_type, type):
        raise TypeError(f"Parameter 'name' expect str, got {type(param).__name__} instead.")

    if not isinstance(param, expected_type):
        raise TypeError(f"Parameter '{name}' expect type {expected_type.__name__}, got {type(param).__name__} instead.")

def menu(
        config: Container,
        option_prefix: str = "",
        option_suffix: str = "",
        start: int = 1,
        trailing_dot: bool = True,
        roman_numeral_mode: bool = False
    ) -> str:
    """
    Generate the options in a menu.

    :type config: Container
    :param config: The options in the menu.

    :type option_prefix: str
    :param option_prefix: The prefix of the options. Empty by default.

    :type option_suffix: str
    :param option_suffix: The suffix of the options. Empty by default.

    :type start: int
    :param start: Accept int. Specify where to start generate a menu. Default is 1.

    :type trailing_dot: bool
    :param trailing_dot: Accept bool. Decide whether option should end with a dot. Default is True.

    :type roman_numeral_mode: bool
    :param roman_numeral_mode: Decide whether to use Roman numerals instead of integer or not. Default is False.
    """
    param_tuples: list[tuple[object, str, type]] = [
        (config, "config", Container),
        (option_prefix, "option_prefix", str),
        (option_suffix, "option_suffix", str),
        (start, "start", int),
        (trailing_dot, "trailing_dot", bool),
        (roman_numeral_mode, "roman_numeral_mode", bool),
    ]
    for i, j, k in param_tuples:
        validate_param(i, j, k)

    if isinstance(config, dict):
        config = [x for x in config.keys()]

    option_prefix = option_prefix.strip()
    option_suffix = option_suffix.strip()
    if option_prefix:
        option_prefix += " "
    if option_suffix:
        option_suffix = " " + option_suffix

    output = ""
    for i in range(start, len(config) + start):
        if not roman_numeral_mode:
            if trailing_dot:
                output += f"{i}. {option_prefix}{config[i - start]}{option_suffix}."
            else:
                output += f"{i}. {option_prefix}{config[i - start]}{option_suffix}"
        else:
            if trailing_dot:
                output += f"{num_to_roman(i)}. {option_prefix}{config[i - start]}{option_suffix}."
            else:
                output += f"{num_to_roman(i)}. {option_prefix}{config[i - start]}{option_suffix}"
        
        if i - start + 1 < len(config):
            output += "\n"
    return output

def write_config(def_config: dict, config: dict, config_folder: str, config_file_name: str, compare_keys: bool = True):
    """
    Write config to its file, automatically generate new config file (from def_config) if config doesn't exist or corrupted.

    :type def_config: dict
    :param def_config: The default config.

    :type config: dict
    :param config: The current config.

    :type config_folder: str
    :param config_folder: The path to the folder contains the config file.

    :type config_file_name: str
    :param config_file_name: The name of the config file.

    :type compare_keys: bool
    :param compare_keys: Decide whether to compare the keys of def_config and config or not, this is used for the config_manager function. Default is True.
    """
    param_tuples: list[tuple[object, str, type]] = [
        (def_config, "def_config", dict),
        (config, "config", dict),
        (config_folder, "config_folder", str),
        (config_file_name, "config_file_name", str)
    ]
    for i, j, k in param_tuples:
        validate_param(i, j, k)

    config_path = path.join(config_folder, config_file_name)
    try:
        with open(config_path, "w") as temp:
            json.dump(config, temp, ensure_ascii = False, indent = 4)
    except FileNotFoundError:
        config_manager(def_config, config_folder, config_file_name, compare_keys)
        write_config(def_config, config, config_folder, config_file_name)

def config_manager(def_config: dict, config_folder: str, config_file_name: str, compare_keys: bool = True) -> None:
    """
    Check the config file to see if it's valid or not. Create new config folder if not exist, write new config file if config doesn't exist or corrupted.

    :type def_config: dict
    :param def_config: The default config.

    :type config_folder: str
    :param config_folder: The path to the folder contains the config file.

    :type config_file_name: str
    :param config_file_name: The name of the config file.

    :type compare_keys: bool
    :param compare_keys: Decide whether to compare the keys of def_config and config or not, set to False only if every key have the same value type. Default is True.
    """
    param_tuples: list[tuple[object, str, type]] = [
        (def_config, "def_config", dict),
        (config_folder, "config_folder", str),
        (config_file_name, "config_file_name", str),
        (compare_keys, "compare_keys", bool)
    ]
    for i, j, k in param_tuples:
        validate_param(i, j, k)

    makedirs(config_folder, exist_ok=True)
    config_path = path.join(config_folder, config_file_name)

    if not path.exists(config_path):
        with open(config_path, "w") as temp:
            json.dump(def_config, temp, ensure_ascii=False, indent=4)
        return

    try:
        with open(config_path) as file:
            config: dict = json.load(file)
    except json.JSONDecodeError:
        with open(config_path, "w") as file:
            json.dump(def_config, file, ensure_ascii=False, indent=4)
        return
    
    if compare_keys:
        if def_config.keys() != config.keys():
            write_config(def_config, config, config_folder, config_file_name)
            return
    
        for key in def_config.keys():
            if isinstance(config.get(key), dict):
                config[key] = config.get(key, {})
            elif type(config.get(key)) != type(def_config[key]):
                write_config(def_config, config, config_folder, config_file_name)
                return
    else:
        temp: set[str] = {}
        temp2: set[str] = {}
        for i in config.values():
            temp.add(type(i).__name__)

        for i in def_config.values():
            temp2.add(type(i).__name__)

        if temp != temp2:
            write_config(def_config, config, config_folder, config_file_name)
            return

def is_prime(number: int) -> bool:
    """
    Check if number is a prime number or not.

    :type number: int
    :param number: The number you want to check.
    """
    validate_param(number, "number", int)
    if number <= 1:
        return False
    for i in range(2, number):
        if number % i == 0:
            return False
    return True

def first_n_primes(n: int) -> list[int]:
    """
    Return a list[int] of the first n prime number(s).

    :type n: int
    :param n: The number of prime number.
    """
    validate_param(n, "n", int)
    if n <= 0:
        raise ValueError("The amount of prime numbers cannot be equal or less than 0.")

    primes = []
    num = 2  # Start checking from the number 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes