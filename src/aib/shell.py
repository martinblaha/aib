"""Shell integration script generator for aib."""

BASH_INTEGRATION = '''\
# aib shell integration
# Add to ~/.bashrc or ~/.bash_profile

# True readline injection via keybinding (recommended):
#   1. Type your query at the prompt: find large files
#   2. Press Alt+a
#   3. Picker appears, selected command replaces the buffer
#   4. Press Enter to run (or edit first)
__aib_widget__() {
  local query="$READLINE_LINE"
  READLINE_LINE=""
  READLINE_POINT=0
  if [[ -n "$query" ]]; then
    local cmd
    cmd=$(_aib "$query") || {
      # On error or cancel: restore the original query
      READLINE_LINE="$query"
      READLINE_POINT=${#query}
      return
    }
    if [[ -n "$cmd" ]]; then
      READLINE_LINE="$cmd"
      READLINE_POINT=${#cmd}
    else
      READLINE_LINE="$query"
      READLINE_POINT=${#query}
    fi
  fi
}
bind -x '"\\ea": __aib_widget__'

# Direct invocation fallback: aib "your query"
# The selected command is shown pre-filled for editing; press Enter to run.
aib() {
  local cmd result
  cmd=$(_aib "$@") || return $?
  if [[ -n "$cmd" ]]; then
    read -e -i "$cmd" result || return 0
    if [[ -n "$result" ]]; then
      history -s "$result"
      eval "$result"
    fi
  fi
}
'''

ZSH_INTEGRATION = '''\
# aib shell integration
# Add to ~/.zshrc
aib() {
  local cmd
  cmd=$(_aib "$@") || return $?
  [[ -n "$cmd" ]] && print -z "$cmd"
}
'''

FISH_INTEGRATION = '''\
# aib shell integration
# Add to ~/.config/fish/config.fish
function aib
  set cmd (_aib $argv)
  or return $status
  if test -n "$cmd"
    commandline "$cmd"
  end
end
'''


def get_integration(shell: str) -> str:
    """Return shell integration code for the given shell."""
    shell = shell.lower()
    if "zsh" in shell:
        return ZSH_INTEGRATION
    elif "fish" in shell:
        return FISH_INTEGRATION
    else:
        return BASH_INTEGRATION
