#!/usr/bin/env bash
set -e

echo "=== Encoding Repair Lambda: Build Start ==="

BUILD_DIR="lambda_build"
OUTPUT_ZIP="lambda_http/deployment.zip"

echo "[1] Clean build directory"
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"

echo "[2] Install dependencies into build directory"
pip install --no-deps --target "${BUILD_DIR}" -r requirements.txt

echo "[3] Copy application source"
cp -r core "${BUILD_DIR}/"
cp -r backend "${BUILD_DIR}/"
cp lambda_http/main.py "${BUILD_DIR}/"

echo "[4] Create ZIP archive"
mkdir -p lambda_http
cd "${BUILD_DIR}"
zip -r ../"${OUTPUT_ZIP}" .
cd -

echo "=== Encoding Repair Lambda: Build Completed Successfully ==="
echo "ZIP output → ${OUTPUT_ZIP}"

