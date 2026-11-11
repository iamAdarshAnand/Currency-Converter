# Contributing to Currency Converter

Thanks for helping improve this project. Contributions should address a real bug, improve reliability, or make the project easier to use.

## Before making changes

1. Read the README and inspect the source code to identify the application entry point.
2. Open an issue describing the bug or improvement, including expected behavior.
3. Keep each change focused and avoid committing secrets, API tokens, or generated files.

## Proposing a change

1. Create a branch from the default branch.
2. Implement the improvement and test the behavior you changed.
3. In your pull request, describe what changed, why it matters, and how you tested it.
4. Respond to review feedback before merging.

## Working with a collaborator

If two people genuinely work on the same commit, Git supports a `Co-authored-by: Name <verified-email>` trailer in the commit message. Only credit someone who actually contributed, and use an email they approve for GitHub attribution. A pull-request description alone is not a substitute for a co-authored commit.

## Review checklist

- [ ] The change addresses a documented issue or improvement.
- [ ] Existing behavior is preserved unless the change intentionally fixes it.
- [ ] Relevant manual or automated checks are documented.
- [ ] No credentials or personal data are included.

## Reproducible bug reports

When reporting a conversion problem, include:

- The source and target currency codes, and the input amount.
- The expected result and the actual result, without exposing API credentials.
- The application version or commit, Python version, and relevant error output.
- Whether the issue reproduces consistently or only during network failures.

For exchange-rate discrepancies, include the rate provider and the time of the rate lookup; rates can change between requests.
