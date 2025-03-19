## v0.1.14 (2025-03-11)

### Feat

- add auto versioning (#973)
- Forking agents now removes X (Twitter) event triggers to prevent scheduler extra run. Ensures forked agents start clean, requiring users to configure their own X integrations. (#988)
- add objects as options for combobox in request_data country-name (#968)
- image-to-image support for fireworks.ai (#984)
- setup_and_run.sh to back up old log files before starting new processes (#974)
- enhance agent create next steps (#970)
- add agent embed docs (#965)
- cached agent creation from constructor added (#938)
- env.find_agents to get offset & limit args (#945)
- add MIT License (#943)
- add docs agent tutorial (#901)
- web agent to support eth libs
- ts runner to support vector stores (#913)

### Fix

- add all folders in the root directory as potential modules to import (#960)
- move docs agent to tutorial section (#950)

[main b1a4ab24] bump: version 0.1.13 → 0.1.14
 2 files changed, 24 insertions(+), 1 deletion(-)

