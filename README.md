# homebrew-tap

Homebrew tap for `roll`.

## Install

```bash
brew install katrinio/tap/roll
```

## Bottles

Build and publish a bottle with the `publish-bottle` GitHub Actions workflow.
It will:

- install the formula from source on macOS;
- run `brew bottle`;
- upload the bottle to the `bottles` GitHub release;
- update the `bottle do` block in the formula.

After that, `brew install katrinio/tap/roll` can download the prebuilt bottle instead of rebuilding the Python environment locally.

## Formulae

- `roll` — personal film roll index
