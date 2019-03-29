#!/usr/bin/env bash
set -euo pipefail

zipcodes="$(
    sqlite3 "$(pp-db load-path)" \
        'SELECT DISTINCT(zipcode) FROM training_std_scores;'
)"
echo "${zipcodes}" | parallel '
pp-model k-means-zip-code-price {} --plot -k 1 > zip-code-{}-k-1.svg
pp-model k-means-zip-code-price {} --plot -k 2 > zip-code-{}-k-2.svg
pp-model k-means-zip-code-price {} --plot -k 3 > zip-code-{}-k-3.svg
pp-model k-means-zip-code-price {} --plot -k 4 > zip-code-{}-k-4.svg
pp-model k-means-zip-code-price {} --plot -k 5 > zip-code-{}-k-5.svg
pp-model k-means-zip-code-price {} --plot -k 6 > zip-code-{}-k-6.svg
pp-model k-means-zip-code-price {} --plot -k 7 > zip-code-{}-k-7.svg
pp-model k-means-zip-code-price {} --plot -k 8 > zip-code-{}-k-8.svg
'
