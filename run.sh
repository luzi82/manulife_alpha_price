#!/bin/bash -e

rm -rf output

rm -rf profile
rm -rf tmp
rm -rf tmp_0
rm -rf venv

mkdir -p tmp_0
pushd tmp_0
wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz
wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz.asc
sha256sum -c ../geckodriver-v0.29.0-linux64.tar.gz.sha256sum
tar -xzvf geckodriver-v0.29.0-linux64.tar.gz
popd

python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt

python3 -u -m mil_alpha_price.browser_bot "$@"

deactivate

rm -rf profile
rm -rf tmp
rm -rf tmp_0
rm -rf venv
