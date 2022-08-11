ls protocol_buffers | \
grep .proto | \
xargs python3 -m grpc_tools.protoc \
    --proto_path=protocol_buffers \
    --python_out=compiled_protobufs \
    --grpc_python_out=compiled_protobufs