#!/bin/sh

PID=$1
gdbserver :9999 --attach $PID
