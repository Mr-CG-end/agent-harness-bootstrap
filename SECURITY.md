# Security Policy

## Supported versions

Security fixes are applied to the latest release and the default branch.

## Reporting a vulnerability

Use GitHub private vulnerability reporting after the repository is published. Do not include credentials or private repository contents in a public issue.

## Trust boundary

The packaged auditor is designed to be read-only and offline. It inventories filenames, selected package scripts, and source counts. It must not read environment variables, credential stores, source-file contents, Git remotes, or network resources.

Skill instructions are executable supply-chain inputs for coding agents. Review changes to `SKILL.md`, scripts, permissions, remote operations, and installation guidance with the same care as executable code.
