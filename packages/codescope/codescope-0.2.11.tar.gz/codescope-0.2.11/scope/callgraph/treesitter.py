# Standard library
from typing import List, Tuple, Dict
from collections import defaultdict

# Local
from scope import RepoFile
from scope.callgraph.resources.tree_sitter import (
    TREE_SITTER_REF_DEF_QUERIES,
    EXT_TO_TREE_SITTER_LANGUAGE,
)

# Third party
from tree_sitter import Language, Parser, Tree
from tree_sitter_languages import get_parser, get_language


class ASTSearch:
    def __init__(self, files: List[RepoFile], debug=False):
        self.files = files
        self.ext_set = set(file.ext for file in files)
        self.ext_to_sitter_language: Dict[str, Language] = {}
        self.ext_to_parser: Dict[str, Parser] = {}
        self.valid_ident_types = {"definitions", "references"}
        self.trees: Dict[str, Tree] = {}
        self._setup_parsers()
        self._setup_trees()

        # Debugging
        self.matched_node_names = {}
        self.errors = {}

    def _setup_parsers(self):
        for ext in self.ext_set:
            lang = EXT_TO_TREE_SITTER_LANGUAGE.get(ext)
            if lang is None:
                continue
            parser_language = get_language(lang)
            self.ext_to_sitter_language[ext] = parser_language
            parser = get_parser(lang)
            self.ext_to_parser[ext] = parser

    def _setup_trees(self):
        files_to_remove = []
        for file in self.files:
            parser = self.ext_to_parser.get(file.ext)
            if parser is None:
                files_to_remove.append(file.abs_path)
                continue
            file_content = file.content.encode()
            self.trees[file.name] = parser.parse(file_content)

        _files = [file for file in self.files if file.abs_path not in files_to_remove]
        self.files = _files

    def _search_file(
        self, file: RepoFile, identifier: str, ident_type: str, log=False
    ) -> List[Tuple[int, int]]:
        tree = self.trees.get(file.name)
        parser_language = self.ext_to_sitter_language.get(file.ext)
        queries = TREE_SITTER_REF_DEF_QUERIES.get(parser_language, {}).get(
            ident_type, []
        )
        self.matched_node_names[file.relative_path] = {}
        self.errors[file.relative_path] = []

        ranges = set()
        for query in queries:
            ref_query = queries[query]["query"]
            output_name = queries[query]["output_name"]
            function_references_query = parser_language.query(ref_query)
            reference_matches = function_references_query.matches(tree.root_node)

            for match in reference_matches:
                try:
                    node = match[1][output_name]
                    node_name = node.text.decode("utf-8")
                    self.matched_node_names[file.relative_path][output_name].append(
                        node_name
                    )
                    if node_name == identifier:
                        start_line, start_col = node.start_point
                        end_line, end_col = node.end_point
                        if start_line is not None and end_line is not None:
                            ranges.add((start_line, end_line))
                except Exception as e:
                    err = []
                    err.append(
                        f"query_file_code_tree({ident_type}, lang:{file.ext}) ERROR with match, so continuing"
                    )
                    err.append(
                        f"query_file_code_tree({ident_type}, lang:{file.ext}): ERROR: {str(e)}"
                    )
                    err.append(f"MATCH: {match}")
                    self.errors[file.relative_path].append(err)
                    continue
            if log:
                print("TS QUERY: ", query)
                print(
                    f"MATCHED NODE NAMES: {self.matched_node_names[file.relative_path]}"
                )

        return list(ranges)

    def search(
        self, identifier: str, ident_type: str, log=False
    ) -> Dict[str, List[List[int]]]:
        if ident_type not in self.valid_ident_types:
            raise ValueError(f"Invalid identifier type: {ident_type}")
        ranges = {}
        for file in self.files:
            ranges[file.relative_path] = self._search_file(
                file, identifier, ident_type, log
            )
        return ranges

    def bulk_search(
        self, identifiers: List[str], ident_type: str, log=False
    ) -> Dict[str, Dict[str, List[Tuple[int, int]]]]:
        searched = {}
        for identifier in identifiers:
            searched[identifier] = self.search(identifier, ident_type, log)
        return searched


def search_file(
    file: RepoFile, identifier: str, ident_type: str, log=False
) -> Tuple[List[List[int]], List[str]]:
    if ident_type not in ["definitions", "references"]:
        raise ValueError(f"Invalid identifier type: {ident_type}")

    file_ext = file.ext
    lang = EXT_TO_TREE_SITTER_LANGUAGE.get(file_ext, None)

    if lang is None:
        if log:
            print(
                f"query_file_code_tree({ident_type}) ERROR with language, so returning []"
            )
        return [], []

    parser_language = get_language(lang)
    parser = get_parser(lang)
    tree = parser.parse(file.content.encode())

    ranges, matched_node_names, errors = [], defaultdict(list), []
    queries = TREE_SITTER_REF_DEF_QUERIES.get(lang, {}).get(ident_type, [])

    # If matches any of function_reference, method_reference, or class_reference, get the line range
    if log:
        print(f"FILE {file.name} EXT: {file_ext} TS LANG: {lang}")
    for query in queries:
        if log:
            print("------------------------------------------")
        try:
            ref_query = queries[query]["query"]
            output_name = queries[query]["output_name"]
            # print(f"REF QUERY: {ref_query}")
            # print(f"OUTPUT NAME: {output_name}")
            function_references_query = parser_language.query(ref_query)
            reference_matches = function_references_query.matches(tree.root_node)
            for match in reference_matches:
                try:
                    node = match[1][output_name]
                    node_name = node.text.decode("utf-8")
                    matched_node_names[output_name].append(node_name)
                    if node_name == identifier:
                        start_line, start_col = node.start_point
                        end_line, end_col = node.end_point
                        if start_line is not None and end_line is not None:
                            ranges.append((start_line, end_line))
                except Exception as e:
                    err = []
                    err.append(
                        f"query_file_code_tree({ident_type}, lang:{lang}) ERROR with match, so continuing"
                    )
                    err.append(
                        f"query_file_code_tree({ident_type}, lang:{lang}): ERROR: {str(e)}"
                    )
                    err.append(f"MATCH: {match}")
                    errors.append(err)
                    continue
            if log:
                print("TS QUERY: ", query)
                print(f"MATCHED NODE NAMES: {matched_node_names}")
        except Exception as e:
            err = []
            err.append(
                f"query_file_code_tree({ident_type}, lang:{lang}, query_name:{query}) ERROR with query, so returning []"
            )
            err.append(
                f"query_file_code_tree({ident_type}, lang:{lang}): ERROR: {str(e)}"
            )
            errors.append(err)
            continue
        if log:
            print("------------------------------------------")

    return list(set(ranges)), dict(matched_node_names), errors
