# Tools for server operators

Small, read-only Python helpers that check a Star Conflict server install
before you restart it. They only read files (and, for `security_audit.py`,
optionally `netstat`); nothing is modified. All of them use the Python
standard library only.

Run them from a virtual environment at the repository root:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -X utf8 -I tools\<tool>.py --help
```

`<game>` below is the `star conflict` folder of your install (for Steam:
`...\steamapps\common\star conflict`). Work on a copy of the install when you
edit files.

| Tool | What it checks | Typical use |
|---|---|---|
| [`queue_lint.py`](queue_lint.py) | the matchmaker queue block of `cloud/data/default_platform_config.lua`: syntax, `InstantiateQueueTemplate` arguments, rank/value ranges, unknown templates and bot presets, levels that are not active, rank coverage | `queue_lint.py --depot "<game>"` after editing queues |
| [`defname_check.py`](defname_check.py) | whether definition names (ships, modules, resources, bot presets) exist, where they are defined and the closest matches | `defname_check.py --depot "<game>" --xml edited_store.xml` |
| [`data_drift_check.py`](data_drift_check.py) | an edited install against an untouched copy: changed/added/missing data files, generated XML that is stale or edited by hand, store ids shifted by inserted or removed definitions | `data_drift_check.py "<untouched copy>" "<game>"` |
| [`security_audit.py`](security_audit.py) | node configuration: listening interfaces, MongoDB exposure, console settings, logging of sensitive data; secrets are never printed | `security_audit.py "<game>" --listening` |
| [`extract_cvars.py`](extract_cvars.py) | generates the [cvar reference](../docs/05-configuration/cvar-reference.md) from the platform config with English translations (`cvar_translations.json`) | maintainers |

Background and the shipped-config results:
[config-validation-tools](../docs/07-administration/config-validation-tools.md),
[security chapter](../docs/07-administration/security.md),
[settings reload map](../docs/05-configuration/settings-reload-map.md).
