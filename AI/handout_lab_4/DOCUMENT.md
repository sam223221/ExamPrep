# `handout_lab_4/` — Lab 4 (Genetic Algorithm) handout + solutions

Lab 4 from the AI exam prep package. The handout files (`ga.py`, `Queen.py`, `Number.py`, `queens_fitness.py`) are the original course templates with `# TODO` stubs. The `*_solution.py` siblings are the worked answers.

## Files

| File | Role | Entry point? |
|---|---|---|
| `Lab 4.pdf` | Original handout PDF (problem statement). | No (reference) |
| `ga.py` | Template GA driver — `genetic_algorithm`, `Individual` ABC, `random_selection`, `pick_individual`, helpers. | No (imported) |
| `ga_solution.py` | Worked solution for the GA driver — adds `roulette_wheel_select`, μ+λ option, knob block. Re-exposes the template's top-level callables and parameter names. | Yes (`py -3.12 ga_solution.py` runs both Number and Queens demos) |
| `Number.py` | Template Number-individual class with bitstring representation. | No |
| `Number_solution.py` | Worked Number solution. Imports `ga_solution.genetic_algorithm`. | Yes (`py -3.12 Number_solution.py`) |
| `Queen.py` | Template N-Queens Board class. Defines `Board`, `get_initial_population`, **`test()`** (smoke test stub), `main()`. | Yes (template — but raises) |
| `Queen_solution.py` | Worked N-Queens solution. Preserves the template's top-level callables: `Board`, `get_initial_population`, **`test()`**, `main()`. | Yes (`py -3.12 Queen_solution.py`) |
| `queens_fitness.py` | Template fitness functions — `fitness_fn_negative(board_view)`, `fitness_fn_positive(state)`. | No |
| `queens_fitness_solution.py` | Worked + extended fitness functions — `fitness_fn_negative`, `fitness_fn_positive(state)` (signature matches template), `fitness_fn_weighted`. | No |

## Signature contract with templates

Per the verifier (Phase 3.3) the `*_solution.py` files must preserve every public function signature from their template sibling, since exam rubrics and IDE renames may rely on them. Specifically:

- `ga_solution.genetic_algorithm(...)` exposes the kwarg **`should_trim_population`** (matches `ga.py`). The solution adds one *new* kwarg (`use_mu_plus_lambda`) — additive, no renames.
- `Queen_solution.test()` exists at module level (matches `Queen.py`'s smoke-test stub). It constructs `Board((1, 2, 3, 4, 5, 6, 7, 8))` and prints its fitness.
- `queens_fitness_solution.fitness_fn_positive(state)` — parameter named `state`, matching `queens_fitness.py`.

## Recent changes

- **2026-05-23 (Phase 3.3 targeted fix):**
  - `ga_solution.py`: renamed `genetic_algorithm(..., trim_population_flag=...)` back to `should_trim_population` to match the template; updated both call sites (`_run_number_demo`, `_run_queens_demo`).
  - `Number_solution.py`: updated the `genetic_algorithm` kwarg name accordingly.
  - `Queen_solution.py`: updated the `genetic_algorithm` kwarg name; **re-added the top-level `def test()` smoke-test stub** (was missing).
  - `queens_fitness_solution.py`: renamed `fitness_fn_positive(board_view)` parameter to `state` per the template signature.
  - Verified all three entry points still run end-to-end with the original outputs.
