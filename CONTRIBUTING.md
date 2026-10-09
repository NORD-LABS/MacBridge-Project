# Contributing to MacBridge

Thank you for your interest. MacBridge is a small, independent research project, and careful outside eyes
are valuable: a corrected fact, a sharper question or a reproducible observation can save weeks.

Please read this page before contributing. It explains what is welcome, how to send it, and the terms that
apply.

## What this repository is

This public repository holds MacBridge's project page, status, roadmap and research documentation. The
implementation is in a separate private repository, so code changes to MacBridge itself cannot be proposed
here.

This repository is **source-available, not open source**. It is licensed under the
[ISO NORD CA Commercial & Source-Available License](LICENSE.md). In particular:

- Contributions are governed by **Section 11 (Contributions)** of the license. By intentionally submitting a
  contribution, you confirm that you have the right to submit it and you grant the licensor the license
  described there. You keep your copyright unless a separate signed agreement says otherwise.
- The licensor may accept, change or decline any contribution, and contributions are voluntary and unpaid
  (Sections 11.4 and 11.5). **No contribution is guaranteed to be accepted.**
- Submitting a contribution does not give you any right to use, copy, modify or redistribute this
  repository beyond what the license already allows.

If you are unsure whether you can contribute something (for example because it came from your employer's
work, or from another project's code), please do not submit it.

## Ways to help

### Report a documentation error

Something wrong, unclear, outdated or contradictory? Open an issue with the **Documentation correction**
template. Quote the exact sentence, say where it is, and, if you can, link to the source that shows the
correct version.

### Ask a technical research question

Questions about the approach, a claim or an assumption are welcome. Use the **Research question** template.
Good questions are specific: "how does the loader handle X?" is easier to answer well than "will it work?".

### Share a reproducible observation

If you have measured something relevant on your own hardware, such as how an iPadOS version behaves for a
documented API, use the **Reproducible observation** template, and include:

- what you did, step by step;
- what you expected and what happened;
- the device model and the exact OS version and build;
- the tools and versions you used.

Please do **not** include device identifiers (serial numbers, UDIDs, ECIDs), account names, signing
certificates, provisioning profiles or any other secret.

### Propose an experiment or a hypothesis

Ideas for experiments are welcome when they respect the [research boundaries](SECURITY.md): only original
test code, standard developer tools, and no bypassing of code signing, the sandbox or any other platform
protection. Explain what the experiment would show in either outcome. Experiments that are only
informative if they succeed are less useful than ones whose failure also teaches something.

### Suggest a documentation improvement

Pull requests that fix typos, broken links or unclear wording in this repository's documentation are
welcome. Keep them small and focused. Before opening one:

- run `python3 scripts/check-docs.py` and make sure it passes;
- keep to the facts in [docs/facts.md](docs/facts.md); a pull request should not add a claim about what
  MacBridge has achieved;
- follow the [evidence rules](docs/evidence.md#rules): every result names its environment.

## Security issues

Do not open a public issue for anything that could help someone bypass a platform protection, or that
exposes information that should not be public. Follow [SECURITY.md](SECURITY.md) instead. MacBridge has no
bug-bounty program.

## Conduct

Be precise, be kind, and assume good faith. Disagreement about evidence is welcome; personal attacks are
not. The maintainer may close or hide content that does not follow this.

## Licensing and permission requests

For commercial use, redistribution or any use the license does not allow, write to
info@theo-picture.com. Nothing is authorized until it is confirmed in writing (license Section 8).
