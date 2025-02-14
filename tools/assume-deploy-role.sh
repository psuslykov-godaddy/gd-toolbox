#!/bin/bash

export AWS_DEFAULT_REGION=us-west-2

# Get the AWS account ID of the current user
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
if [ -z "$ACCOUNT_ID" ]; then
  echo "Failed to retrieve AWS Account ID"
  exit 1
fi

# Get Deploy Role Name
DEPLOY_ROLE_NAME=$(aws ssm get-parameter --name "/AdminParams/Role/DeployRole" --query "Parameter.Value" --output text)
if [ -z "$DEPLOY_ROLE_NAME" ]; then
  echo "Failed to retrieve Deploy Role Name"
  exit 1
fi
ROLE_ARN="arn:aws:iam::$ACCOUNT_ID"":role/$DEPLOY_ROLE_NAME"

# Log into the Deploy User
SECRET_ARN=$(aws secretsmanager list-secrets --region $AWS_DEFAULT_REGION --query "SecretList[?starts_with(Name, '/Secrets/IAMUser/GD-AWS-DeployUser-RevRelvnc')].ARN" --output text)
if [ -z "$SECRET_ARN" ]; then
  echo "Failed to retrieve the secret ARN"
  exit 1
fi

DEPLOY_USER_CREDS=$(aws secretsmanager get-secret-value --secret-id $SECRET_ARN --output json)
AWS_ACCESS_KEY_ID=$(echo $DEPLOY_USER_CREDS | jq -r ".SecretString" | jq -r '.AccessKeyId')
AWS_SECRET_ACCESS_KEY=$(echo $DEPLOY_USER_CREDS | jq -r ".SecretString" | jq -r '.SecretAccessKey')
unset AWS_SESSION_TOKEN

# Assume the Deploy Role
DEPLOY_ROLE_SECRETS=$(aws sts assume-role --role-arn "$ROLE_ARN" --role-session-name assume-deploy-role)

export AWS_ACCESS_KEY_ID=$(echo $DEPLOY_ROLE_SECRETS | jq -r ".Credentials.AccessKeyId")
export AWS_SECRET_ACCESS_KEY=$(echo $DEPLOY_ROLE_SECRETS | jq -r ".Credentials.SecretAccessKey")
export AWS_SESSION_TOKEN=$(echo $DEPLOY_ROLE_SECRETS | jq -r ".Credentials.SessionToken")
