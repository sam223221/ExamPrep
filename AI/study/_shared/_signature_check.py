"""Compare top-level def/class declarations between template and solution.

For each *_solution.py, find the corresponding template file (without _solution
suffix) and check that every top-level def and class name from the template
exists in the solution with matching parameter names and order.
"""
import ast
import os
import sys
from pathlib import Path

ROOT = Path(r"c:\Users\samgl\Documents\GitHub\ExamPrep\AI")

# Map solution -> template (some have spaces or are in different dirs)
PAIRS = [
    ("Lab1-Agents/Enums_solution.py", "Lab1-Agents/Enums.py"),
    ("Lab1-Agents/reflex_agent_with_state_solution.py", "Lab1-Agents/reflex_agent_with_state.py"),
    ("Lab1-Agents/reflex_vacuum_agent_solution.py", "Lab1-Agents/reflex_vacuum_agent.py"),
    ("Lab1-Agents/table_driven_agent_solution.py", "Lab1-Agents/table_driven_agent.py"),
    ("Lab 2/Search_solution.py", "Lab 2/Search.py"),
    ("handout/handout/alpha_beta_solution.py", "handout/handout/alpha_beta.py"),
    ("handout/handout/tictactoe_template_solution.py", "handout/handout/tictactoe_template.py"),
    ("handout_lab_4/ga_solution.py", "handout_lab_4/ga.py"),
    ("handout_lab_4/Number_solution.py", "handout_lab_4/Number.py"),
    ("handout_lab_4/Queen_solution.py", "handout_lab_4/Queen.py"),
    ("handout_lab_4/queens_fitness_solution.py", "handout_lab_4/queens_fitness.py"),
    ("lab6/Colors_solution.py", "lab6/Colors.py"),
    ("lab6/States_solution.py", "lab6/States.py"),
    ("lab6/constraints_template_solution.py", "lab6/constraints_template.py"),
    ("Lab7/handout/bn_solution.py", "Lab7/handout/bn.py"),
    ("Lab7/handout/Runner_solution.py", "Lab7/handout/Runner.py"),
    ("Lab7/handout/Variable_solution.py", "Lab7/handout/Variable.py"),
    ("Lab 8/handout/hidden_markov_models_solution.py", "Lab 8/handout/hidden_markov_models.py"),
]


def collect_signatures(path: Path):
    """Return dict { name -> (kind, [param_names]) } for top-level def and class."""
    src = path.read_text(encoding="utf-8", errors="replace")
    tree = ast.parse(src)
    sigs = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            params = [a.arg for a in node.args.args]
            # posonly + kwonly
            posonly = [a.arg for a in node.args.posonlyargs]
            kwonly = [a.arg for a in node.args.kwonlyargs]
            full = posonly + params + kwonly
            sigs[node.name] = ("def", full)
        elif isinstance(node, ast.ClassDef):
            # also collect __init__ signature if present
            init_params = None
            for m in node.body:
                if isinstance(m, ast.FunctionDef) and m.name == "__init__":
                    init_params = [a.arg for a in m.args.args]
            sigs[node.name] = ("class", init_params)
    return sigs


def main():
    results = []
    for sol_rel, tpl_rel in PAIRS:
        sol = ROOT / sol_rel
        tpl = ROOT / tpl_rel
        if not sol.exists():
            results.append(("MISSING_SOL", sol_rel, tpl_rel, f"solution file missing"))
            continue
        if not tpl.exists():
            results.append(("MISSING_TPL", sol_rel, tpl_rel, f"template file missing"))
            continue
        try:
            tpl_sigs = collect_signatures(tpl)
            sol_sigs = collect_signatures(sol)
        except SyntaxError as e:
            results.append(("PARSE_ERR", sol_rel, tpl_rel, str(e)))
            continue

        problems = []
        for name, (kind, params) in tpl_sigs.items():
            if name not in sol_sigs:
                problems.append(f"  MISSING in solution: {kind} {name}({params})")
                continue
            sol_kind, sol_params = sol_sigs[name]
            if sol_kind != kind:
                problems.append(f"  KIND CHANGED: {name} template={kind} solution={sol_kind}")
                continue
            if params is None or sol_params is None:
                # class with no __init__ on one side - skip
                continue
            if params != sol_params:
                problems.append(f"  PARAM MISMATCH: {kind} {name}: template={params} solution={sol_params}")
        status = "PASS" if not problems else "FAIL"
        results.append((status, sol_rel, tpl_rel, "\n".join(problems) if problems else "ok"))

    # Print
    fails = 0
    for status, sol, tpl, info in results:
        if status == "PASS":
            print(f"[PASS] {sol}  vs  {tpl}")
        else:
            fails += 1
            print(f"[{status}] {sol}  vs  {tpl}")
            for line in info.splitlines():
                print(line)
    print()
    print(f"Total pairs: {len(results)}, FAILs: {fails}")
    sys.exit(0 if fails == 0 else 1)


if __name__ == "__main__":
    main()
