@echo off
cd /d "C:\Users\virgi\OneDrive\Documents\Portfolio Website\website-code"
node tools/auto-publish.mjs >> "%~dp0auto-publish.log" 2>&1
