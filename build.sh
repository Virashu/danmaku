#!/bin/env bash

python -m pyinstaller --onefile --clean --name danmaku --icon ./danmaku/resources/icon.ico ./danmaku/main.py
cp -r ./danmaku/resources ./dist/resources
