#!/bin/bash

python -m grpc_tools.protoc -Iproto \
    -I /usr/local/Cellar/protobuf/3.12.4/include \
    --python_out=./ --grpc_python_out=./ \
    proto/tron/api/api.proto proto/tron/core/*
