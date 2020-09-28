#!/bin/bash

python -m grpc_tools.protoc -Iproto \
    -I /usr/local/Cellar/protobuf/3.13.0/include \
    --python_out=./ --grpc_python_out=./ \
    proto/tron/proto/api/api.proto proto/tron/proto/core/*
