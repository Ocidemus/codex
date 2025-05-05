import ast
import graphviz
import os
from typing import Dict, List, Tuple

class CodeAnalyzer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tree = ast.parse(source_code)
        self.functions: Dict[str, Dict[str, any]] = {}
        self.classes: Dict[str, Dict[str, any]] = {}
        self.analyze_code()

    def analyze_code(self):
        class Visitor(ast.NodeVisitor):
            def __init__(self, analyzer):
                self.analyzer = analyzer
                self.current_scope = None
                self.node_counter = 0
                self.prev_nodes: List[str] = []

            def _new_node_id(self):
                self.node_counter += 1
                return f"{self.current_scope}_{self.node_counter}"

            def visit_ClassDef(self, node):
                self.current_scope = node.name
                self.analyzer.classes[node.name] = {"methods": {}}
                self.prev_nodes = []
                self.generic_visit(node)
                self.current_scope = None

            def visit_FunctionDef(self, node):
                scope = self.current_scope if self.current_scope else node.name
                self.current_scope = f"{scope}.{node.name}" if self.current_scope else node.name
                self.prev_nodes = []
                target_dict = (self.analyzer.classes[scope]["methods"]
                             if scope in self.analyzer.classes
                             else self.analyzer.functions)
                target_dict[node.name] = {
                    "calls": set(),
                    "nodes": {},
                    "edges": [],
                    "returns": set()
                }
                entry_id = self._new_node_id()
                target_dict[node.name]["nodes"][entry_id] = {
                    "type": "entry",
                    "label": f"Enter {node.name}()"
                }
                self.prev_nodes = [entry_id]
                self.generic_visit(node)
                self.current_scope = scope.split('.')[0] if '.' in scope else None

            def visit_Assign(self, node):
                if self.current_scope:
                    node_id = self._new_node_id()
                    target = ast.unparse(node.targets[0]).strip()
                    value = ast.unparse(node.value).strip()
                    label = f"{target} = {value}" if len(value) < 20 else f"{target} = ..."
                    target_dict = (self.analyzer.classes[self.current_scope.split('.')[0]]["methods"]
                                 [self.current_scope.split('.')[1]]
                                 if '.' in self.current_scope
                                 else self.analyzer.functions[self.current_scope])
                    target_dict["nodes"][node_id] = {"type": "assign", "label": label}
                    for prev in self.prev_nodes:
                        target_dict["edges"].append((prev, node_id, "next"))
                    self.prev_nodes = [node_id]
                self.generic_visit(node)

            def visit_Call(self, node):
                if self.current_scope and isinstance(node.func, ast.Name):
                    called_func = node.func.id
                    target_dict = (self.analyzer.classes[self.current_scope.split('.')[0]]["methods"]
                                 [self.current_scope.split('.')[1]]
                                 if '.' in self.current_scope
                                 else self.analyzer.functions[self.current_scope])
                    target_dict["calls"].add(called_func)
                    node_id = self._new_node_id()
                    args = ", ".join(ast.unparse(arg).strip() for arg in node.args)
                    label = f"{called_func}({args})" if len(args) < 20 else f"{called_func}(...)"
                    target_dict["nodes"][node_id] = {"type": "call", "label": label}
                    for prev in self.prev_nodes:
                        target_dict["edges"].append((prev, node_id, "call"))
                    self.prev_nodes = [node_id]
                self.generic_visit(node)

            def visit_While(self, node):
                if self.current_scope:
                    node_id = self._new_node_id()
                    condition = ast.unparse(node.test).strip()
                    target_dict = (self.analyzer.classes[self.current_scope.split('.')[0]]["methods"]
                                 [self.current_scope.split('.')[1]]
                                 if '.' in self.current_scope
                                 else self.analyzer.functions[self.current_scope])
                    target_dict["nodes"][node_id] = {"type": "while", "label": f"While {condition}"}
                    for prev in self.prev_nodes:
                        target_dict["edges"].append((prev, node_id, "start"))
                    self.prev_nodes = [node_id]
                    # Visit each statement in the body
                    for stmt in node.body:
                        self.visit(stmt)
                    loop_end = self.prev_nodes
                    for end in loop_end:
                        target_dict["edges"].append((end, node_id, "loop"))
                    merge_id = self._new_node_id()
                    target_dict["nodes"][merge_id] = {"type": "merge", "label": "End Loop"}
                    target_dict["edges"].append((node_id, merge_id, "exit"))
                    self.prev_nodes = [merge_id]

            def visit_If(self, node):
                if self.current_scope:
                    node_id = self._new_node_id()
                    condition = ast.unparse(node.test).strip()
                    target_dict = (self.analyzer.classes[self.current_scope.split('.')[0]]["methods"]
                                 [self.current_scope.split('.')[1]]
                                 if '.' in self.current_scope
                                 else self.analyzer.functions[self.current_scope])
                    target_dict["nodes"][node_id] = {"type": "if", "label": f"If {condition}"}
                    for prev in self.prev_nodes:
                        target_dict["edges"].append((prev, node_id, "condition"))
                    self.prev_nodes = [node_id]
                    if_start = self.prev_nodes
                    # Visit each statement in the body
                    for stmt in node.body:
                        self.visit(stmt)
                    if_end = self.prev_nodes
                    else_end = None
                    if node.orelse:
                        self.prev_nodes = [node_id]
                        # Visit each statement in the else branch
                        for stmt in node.orelse:
                            self.visit(stmt)
                        else_end = self.prev_nodes
                    merge_id = self._new_node_id()
                    target_dict["nodes"][merge_id] = {"type": "merge", "label": "Merge"}
                    for end in if_end:
                        target_dict["edges"].append((end, merge_id, "then"))
                    if else_end:
                        for end in else_end:
                            target_dict["edges"].append((end, merge_id, "else"))
                    else:
                        target_dict["edges"].append((node_id, merge_id, "else"))
                    self.prev_nodes = [merge_id]

            def visit_Return(self, node):
                if self.current_scope:
                    node_id = self._new_node_id()
                    return_val = ast.unparse(node.value).strip() if node.value else "None"
                    target_dict = (self.analyzer.classes[self.current_scope.split('.')[0]]["methods"]
                                 [self.current_scope.split('.')[1]]
                                 if '.' in self.current_scope
                                 else self.analyzer.functions[self.current_scope])
                    target_dict["nodes"][node_id] = {"type": "return", "label": f"Return {return_val}"}
                    for prev in self.prev_nodes:
                        target_dict["edges"].append((prev, node_id, "return"))
                    target_dict["returns"].add(node_id)
                    self.prev_nodes = [node_id]

        visitor = Visitor(self)
        visitor.visit(self.tree)

    def generate_flowchart(self, output_file="Flowchart"):
        dot = graphviz.Digraph(comment="Code Flowchart")
        dot.attr(rankdir="TB", nodesep="0.5", ranksep="1.2", dpi="300", bgcolor="white")

        for func, details in self.functions.items():
            with dot.subgraph(name=f'cluster_{func}') as sub:
                sub.attr(label=f"Function: {func}()", style='filled', color='lightgrey')
                self._render_subgraph(sub, details)

        for class_name, class_details in self.classes.items():
            with dot.subgraph(name=f'cluster_{class_name}') as sub:
                sub.attr(label=f"Class: {class_name}", style='filled', color='lightblue')
                for method_name, details in class_details["methods"].items():
                    with sub.subgraph(name=f'cluster_{class_name}_{method_name}') as method_sub:
                        method_sub.attr(label=f"Method: {method_name}()", style='filled', color='lightgrey')
                        self._render_subgraph(method_sub, details)

        output_dir = r"S:\minor2\ai-doc-generator\frontend\public\images"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_file)

        try:
            dot.render(output_path, format="png", cleanup=True)
            print(f"✅ Flowchart saved at {output_path}.png")
        except graphviz.backend.execute.CalledProcessError as e:
            print(f"❌ Error rendering flowchart: {e}")
            print("DOT source:\n", dot.source)
            raise


    def _render_subgraph(self, sub, details):
        for node_id, info in details["nodes"].items():
            shape = {
                "entry": "oval", "if": "diamond", "while": "hexagon",
                "assign": "box", "call": "box", "return": "parallelogram", "merge": "point"
            }.get(info["type"], "ellipse")
            color = {
                "entry": "lightblue", "if": "moccasin", "while": "lightyellow",
                "assign": "lightcyan", "call": "lightgreen", "return": "pink", "merge": "gray"
            }.get(info["type"], "white")
            label = f"[{node_id.split('_')[-1]}] {info['label']}" if info["type"] != "merge" else info["label"]
            sub.node(node_id, label=label, shape=shape, style="filled", fillcolor=color,
                    fontname="Arial", fontsize="10")

        for start, end, label in details["edges"]:
            edge_attrs = {"arrowhead": "vee", "fontname": "Arial", "fontsize": "8"}
            if label == "loop":
                edge_attrs.update({"label": "Loop", "color": "red", "style": "dashed"})
            elif label == "condition":
                edge_attrs.update({"label": "Yes"})
            elif label == "else":
                edge_attrs.update({"label": "No", "color": "purple"})
            elif label == "then" or label == "return":
                edge_attrs.update({"color": "blue"})
            elif label == "call":
                edge_attrs.update({"label": "Call"})
            sub.edge(start, end, **edge_attrs)

        for callee in details["calls"]:
            if callee not in self.functions and not any(callee in c["methods"] for c in self.classes.values()):
                sub.node(callee, shape="box", style="rounded,filled", fillcolor="lightgreen",
                        label=f"{callee}()", fontname="Arial", fontsize="10")

# if __name__ == "__main__":
#     sample_code = """
# def abcd_sort(arr):
#     n = len(arr)
#     for i in range(n):
#         for j in range(n - i - 1):
#             if arr[j] > arr[j + 1]:
#                 arr[j], arr[j + 1] = arr[j + 1], arr[j]

# arr = [64, 34, 25, 12, 22, 11, 90]
# abcd_sort(arr)
# print(arr)
# """
    # analyzer = CodeAnalyzer(sample_code)
    # analyzer.generate_flowchart("flowchart")