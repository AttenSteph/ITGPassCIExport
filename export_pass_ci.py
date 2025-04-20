import argparse
from pathlib import Path
from sys import exit

import pandas as pd
import requests


def id2org_name(org_id):
    api_organization_id_url = "https://api.itglue.com/organizations/" + org_id
    response = requests.get(api_organization_id_url, headers=headers_payload, data=requests_payload).json()
    name = response['data']['attributes']['name']
    filename = name.lower()
    filename = filename.replace(" ", "_")
    return name, filename


def all_orgs_id_names_dic():
    api_organization_ids_url = "https://api.itglue.com/organizations?page[size]=1000&sort=-name"
    response = requests.get(api_organization_ids_url, headers=headers_payload, data=requests_payload).json()
    orgs = {}
    for x in response['data']:
        orgs[x['id']] = x['attributes']['name']
    return orgs


def print_dic_sorted_by_values(dic):
    sorted_dic = sorted(dic.items(), key=lambda item: item[1])
    for x, y in sorted_dic:
        print(f"{x}: {y}")


def get_request_as_df(api_url):
    response = requests.get(api_url, headers=headers_payload, data=requests_payload).json()
    response_list = []
    for x in response['data']:
        response_list.append(x['attributes'])
    our_df = pd.DataFrame(response_list)
    return our_df


def drop_df_columns(df, drop_list):
    for column_name in drop_list:
        try:
            df = df.drop([column_name], axis=1)
        except Exception as e:
            print(f"\tAn unexpected error occurred: {e}")
            continue
    return df


def make_df(org_id, url_type, drop_list, new_columns):
    if url_type == "configs":
        api_url = "https://api.itglue.com/organizations/" + org_id + "/relationships/configurations?page[size]=1000"
    elif url_type == "passwords":
        api_url = "https://api.itglue.com/organizations/" + org_id + "/relationships/passwords?page[size]=1000"
    else:
        exit(1)
    # create initial configs dataframe
    df = get_request_as_df(api_url)
    # drop columns we do not want
    df = drop_df_columns(df, drop_list)
    # reindex and insert some blank columns
    df = df.reindex(columns=new_columns)
    return df


def write_excel_file(org_file_name, df_configs, df_passwords):
    dir_path = Path('./export_data/')
    dir_path.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter('./export_data/' + org_file_name + '.xlsx') as writer:
        df_configs.to_excel(writer, sheet_name='configs', index=False)
        df_passwords.to_excel(writer, sheet_name='passwords', index=False)
    print("\tWrote data to: ./export_data/" + org_file_name + ".xlsx")


# command line parser
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--key", type=str, required=True, help="Required ITG API Key")
parser.add_argument("-l", "--list-organizations", required=False, action='store_true',
                    help="Lists organization ID numbers.")
parser.add_argument("-i", "--id", type=str, required=False,
                    help="Export for single organization. Requires organization ID number.")
parser.add_argument("-a", "--all-organizations", required=False, action='store_true',
                    help="Export for all organizations in ITG tenant.")
args = parser.parse_args()

# requests payload variables
requests_payload = {}
headers_payload = {'x-api-key': args.key}

# columns to drop from the initial request
# noinspection SpellCheckingInspection
configs_drop_list = ["organization-id", "organization-name", "restricted", "psa-integration", "my-glue", "hostname",
                     "primary-ip", "mac-address", "default-gateway", "serial-number", "asset-tag", "position",
                     "installed-by", "purchased-by", "notes", "operating-system-notes", "warranty-expires-at",
                     "mitp-device-expiration-date", "mitp-end-of-life-date", "installed-at", "purchased-at",
                     "organization-short-name", "configuration-type-id", "configuration-status-id",
                     "configuration-status-name", "manufacturer-id", "manufacturer-name", "model-id",
                     "operating-system-id", "operating-system-name", "location-id", "location-name", "contact-id",
                     "model-name", "contact-name"]
new_configs_columns = ["resource-url", "name", "assigned-technician", "corrected-information", "cross-linked",
                       "created-at", "updated-at", "configuration-type-name", "configuration-type-kind", "archived"]
passwords_drop_list = ["notes", "organization-id", "organization-name", "restricted", "my-glue", "autofill-selectors",
                       "username", "url", "updated-by", "updated-by-type", "resource-id", "cached-resource-type-name",
                       "cached-resource-name", "password-category-id", "created-at", "updated-at", "otp-enabled",
                       "password-folder-id", "resource-type", "rotation-permitted", "parent-url", "vault-id",
                       "personal", "is-live"]
new_passwords_columns = ["resource-url", "name", "assigned-technician", "corrected-information", "cross-linked",
                         "password-updated-at", "password-category-name", "archived"]

# -l, --list-companies
if args.list_organizations is True:
    organizations = all_orgs_id_names_dic()
    print_dic_sorted_by_values(organizations)
    exit(0)

# -a, --all-organizations
if args.all_organizations is True:
    organizations = all_orgs_id_names_dic()
    for key, value in organizations.items():
        print("Querying API for " + key + ", " + value + " ...")

        organization_file_name = value.lower()
        organization_file_name = organization_file_name.replace(" ", "_")

        print("\t" + value + " configurations...")
        try:
            configs = make_df(key, "configs", configs_drop_list, new_configs_columns)
        except Exception as e:
            print(f"\tAn unexpected error occurred: {e}")
            continue

        print("\t" + value + " passwords...")
        try:
            passwords = make_df(key, "passwords", passwords_drop_list, new_passwords_columns)
        except Exception as e:
            print(f"\tAn unexpected error occurred: {e}")
            continue

        # write Excel spreadsheet
        write_excel_file(organization_file_name, configs, passwords)
    exit(0)

# -i, --id
if len(args.id) == 7 and int(args.id) >= 0:
    ("Querying API for " + str(args.id) + " ...")
    # get org name
    organization_name, organization_file_name = id2org_name(args.id)
    print(str(args.id) + " is " + organization_name + ". Querying for:")

    print("\t" + organization_name + " configurations...")
    configs = make_df(args.id, "configs", configs_drop_list, new_configs_columns)
    print("\t" + organization_name + " passwords...")
    passwords = make_df(args.id, "passwords", passwords_drop_list, new_passwords_columns)

    # write Excel spreadsheet
    write_excel_file(organization_file_name, configs, passwords)
    exit(0)
else:
    print("Organization ID is not a valid 7 digit number.")
    exit(1)