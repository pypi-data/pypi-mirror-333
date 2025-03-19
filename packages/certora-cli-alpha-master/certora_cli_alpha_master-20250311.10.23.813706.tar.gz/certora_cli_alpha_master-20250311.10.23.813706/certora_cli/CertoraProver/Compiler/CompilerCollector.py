#     The Certora Prover
#     Copyright (C) 2025  Certora Ltd.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, version 3 of the License.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

from abc import abstractmethod, ABC
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set
from Shared.certoraUtils import AbstractAndSingleton, CompilerVersion
from CertoraProver.certoraContractFuncs import SourceBytes
import CertoraProver.certoraType as CT


# TODO: merge this with Func in certoraBuild
@dataclass
class CompilerLangFunc:
    name: str
    fullArgs: List[CT.TypeInstance]
    paramNames: List[str]
    returns: List[CT.TypeInstance]
    sighash: str
    notpayable: bool
    fromLib: bool  # not serialized
    isConstructor: bool  # not serialized
    stateMutability: str
    visibility: str
    implemented: bool  # does this function have a body? (false for interface functions)
    overrides: bool  # does this function override an interface declaration or super-contract definition?
    contractName: str
    source_bytes: Optional[SourceBytes]
    ast_id: Optional[int] = None
    original_file: Optional[str] = None
    body_location: Optional[str] = None


class CompilerLang(metaclass=AbstractAndSingleton):
    """
    This class represents the compiler-language property attached to [CompilerCollector].
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def compiler_name(self) -> str:
        pass

    @staticmethod
    def normalize_func_hash(func_hash: str) -> str:
        """
        Normalizes the hash [func_hash] (first 4 bites in a function's signature).
        """
        return func_hash

    @staticmethod
    def normalize_file_compiler_path_name(file_abs_path: str) -> str:
        """
        Normalizes the absolute path name [file_abs_path] of a file, given to the compiler.
        """
        return file_abs_path

    @staticmethod
    def normalize_deployed_bytecode(deployed_bytecode: str) -> str:
        """
        Normalizes the deployed bytecode [deployed_bytecode].
        """
        return deployed_bytecode

    @staticmethod
    @abstractmethod
    def get_contract_def_node_ref(contract_file_ast: Dict[int, Any], contract_file: str, contract_name: str) -> \
            int:
        """
        Given the AST [contract_file_ast], the contract-file [contract_file] and the contract [contract_name] inside
        [contract_file], returns the (expected to be single) definition node reference for [contract_name] which is
        located inside [contract_file_ast].
        """
        pass

    @staticmethod
    @abstractmethod
    def compilation_output_path(sdc_name: str) -> Path:
        """
        Returns the path to the output file generated by the compiler for [sdc_name],
        using the given config path [config_path]. If several output files are generated by the compiler, returns the
        one that stores stdout.
        """
        pass

    @staticmethod
    @abstractmethod
    def all_compilation_artifacts(sdc_name: str) -> Set[Path]:
        """
        Returns the set of paths for all files generated after compilation.
        """
        pass

    @staticmethod
    def collect_storage_layout_info(file_abs_path: str,
                                    config_path: Path,
                                    compiler_cmd: str,
                                    compiler_version: Optional[CompilerVersion],
                                    data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns the data dictionary of the contract with storage layout information if needed
        """
        return data

    @staticmethod
    @abstractmethod
    def get_supports_imports() -> bool:
        """
        Returns True if the language supports imports, False otherwise
        """
        pass

    @staticmethod
    @abstractmethod
    def collect_source_type_descriptions_and_funcs(asts: Dict[str, Dict[str, Dict[int, Any]]],
                                                   data: Dict[str, Any],
                                                   contract_file: str,
                                                   contract_name: str,
                                                   build_arg_contract_file: str) -> \
            Tuple[List[CT.Type], List[CompilerLangFunc]]:
        """
        :return: `(types, funcs)` where `types` contains the user-defined types that are declared in the contract,
          and `funcs` contains descriptors for the internal and external functions defined in the contract
        :param asts: A flattened mapping filename -> contract name -> node ID -> AST node
        :param data: The original standard JSON output from the underlying compiler
        :param contract_file: ?
        :param contract_name:
        :param build_arg_contract_file: ?
        TODO: presumably one of these files is the original file, and the other is the munged file, but I'm not sure
          which is which
        """
        pass

    @property
    @abstractmethod
    def supports_typed_immutables(self) -> bool:
        """
        :return: True if has type information associated to immutables
        """
        pass

    @property
    @abstractmethod
    def supports_ast_output(self) -> bool:
        """
        :return: True if compiling contracts in this language produces AST output
        """
        pass

    @property
    @abstractmethod
    def supports_srclist_output(self) -> bool:
        """
        :return: True if compiling contracts in this language produces srclist output
        """
        pass


class CompilerCollector(ABC):
    """
    This class incorporates all the compiler settings.
    Compiler-settings related computations should be done here.
    """

    @property
    @abstractmethod
    def compiler_name(self) -> str:
        pass

    @property
    @abstractmethod
    def smart_contract_lang(self) -> CompilerLang:
        pass

    @property
    @abstractmethod
    def compiler_version(self) -> CompilerVersion:
        pass

    def __str__(self) -> str:
        return f"{self.compiler_name} {self.compiler_version}"
