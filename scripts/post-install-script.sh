#!/bin/bash

# This script is intended to run after pnpm install
# CWD into apps/backend and run uv sync
cd apps/backend
uv sync