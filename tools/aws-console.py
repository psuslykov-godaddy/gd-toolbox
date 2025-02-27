#!/usr/bin/env python3

"""
Usage:
 - Save this script somewhere on your path (e.g. `vi /usr/local/bin/aws-console && chmod +x /usr/local/bin/aws-console`)
 - Make AWS credentials available in one of the usual places where boto3 can find them (~/.aws/credentials, env var, etc.)
 - Excute the script: `aws-console --profile myprofile`
 - :tada: Your browser opens and you are signed in into the AWS console
"""

import argparse
import json
import webbrowser
from urllib import parse, request

import boto3


def open_console(profile_name=None, echo_to_stdout=False):
    creds = boto3.Session(profile_name=profile_name).get_credentials()
    url_credentials = dict(sessionId=creds.access_key,sessionKey=creds.secret_key, sessionToken=creds.token)

    request_parameters = "?Action=getSigninToken"
    request_parameters += "&DurationSeconds=43200"
    request_parameters += "&Session=" + parse.quote_plus(json.dumps(url_credentials))
    request_url = "https://signin.aws.amazon.com/federation" + request_parameters
    with request.urlopen(request_url) as response:
        if not response.status == 200:
            raise Exception("Failed to get federation token")
        signin_token = json.loads(response.read())

    request_parameters = "?Action=login"
    request_parameters += "&Destination=" + parse.quote_plus("https://console.aws.amazon.com/")
    request_parameters += "&SigninToken=" + signin_token["SigninToken"]
    request_parameters += "&Issuer=" + parse.quote_plus("https://example.com")
    request_url = "https://signin.aws.amazon.com/federation" + request_parameters

    if echo_to_stdout:
        print(request_url)
    else:
        webbrowser.open(request_url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Open the AWS console in your web browser, using your AWS CLI credentials')
    parser.add_argument('--profile', default=None, help='the AWS profile to create the presigned URL with')
    parser.add_argument(
        '--stdout', action='store_true', help='don\'t open the webbrowser, but echo the signin URL to stdout')

    args = parser.parse_args()
    open_console(args.profile, args.stdout)
