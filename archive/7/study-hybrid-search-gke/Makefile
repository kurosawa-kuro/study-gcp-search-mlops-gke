SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/../..)

.PHONY: help
help:
	@$(MAKE) -C $(ROOT) help

.DEFAULT:
	@$(MAKE) -C $(ROOT) $(MAKECMDGOALS)
