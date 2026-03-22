#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$ROOT_DIR/data"
TMP_DIR="$DATA_DIR/_tmp_download"
TEST_UNZIP_DIR="$TMP_DIR/test_unzip"
BASE_URL="https://huggingface.co/datasets/osunlp/Mind2Web/resolve/main"

mkdir -p "$DATA_DIR/train" "$DATA_DIR/test_task" "$DATA_DIR/test_website" "$DATA_DIR/test_domain" "$TMP_DIR"

download_if_missing() {
  local url="$1"
  local out="$2"
  if [ -f "$out" ] && [ -s "$out" ]; then
    echo "skip existing: $out"
    return 0
  fi
  echo "download: $url"
  curl -L --fail --output "$out" "$url"
}

for idx in 0 1 2 3 4 5 6 7 8 9 10; do
  download_if_missing "$BASE_URL/data/train/train_${idx}.json" "$DATA_DIR/train/train_${idx}.json"
done

download_if_missing "$BASE_URL/scores_all_data.pkl" "$DATA_DIR/scores_all_data.pkl"
download_if_missing "$BASE_URL/test.zip" "$TMP_DIR/test.zip"

rm -rf "$TEST_UNZIP_DIR"
mkdir -p "$TEST_UNZIP_DIR"
unzip -q -o -P mind2web "$TMP_DIR/test.zip" -d "$TEST_UNZIP_DIR"

if [ -d "$TEST_UNZIP_DIR/data/test_task" ]; then
  cp -f "$TEST_UNZIP_DIR"/data/test_task/*.json "$DATA_DIR/test_task/"
  cp -f "$TEST_UNZIP_DIR"/data/test_website/*.json "$DATA_DIR/test_website/"
  cp -f "$TEST_UNZIP_DIR"/data/test_domain/*.json "$DATA_DIR/test_domain/"
elif [ -d "$TEST_UNZIP_DIR/test_task" ]; then
  cp -f "$TEST_UNZIP_DIR"/test_task/*.json "$DATA_DIR/test_task/"
  cp -f "$TEST_UNZIP_DIR"/test_website/*.json "$DATA_DIR/test_website/"
  cp -f "$TEST_UNZIP_DIR"/test_domain/*.json "$DATA_DIR/test_domain/"
else
  echo "unexpected test.zip structure under $TEST_UNZIP_DIR" >&2
  exit 1
fi

echo
echo "download completed"
echo "train files: $(find "$DATA_DIR/train" -maxdepth 1 -name '*.json' | wc -l | tr -d ' ')"
echo "test_task files: $(find "$DATA_DIR/test_task" -maxdepth 1 -name '*.json' | wc -l | tr -d ' ')"
echo "test_website files: $(find "$DATA_DIR/test_website" -maxdepth 1 -name '*.json' | wc -l | tr -d ' ')"
echo "test_domain files: $(find "$DATA_DIR/test_domain" -maxdepth 1 -name '*.json' | wc -l | tr -d ' ')"
echo "scores file: $DATA_DIR/scores_all_data.pkl"
