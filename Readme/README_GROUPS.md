# ClearCom Project Split for 4 Groups

This document divides the Mini-Compiler project into 4 groups.
Only documentation is changed. No code changes are required for this split.

## Group 1: Lexer and Input Validation Team

Scope:
- Own lexical analysis rules and token definitions.
- Handle invalid characters and lexical error messages.
- Keep token coverage aligned with supported language syntax.

Main files:
- lexer.py
- input.mc
- error_input.mc
- error_test2.mc

Responsibilities:
- Maintain keyword, identifier, number, and string token rules.
- Improve clarity of lexer error output with line numbers.
- Create and maintain lexer-focused test inputs.

Deliverables:
- Token rule documentation table.
- 5 valid and 5 invalid lexer test snippets.
- Short report: common lexical failures and fixes.

## Group 2: Parser and Semantic Rules Team

Scope:
- Own grammar rules and parser error recovery.
- Handle declarations, assignments, and expression parsing.
- Own semantic checks based on symbol declarations.

Main files:
- parser.py
- symbol_table.py

Responsibilities:
- Maintain grammar for supported mini language.
- Keep parser/semantic error messages readable and precise.
- Ensure duplicate/undeclared variable checks work consistently.

Deliverables:
- Grammar summary in EBNF-like notation.
- Parser test matrix with pass/fail cases.
- Short report: parser recovery behavior and limitations.

## Group 3: Runtime Execution and Output Team

Scope:
- Own expression evaluation and statement execution.
- Maintain runtime value handling and runtime error reporting.
- Validate print/printf behavior.

Main files:
- executor.py

Responsibilities:
- Evaluate numeric/id/binop expressions correctly.
- Enforce runtime type behavior for int and float assignments.
- Keep output formatting and runtime errors consistent.

Deliverables:
- Runtime behavior checklist.
- 8 execution test cases with expected output.
- Short report: runtime edge cases (division, modulo, type mismatch).

## Group 4: CLI, UX, and Documentation Team

Scope:
- Own user-facing compile flow and interactive mode.
- Maintain run instructions and project documentation quality.
- Keep onboarding simple for first-time users.

Main files:
- main.py
- interactive.py
- README.md
- HOW_TO_RUN.md
- PRESENTATION.md
- VENV_TERMINAL_ONLY.md

Responsibilities:
- Keep command-line experience clear in success/failure cases.
- Keep interactive prompts/help text accurate.
- Ensure all docs match current project behavior.

Deliverables:
- Updated run guide and quick start.
- Demo script for project presentation.
- Documentation consistency checklist.

## Integration Plan (All Groups)

1. Weekly sync with one representative from each group.
2. Merge order:
- Group 1 first, then Group 2, then Group 3, then Group 4 docs and UX updates.
3. Final end-to-end testing with:
- input.mc
- error_input.mc
- error_test2.mc
- cstyle.mc

## Suggested Team Roles Inside Each Group

- Lead: coordinates tasks and reviews output.
- Implementer: makes file updates.
- Tester: validates behavior using sample inputs.
- Reporter: prepares summary and demo notes.

## Definition of Done

- Group deliverables completed.
- No regressions in compile and interactive flows.
- Errors are readable and include line context.
- Documentation reflects actual project behavior.
