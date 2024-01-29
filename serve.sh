#!/bin/bash
# From: https://shotor.com/blog/build-a-hugo-static-site-in-your-browser-using-github-codespaces/
# Obtain GitHub URL from CodeSpaces' "Ports" bottom panel: right-click port 1313 > Copy Local Address
# export GITHUB_URL=""

if [[ -z "${GITHUB_URL}" ]]; then
    echo "WARNING: in Codespaces, export GITHUB_URL starting with HTTPS if needed"
    extra_params=""
else
    extra_params="--baseUrl=\"${GITHUB_URL}\" --appendPort=false"
fi

hugo server -D ${extra_params}