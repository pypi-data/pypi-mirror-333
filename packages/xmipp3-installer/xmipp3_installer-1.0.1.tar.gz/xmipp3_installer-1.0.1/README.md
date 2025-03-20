# xmipp3-installer
Python package that handles the installation of xmipp3

## Testing the code
The automatic tests for this package can be run using `./scripts/run-tests.sh` in bash, or `.\scripts\run-tests.ps1` in PowerShell.
If you intend to run this tests from within VSCode, you will need extension `Test Adapter Converter`, and a local `.vscode` folder with a file named `settings.json` inside with the following content:
```json
{
  "python.testing.pytestArgs": [
    ".",
    "--capture=no"
  ],
  "python.testing.unittestEnabled": false,
  "python.testing.pytestEnabled": true
}
```

## SonarQube status
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=I2PC_xmipp3-installer&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=I2PC_xmipp3-installer)

### Ratings
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=I2PC_xmipp3-installer&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=I2PC_xmipp3-installer)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=I2PC_xmipp3-installer&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=I2PC_xmipp3-installer)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=I2PC_xmipp3-installer&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=I2PC_xmipp3-installer)

### Specific metrics
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=I2PC_xmipp3-installer&metric=bugs)](https://sonarcloud.io/summary/new_code?id=I2PC_xmipp3-installer)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=I2PC_xmipp3-installer&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=I2PC_xmipp3-installer)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=I2PC_xmipp3-installer&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=I2PC_xmipp3-installer)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=I2PC_xmipp3-installer&metric=coverage)](https://sonarcloud.io/summary/new_code?id=I2PC_xmipp3-installer)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=I2PC_xmipp3-installer&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=I2PC_xmipp3-installer)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=I2PC_xmipp3-installer&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=I2PC_xmipp3-installer)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=I2PC_xmipp3-installer&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=I2PC_xmipp3-installer)
