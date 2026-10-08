# Security and research boundaries

MacBridge is research into compatibility, not into defeating platform security. The public project follows
these rules.

## What MacBridge does not do

- Bypass, disable, or weaken code signing, the app sandbox, AMFI, or any other platform security mechanism.
- Use exploits, privilege escalation, or jailbreaks.
- Forge or misuse entitlements.
- Change security settings on users' devices.
- Distribute Apple proprietary files: binaries, frameworks, dyld shared caches, system images, or restore
  images.

If a goal turns out to require any of the above, it is recorded as **blocked** — "requires a capability
unavailable in the supported environment" — and the project moves on. A precise negative result is a
legitimate outcome.

## How research is done

- Only NORD LABS's own test programs are executed in experiments.
- Devices are used through standard Apple developer tools and normal developer signing.
- Results are published only when they are safe to publish and do not describe a way around a security
  control.

## Reporting a security issue

If you believe something in this repository could help someone bypass platform security, or exposes
information it should not, please contact NORD LABS privately through the organization's GitHub profile
instead of opening a public issue.
