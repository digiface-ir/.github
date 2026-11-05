# .github

Organization-wide defaults for every DigiFace repository that has none of its own:

| File | Used for |
|---|---|
| `profile/README.md` | The public page at github.com/digiface-ir |
| `PULL_REQUEST_TEMPLATE.md` | The body every new pull request starts with |
| `.github/ISSUE_TEMPLATE/task.md` | A task, in the project's ticket format |
| `.github/ISSUE_TEMPLATE/bug.md` | A bug found on staging or production |

This repository is public, because GitHub only shows the profile page from a public
`.github`. Nothing internal goes here.

The profile images are drawn by `profile/source/make_profile_art.py` (Estedad and Vazirmatn, SIL Open Font License), because GitHub strips fonts from a README. Change the text there and run it again.
