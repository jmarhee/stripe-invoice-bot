#!/bin/bash

TAG=$TAG
TAG_COMMIT=$(git rev-parse --short ${TAG})

#AUTH_TOKEN=$GITEA_TOKEN
#curl -X POST "https://git-central.openfunction.co/api/v1/repos/jmarhee/stripe-invoice-bot/releases" -H "Authorization: token $AUTH_TOKEN" \
#    -H  "accept: application/json" -H  "Content-Type: application/json" \
#    -d "{  \"body\": \"Cutting ${TAG} at ${TAG_COMMIT}\",  \"draft\": false,  \"name\": \"${TAG}\",  \"prerelease\": false,  \"tag_name\": \"${TAG}\",  \"target_commitish\": \"${TAG_COMMIT}\"}" \
#    -ik

AUTH_TOKEN=$GITHUB_TOKEN
curl \
  -X POST "https://api.github.com/repos/jmarhee/stripe-invoice-bot/releases" -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d "{  \"body\": \"Cutting ${TAG} at ${TAG_COMMIT}\",  \"draft\": false,  \"name\": \"${TAG}\",  \"prerelease\": false,  \"tag_name\": \"${TAG}\" }" \
