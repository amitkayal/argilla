#!/usr/bin/env bash

cd frontend \
&& npm install \
&& npm run-script lint \
&& npm run-script test \
&& DIST_FOLDER=../src/argilla/server/static npm run-script build \

