# Contributing

Thanks for helping grow this collection. Skills here should work on any assistant that supports the open [Agent Skills](https://agentskills.io) standard, so please keep them platform-neutral.

## How the repo is organized

- Skills are grouped into **plugins** under `plugins/<group>/skills/<skill-name>/`.
- A group is the unit people install through Claude, Codex/ChatGPT and Gemini. Individual skills are installable through `npx skills` and release zips.
- Skill names must be unique across the whole repo, not just within a group.

All scripts need Python 3.9+ and no extra packages.

## Add a skill to an existing group

```bash
python scripts/new_skill.py <group> <skill-name> "<what it does and when to use it>"
```

This creates `plugins/<group>/skills/<skill-name>/SKILL.md` from the template. Then:

1. Write the instructions in `SKILL.md`. Keep it under ~500 lines; put long reference material in extra files in the same folder and link to them.
2. Make the `description` say **what the skill does and when to use it**, with trigger phrases (max 1024 characters). Assistants read it to decide when to load the skill.
3. Add a row to `plugins/<group>/README.md` and to the group table in `README.md`.
4. Run `python scripts/validate_skills.py`.
5. Open a pull request. CI runs the validator automatically.

## Add a new group

```bash
python scripts/new_group.py <group-name> "<one-line description>" --category <Category>
```

This creates the group's three manifests (Claude, portable/Codex, Gemini), a README, and an empty `skills/` folder, and registers the group in both marketplace files. Add a row for it to the tables in `README.md` and `INSTALL.md`.

Prefer adding to an existing group unless the new skills serve a clearly different audience. A good group is something a person would want to install as a set.

## Writing portable skills

- Don't refer to a specific assistant's tool names (for example "use the Bash tool"). Describe the action instead ("run this command").
- Don't rely on platform-only features unless the skill says so up front.
- Scripts should state their runtime and avoid OS-specific paths.
- No secrets, credentials, or personal data in skill files.

## Versions and releases (maintainers)

Each group is versioned on its own, and every release gets a git tag named **`<group>--v<version>`**, for example `learning--v1.2.0`. That's the tag format Claude Code uses for plugins. One version number covers the whole group: its three manifests plus a `metadata.version` line in each skill's `SKILL.md`.

### Cut a release

```bash
python scripts/release.py learning patch --dry-run   # preview: new version, tag, commits included
python scripts/release.py learning patch             # or minor / major / 2.0.0
git push && git push origin learning--v1.0.1         # or add --push to the command above
```

The script:

1. Refuses to run if the working tree has uncommitted changes or the tag already exists.
2. Sets the new version in all three manifests and in every skill's `metadata.version`.
3. Adds a section to `plugins/<group>/CHANGELOG.md` listing the commits that touched the group since its last tag.
4. Runs the validator, then commits `release(<group>): v<version>` and creates the annotated tag.

Pushing the tag triggers the **Release a skill group** workflow, which checks the tag against `plugin.json` and publishes a GitHub Release with that group's skill zips.

To tag a group at its current version without bumping (for example the very first tag), pass the current version: `python scripts/release.py learning 1.0.0`.

**Why it matters:** Claude users only receive a new copy of a group when its version changes. Edits pushed without a release stay invisible to them, so release whenever you want people to get your changes.

### Debugging with tags

| Question | Command |
| :--- | :--- |
| What versions exist? | `git tag -l "learning--v*" --sort=-v:refname` |
| What changed between two versions? | `git diff learning--v1.0.0 learning--v1.1.0 -- plugins/learning` |
| What changed since the last release? | `git log learning--v1.1.0..HEAD --oneline -- plugins/learning` |
| Look at the files as they were | `git checkout learning--v1.0.0` (then `git switch -` to return) |
| Which release introduced a problem? | `git bisect start <bad-tag> <good-tag>`, then test each step |
| Which version is installed? | Ask the assistant to report the skill's `metadata.version`, or check `/plugin` (Claude), `codex plugin marketplace list`, or `gemini extensions list` |

To reproduce a bug on a specific version, install that tag. See *Pin a specific version* in [INSTALL.md](./INSTALL.md).
