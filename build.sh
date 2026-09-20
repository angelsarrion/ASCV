#!/usr/bin/env bash
set -e

echo "=== Compiling Ángel Sarrión CV & Personal Space ==="
python3 tools/build.py
python3 tools/generate_pdf.py
echo "=== Build completed successfully! ==="
