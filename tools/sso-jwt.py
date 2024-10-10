import argparse

from gd_auth.client import AwsIamAuthTokenClient

conf = {
    "dev": {
        "host": "https://dlms.api.dev-gdcorp.tools",
        "sso_host": "sso.dev-godaddy.com"
    },
    "prod": {
        "host": "https://dlms.api.gdcorp.tools",
        "sso_host": "sso.godaddy.com"
    }
}


def generate_iam_token(env: str):
    sso_client = AwsIamAuthTokenClient(
        conf[env]["sso_host"],
        refresh_min=45,
        primary_region='us-west-2',
        secondary_region='us-west-2')
    return sso_client.token


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser("Generate IAM token for SSO")
    argument_parser.add_argument("-e", "--env", type=str, required=True, help="Environment to generate IAM token for", choices=["dev", "prod"])

    args = argument_parser.parse_args()

    print(generate_iam_token(env=args.env))
