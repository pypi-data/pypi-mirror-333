This directory contains the station-specific deployment settings, and selected versions of external images. The YAML files
are used by levant for rendering the nomad templates.

 For production, they are loaded in `.gitlab-ci.yml` as
part of deployment.

NB:

* For each section, only the one in the last applied file will be used. The sections will not be merged. So be careful when specifying a section in multiple files.
