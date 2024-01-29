#!/bin/bash

TAG=$(git describe --tags)
echo "$TAG" > tag
