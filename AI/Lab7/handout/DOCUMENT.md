# `Lab7/handout/` — Lab 7 (Bayesian Networks) handout + solutions

Lab 7 from the AI exam prep package. The handout files (`Variable.py`, `bn.py`, `Runner.py`) are the original course templates with `# TODO` stubs. The `*_solution.py` siblings are the worked answers.

## Files

| File | Role | Entry point? |
|---|---|---|
| `Lab 7.pdf` | Original handout PDF (Sprinkler + car-diagnosis network problem). | No (reference) |
| `Variable.py` | Template `Variable` class — name, assignments, CPT, parents, marginal cache. | No (imported) |
| `Variable_solution.py` | Worked solution — adds `get_probability`, `get_marginal_probability`, child wiring helpers. | No |
| `bn.py` | Template `BayesianNetwork` class — variable bookkeeping, `get_joint_probability`, `get_conditional_probability`. | No |
| `bn_solution.py` | Worked solution — implements joint + conditional via enumeration over unobserved variables. | No |
| `Runner.py` | Template runner. Defines `sprinkler_network()` (no `build_` prefix — combined build+print), plus helpers (`create_random_sample`, `print_marginal_probabilities`, etc.). | Yes (template) |
| `Runner_solution.py` | Worked runner. Splits sprinkler/car build (`build_sprinkler_network`, `build_car_network`) from `main()` and adds a diagnostic-ranking mode. Exposes **`sprinkler_network`** and **`car_network`** as aliases so the template's flat naming still works. | Yes (`py -3.12 Runner_solution.py`) |

## Signature contract with templates

Per the verifier (Phase 3.3) the `*_solution.py` files must keep every public callable name from their template sibling.

- `Runner_solution.sprinkler_network` is exported as a module-level alias for `build_sprinkler_network`. Calling either name returns the same `BayesianNetwork` instance.
- `Runner_solution.car_network` is exported as a module-level alias for `build_car_network`. The template `Runner.py` never defined `car_network` (the car network is from the homework), but we expose it under the symmetric short name so consumers can use the same pattern for both networks.
- All other top-level template callables (`create_random_sample`, `pad`, `print_conditional_probability`, `print_joint_probability`, `print_marginal_probabilities`, `main`) are preserved verbatim.

## Recent changes

- **2026-05-23 (Phase 3.3 targeted fix):** Added module-level aliases `sprinkler_network = build_sprinkler_network` and `car_network = build_car_network` in `Runner_solution.py` so the template's flat naming continues to work. Verified `Runner_solution.py` still runs end-to-end (sprinkler net default).
