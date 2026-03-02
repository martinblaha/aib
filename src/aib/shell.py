"""Shell integration script generator for aib."""

BASH_INTEGRATION = '''\
# aib — AI in Bash shell integration
# Add to ~/.bashrc or ~/.bash_profile
aib() {
  local cmd
  cmd=$(_aib "$@") || return $?
  if [[ -n "$cmd" ]]; then
    READLINE_LINE="$cmd"
    READLINE_POINT=${#cmd}
  fi
}
'''

ZSH_INTEGRATION = '''\
# aib — AI in Bash shell integration
# Add to ~/.zshrc
aib() {
  local cmd
  cmd=$(_aib "$@") || return $?
  [[ -n "$cmd" ]] && print -z "$cmd"
}
'''

FISH_INTEGRATION = '''\
# aib — AI in Bash shell integration
# Add to ~/.config/fish/config.fish
function aib
  set cmd (_aib $argv) || return $status
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
