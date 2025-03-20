# Stingray

![Build status](git.astron.nl/lofar2.0/cryptocoryne/badges/main/pipeline.svg)
![Test coverage](git.astron.nl/lofar2.0/cryptocoryne/badges/main/coverage.svg)
<!-- ![Latest release](https://git.astron.nl/templates/python-package/badges/main/release.svg) -->

Cryptocoryne registeres and renews certificates for the lofar.net domain based on consul service registrations.

## Installation

```
pip install .
```

## Usage

Cryptocoryne runs periodically on the central nomad cluster.

Every 5 minutes, cryptocoryne queries all services registered within consul that have the tag `cert`.
Then the certificate `<service_name>.lofar.net` is registered or renewed (if needed) and stored in the LOFAR vault.

Services then have the option to retrieve the certificates from the vault using nomads job templating:
```hcl
template {
  data = <<EOH
{{with secret "lets-encrypt/certificates/<service_name>.lofar.net" -}}
{{.Data.data.cert }}
{{.Data.data.chain -}}
{{end}}
EOH
  destination = "${NOMAD_SECRETS_DIR}/fullchain.cer"
}
template {
  data = <<EOH
{{with secret "lets-encrypt/certificates/<service_name>.lofar.net" -}}
{{.Data.data.key -}}
{{end}}
EOH
  destination = "${NOMAD_SECRETS_DIR}/key.key"
}
```
## Contributing

To contribute, please create a feature branch and a "Draft" merge request.
Upon completion, the merge request should be marked as ready and a reviewer
should be assigned.

Verify your changes locally and be sure to add tests. Verifying local
changes is done through `tox`.

```pip install tox```

With tox the same jobs as run on the CI/CD pipeline can be run. These
include unit tests and linting.

```tox```

To automatically apply most suggested linting changes execute:

```tox -e format```

## License
This project is licensed under the Apache License Version 2.0
