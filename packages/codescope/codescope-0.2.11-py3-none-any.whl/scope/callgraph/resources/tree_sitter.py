EXT_TO_TREE_SITTER_LANGUAGE = {
    ".js": "tsx",
    ".jsx": "tsx",
    ".ts": "tsx",
    ".tsx": "tsx",
    ".mjs": "tsx",
    ".py": "python",
    ".rs": "rust",
    ".go": "go",
    ".java": "java",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".c": "cpp",
    ".h": "cpp",
    ".hpp": "cpp",
    ".cs": "cpp",
    ".rb": "ruby",
    # ".md": "markdown",
    # ".rst": "markdown",
    # ".txt": "markdown",
    # ".erb": "embedded-template",
    # ".ejs": "embedded-template",
    # ".html": "embedded-template",
    ".erb": "html",
    ".ejs": "html",
    ".html": "html",
    ".vue": "html",
    ".php": "php",
}

NAME_TO_TREE_SITTER_LANGUAGE = {
    "javascript": "tsx",
    "typescript": "tsx",
    "python": "python",
    "rust": "rust",
    "go": "go",
    "java": "java",
    "c": "cpp",
    "cpp": "cpp",
    "ruby": "ruby",
    "csharp": "cpp",
    "html": "html",
    "php": "php",
}

TREE_SITTER_REF_DEF_QUERIES = {
    "python": {
        "definitions": {
            # This covers both regular functions and class methods
            "function_definition": {
                "query": """
                    (function_definition name: (identifier) @definition_name)
                """,
                "output_name": "definition_name",
            },
            "class_definition": {
                "query": """
                    (class_definition name: (identifier) @definition_name)
                """,
                "output_name": "definition_name",
            },
        },
        "references": {
            # handles things like `func()`
            "call_reference": {
                "query": """
                    (call function: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            # handles things like `obj.method()`
            "call_dot_reference": {
                "query": """
                    (call 
                        function: (attribute 
                            attribute: (identifier) @reference_name))
                """,
                "output_name": "reference_name",
            },
        },
    },
    # This covers JS and TS
    "tsx": {
        "definitions": {
            # example: function oldStyleFunction(param1, param2) {}
            "function_definition": {
                "query": """
                    (function_declaration name: (identifier) @definition_name)
                """,
                "output_name": "definition_name",
            },
            # method under a class
            "method_definition": {
                "query": """
                    (method_definition name: [(property_identifier) (computed_property_name)] @method_name)
                """,
                "output_name": "method_name",
            },
            # example: class Animal {
            "class_definition": {
                "query": """
                    (class_declaration name: (identifier) @definition_name)
                """,
                "output_name": "definition_name",
            },
            # example: class Zoo<T extends Animal>
            "class_definition_with_type_identifier": {
                "query": """
                    (class_declaration name: (type_identifier) @definition_name)                
                """,
                "output_name": "definition_name",
            },
            # example: const arrowFunc = (x) => x * 2;
            "arrow_function_definition": {
                "query": """
                    (variable_declarator name: (identifier) @definition_name value: (arrow_function))
                """,
                "output_name": "definition_name",
            },
        },
        "references": {
            "function_reference": {
                "query": """
                    (call_expression function: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "method_reference": {
                "query": """
                    (call_expression function: (member_expression property: (property_identifier) @reference_name))
                """,
                "output_name": "reference_name",
            },
            "class_reference": {
                "query": """
                    (new_expression constructor: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            # covers <Test /> and <Test>...</Test>
            "jsx_component_reference": {
                "query": """
                    (jsx_self_closing_element name: (identifier) @reference_name)
                    (jsx_opening_element name: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
        },
    },
    # There are no functions in Ruby (only methods)
    "ruby": {
        "definitions": {
            "method_definition": {
                "query": """
                    (method name: (identifier) @method_name)
                """,
                "output_name": "method_name",
            },
            "singleton_method_definition": {
                "query": """
                    (singleton_method name: (identifier) @definition_name)
                """,
                "output_name": "definition_name",
            },
            "class_definition": {
                "query": """
                    (class name: [(constant) (scope_resolution)] @definition_name)
                """,
                "output_name": "definition_name",
            },
            "module_definition": {
                "query": """
                    (module name: [(constant) (scope_resolution)] @definition_name)
                """,
                "output_name": "definition_name",
            },
        },
        "references": {
            "method_reference": {
                "query": """
                    (call method: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "method_call_reference": {
                "query": """
                    (call receiver: (_) operator: ["."] method: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "class_reference": {
                "query": """
                    (call
                      receiver: (constant) @reference_name
                      method: (identifier) @method
                      (#eq? @method "new"))
                """,
                "output_name": "reference_name",
            },
        },
    },
    "rust": {
        "definitions": {
            "function_definition": {
                "query": """
                    (function_item name: (identifier) @definition_name)
                """,
                "output_name": "definition_name",
            },
            "method_definition": {
                "query": """
                    (impl_item 
                        body: (declaration_list 
                            (function_item name: (identifier) @method_name)))
                """,
                "output_name": "method_name",
            },
            "associated_function_definition": {
                "query": """
                    (impl_item
                        body: (declaration_list
                            (function_item name: (identifier) @definition_name)))
                """,
                "output_name": "definition_name",
            },
        },
        "references": {
            "function_reference": {
                "query": """
                    (call_expression function: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "method_reference": {
                "query": """
                    (call_expression 
                        function: (field_expression field: (field_identifier) @reference_name))
                """,
                "output_name": "reference_name",
            },
            "associated_function_reference": {
                "query": """
                    (call_expression
                        function: (scoped_identifier name: (identifier) @reference_name))
                """,
                "output_name": "reference_name",
            },
        },
    },
    "go": {
        "definitions": {
            "function_definition": {
                "query": """
                    (function_declaration name: (identifier) @definition_name)
                """,
                "output_name": "definition_name",
            },
            "method_definition": {
                "query": """
                    (method_declaration receiver: (parameter_list) name: (field_identifier) @method_name)
                """,
                "output_name": "method_name",
            },
        },
        "references": {
            "function_reference": {
                "query": """
                    (call_expression function: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "method_reference": {
                "query": """
                    (call_expression function: (selector_expression field: (field_identifier) @reference_name))
                """,
                "output_name": "reference_name",
            },
        },
    },
    "java": {
        "definitions": {
            "method_definition": {
                "query": """
                    (method_declaration name: (identifier) @method_name)
                """,
                "output_name": "method_name",
            },
            "constructor_definition": {
                "query": """
                    (constructor_declaration name: (identifier) @definition_name)
                """,
                "output_name": "definition_name",
            },
            "class_definition": {
                "query": """
                    (class_declaration name: (identifier) @definition_name)
                """,
                "output_name": "definition_name",
            },
            "record_definition": {
                "query": """
                    (record_declaration name: (identifier) @definition_name)
                """,
                "output_name": "definition_name",
            },
        },
        "references": {
            "method_reference": {
                "query": """
                    (method_invocation name: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "constructor_reference": {
                "query": """
                    (object_creation_expression type: (type_identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "class_reference": {
                "query": """
                    (type_identifier) @reference_name
                """,
                "output_name": "reference_name",
            },
        },
    },
    "php": {
        "definitions": {
            "function_definition": {
                "query": """
                    (function_definition name: (name) @definition_name)
                """,
                "output_name": "definition_name",
            },
            "method_definition": {
                "query": """
                    (method_declaration name: (name) @method_name)
                """,
                "output_name": "method_name",
            },
            "class_definition": {
                "query": """
                    (class_declaration name: (name) @definition_name)
                """,
                "output_name": "definition_name",
            },
            "trait_definition": {
                "query": """
                    (trait_declaration name: (name) @definition_name)
                """,
                "output_name": "definition_name",
            },
        },
        "references": {
            "function_reference": {
                "query": """
                    (function_call_expression function: (name) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "method_reference": {
                "query": """
                    (member_call_expression name: (name) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "class_reference": {
                "query": """
                    (object_creation_expression (name) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "static_method_reference": {
                "query": """
                    (scoped_call_expression scope: (name) name: (name) @reference_name)
                """,
                "output_name": "reference_name",
            },
        },
    },
    "cpp": {  # This covers both C and C++
        "definitions": {
            "function_definition": {
                "query": """
                    (function_definition
                      declarator: (function_declarator
                        declarator: (identifier) @definition_name))
                """,
                "output_name": "definition_name",
            },
            "method_definition": {
                "query": """
                    (function_definition
                      declarator: (function_declarator
                        declarator: (qualified_identifier
                          name: (identifier) @method_name)))
                """,
                "output_name": "method_name",
            },
            "class_definition": {
                "query": """
                    (class_specifier
                      name: (type_identifier) @definition_name)
                """,
                "output_name": "definition_name",
            },
            "struct_definition": {
                "query": """
                    (struct_specifier
                      name: (type_identifier) @definition_name)
                """,
                "output_name": "definition_name",
            },
        },
        "references": {
            "function_reference": {
                "query": """
                    (call_expression
                      function: (identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
            "method_reference": {
                "query": """
                    (call_expression
                      function: (field_expression
                        field: (field_identifier) @reference_name))
                """,
                "output_name": "reference_name",
            },
            "class_reference": {
                "query": """
                    (new_expression
                      type: (type_identifier) @reference_name)
                """,
                "output_name": "reference_name",
            },
        },
    },
    # "c#": {},
}
