# Description
Exports specific password and configurations data for use in documentation review for one or all organizations into an Excel workbook(s) using the [IT Glue API](https://api.itglue.com/developer/).

# Install
Pick one:
1. Clone repo, install needed modules if you don't have them., and run export_pass_ci.py
2. Download latest .exe release and run.

# Usage
You'll need to create an API key. See [Kaseya documentation](https://help.itglue.kaseya.com/help/Content/1-admin/it-glue-api/getting-started-with-the-it-glue-api.html)
```
usage: export_pass_ci.py [-h] -k KEY [-l] [-i ID] [-a]

options:
  -h, --help            show this help message and exit
  -k KEY, --key KEY     Required ITG API Key
  -l, --list-organizations
                        Lists organization ID numbers.
  -i ID, --id ID        Export for single organization. Requires organization ID number.
  -a, --all-organizations
                        Export for all organizations in ITG tenant.
```
Data outputs to .\export_data\company_name.xlsx

# Examples

```
> python export_pass_ci.py -k "ITG.0123456789abcdefghijklmnopqrstuv.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890a" -l
1234567: Contoso Incorporated
0987654: Acme Corporation
4231337: Umbrella Corporation
...
```
```
> python export_pass_ci.py -k "ITG.0123456789abcdefghijklmnopqrstuv.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890a" -i 4231337
4231337 is Umbrella Corporation. Querying for:
        Umbrella Corporation configurations...
        Umbrella Corporation passwords...
        Wrote data to: ./export_data/umbrella_corporation.xlsx
```
```
> python export_pass_ci.py -k "ITG.0123456789abcdefghijklmnopqrstuv.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890a" -a
Querying API for 1234567, Contoso Incorporated ...
        Contoso Incorporated configurations...
        Contoso Incorporated passwords...
        Wrote data to: ./export_data/contoso_incorporated.xlsx
Querying API for 0987654, Acme Corporation ...
        Acme Corporation configurations...
        Acme Corporation passwords...
        Wrote data to: ./export_data/acme_corporation.xlsx
Querying API for 4231337, Umbrella Corporation ...
        Umbrella Corporation configurations...
        Umbrella Corporation passwords...
        Wrote data to: ./export_data/umbrella_corporation.xlsx
...
```