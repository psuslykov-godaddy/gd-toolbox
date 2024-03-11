from gd_auth.client import AwsIamAuthTokenClient

ENV = "prod"

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

sso_client = AwsIamAuthTokenClient(
    conf[ENV]["sso_host"],
    refresh_min=45,
    primary_region='us-west-2',
    secondary_region='us-west-2')
iam_token = sso_client.token
print(iam_token)
