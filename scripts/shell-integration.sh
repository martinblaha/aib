#!/usr/bin/env bash
# aib shell integration template
# This file is a reference; use `_aib init` to generate shell-specific integration.
#
# Usage:
#   _aib init >> ~/.bashrc && source ~/.bashrc
#   _aib init --shell zsh >> ~/.zshrc && source ~/.zshrc
#   _aib init --shell fish >> ~/.config/fish/config.fish

# --- bash ---
aib_bash() {
  local cmd
  cmd=$(_aib "$@") || return $?
  if [[ -n "$cmd" ]]; then
    READLINE_LINE="$cmd"
    READLINE_POINT=${#cmd}
  fi
}

# --- zsh ---
aib_zsh() {
  local cmd
  cmd=$(_aib "$@") || return $?
  [[ -n "$cmd" ]] && print -z "$cmd"
}
