#!/bin/bash
echo "doorbell" | socat - UDP-DATAGRAM:255.255.255.255:12345,broadcast
