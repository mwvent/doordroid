#!/bin/bash
echo "pir_door" | socat - UDP-DATAGRAM:255.255.255.255:12345,broadcast
