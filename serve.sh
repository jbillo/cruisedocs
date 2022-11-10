#!/bin/bash
# From: https://shotor.com/blog/build-a-hugo-static-site-in-your-browser-using-github-codespaces/
# Obtain GitHub URL from CodeSpaces' "Ports" bottom panel: right-click port 1313 > Copy Local Address
# export GITHUB_URL=""

if [[ -z "${GITHUB_URL}" ]]; then
    echo "WARNING: export GITHUB_URL starting with HTTPS if needed"
fi

hugo server -D --baseUrl="${GITHUB_URL}" --appendPort=false