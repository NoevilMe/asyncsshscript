#!/bin/env bash
set -e

ip a|grep '10\.' -C 2
cat /proc/cpuinfo
