################################################################################
# $Id: zshrc 37 2025-01-10 10:07:31 +0100 .m0rph $
################################################################################
# Description:
# ------------
#
# zsh configuration set, derived from my Kali schleppi without an oh-my-zsh
# installation. This configuration set is usable for all environments where
# I make use of my beloved Z-Shell, whether I have to install additional
# frameworks or not. (See zshenv ;-)
#
# I use different sets due to the fact, that I do a lot of things on the shell,
# even under Windows. Especially in my MSYS2 environment, or in virtual ones,
# opening a new shell can be VERY slow! So, we have to clearly decide, which
# features to use and what we do not really need.
#
# Have a lot of Fun ...
#
# .m0rph
#
# ------------------------------------------------------------------------------
# Note:
#  In order to enable syntax-highlighting, zsh-autosuggestions, or other
#  plugins not contained in .oh-my-zsh, check the zsh-users GitHub.
#
#  # cd /usr/share/zsh/plugins
#  # git clone https://github.com/zsh-users/zsh-autosuggestions
#  # git clone https://github.com/zsh-users/zsh-syntax-highlighting
#
################################################################################
# At first another default permission set ...
[[ "$OSID" = 'msys2' ]] || {
   # ... but not under Windows and MSYS2. It only has drawbacks !!!
   umask 0077
}

# We need some options directly at the beginning.
[[ -f ~/.zsh/zoptions ]] && source ~/.zsh/zoptions


# configure key keybindings
bindkey -v                                     # vim key bindings
bindkey ' ' magic-space                        # do history expansion on space
bindkey '^U' backward-kill-line                # ctrl + U
bindkey '^[[3;5~' kill-word                    # ctrl + Supr
bindkey '^[[3~' delete-char                    # delete
bindkey '^[[1;5C' forward-word                 # ctrl + ->
bindkey '^[[1;5D' backward-word                # ctrl + <-
bindkey '^[[5~' beginning-of-buffer-or-history # page up
bindkey '^[[6~' end-of-buffer-or-history       # page down
bindkey '^[[H' beginning-of-line               # home
bindkey '^[[F' end-of-line                     # end
bindkey '^[[Z' undo                            # shift + tab undo last action

## Lines configured by zsh-newuser-install
## End of lines configured by zsh-newuser-install
## The following lines were added by compinstall
#autoload -Uz compinit
#compinit
## End of lines added by compinstall
# enable completion features
zstyle :compinstall filename '~/.zshrc'
autoload -Uz compinit
compinit -d ~/.cache/zcompdump
zstyle ':completion:*:*:*:*:*' menu select
zstyle ':completion:*' auto-description 'specify: %d'
zstyle ':completion:*' completer _expand _complete
zstyle ':completion:*' format 'Completing %d'
zstyle ':completion:*' group-name ''
zstyle ':completion:*' list-colors ''
zstyle ':completion:*' list-prompt %SAt %p: Hit TAB for more, or the character to insert%s
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'
zstyle ':completion:*' rehash true
zstyle ':completion:*' select-prompt %SScrolling active: current selection at %p%s
zstyle ':completion:*' use-compctl false
zstyle ':completion:*' verbose true
zstyle ':completion:*:kill:*' command 'ps -u $USER -o pid,%cpu,tty,cputime,cmd'


# Do we work in a screen session?
scr=0
[[ ${(s.:.)TERM[1,6]} == 'screen' ]] && scr=1


# make less more friendly for non-text input files, see lesspipe(1)
[[ -x /usr/bin/lesspipe ]] && eval "$(SHELL=/bin/sh lesspipe)"


# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
force_color_prompt=yes


if [ -n "$force_color_prompt" ]; then
   if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
      # We have color support; assume it's compliant with Ecma-48
      # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
      # a case would tend to support setf rather than setaf.)
      color_prompt=yes
   else
      color_prompt=
   fi
fi


# The following block is surrounded by two delimiters.
# These delimiters must not be modified. Thanks.
# START KALI CONFIG VARIABLES
PROMPT_ALTERNATIVE=twoline
NEWLINE_BEFORE_PROMPT=yes
# STOP KALI CONFIG VARIABLES

ptitle=''
pfiller=''
psymbol=''
pactive='kprompt' # default prompt
[[ -f ~/.zsh/zsh_title ]]      && source ~/.zsh/zsh_title
[[ -f ~/.zsh/zsh_precmd ]]     && source ~/.zsh/zsh_precmd
[[ -f ~/.zsh/zsh_preexec ]]    && source ~/.zsh/zsh_preexec
[[ -f ~/.zsh/zsh_kprompt ]]    && source ~/.zsh/zsh_kprompt
[[ -f ~/.zsh/zsh_workprompt ]] && source ~/.zsh/zsh_workprompt
[[ -f ~/.zsh/zsh_ptsprompt ]]  && source ~/.zsh/zsh_ptsprompt
[[ -f ~/.zsh/zsh_zprompt ]]    && source ~/.zsh/zsh_zprompt
toggle_prompt(){
   pactive="$1"
   [[ "$pactive" == 'kprompt' ]] && {
   # This one we only have in kprompt
      if [ "$PROMPT_ALTERNATIVE" = oneline ]; then
         PROMPT_ALTERNATIVE=twoline
      else
         PROMPT_ALTERNATIVE=oneline
      fi
   }
   clear
   set_title
   precmd
   preexec
   "set_$pactive"
   zle reset-prompt
}
toggle_kprompt()    { toggle_prompt kprompt }
toggle_workprompt() { toggle_prompt workprompt }
toggle_ptsprompt()  { toggle_prompt ptsprompt }
toggle_zprompt()    { toggle_prompt zprompt }
zle -N toggle_kprompt
zle -N toggle_workprompt
zle -N toggle_ptsprompt
zle -N toggle_zprompt
bindkey ^K toggle_kprompt
bindkey ^W toggle_workprompt
bindkey ^P toggle_ptsprompt
bindkey ^Z toggle_zprompt


if [ "$color_prompt" = yes ]; then
   # override default virtualenv indicator in prompt
   VIRTUAL_ENV_DISABLE_PROMPT=1

   set_title
   precmd
   preexec
   "set_$pactive"

   # enable syntax-highlighting
   [[ -f $ZSH_PLUGINS/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]] && {
      . $ZSH_PLUGINS/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
      ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets pattern)
      ZSH_HIGHLIGHT_STYLES[default]=none
      ZSH_HIGHLIGHT_STYLES[unknown-token]=fg=white,underline
      ZSH_HIGHLIGHT_STYLES[reserved-word]=fg=cyan,bold
      ZSH_HIGHLIGHT_STYLES[suffix-alias]=fg=green,underline
      ZSH_HIGHLIGHT_STYLES[global-alias]=fg=green,bold
      ZSH_HIGHLIGHT_STYLES[precommand]=fg=green,underline
      ZSH_HIGHLIGHT_STYLES[commandseparator]=fg=blue,bold
      ZSH_HIGHLIGHT_STYLES[autodirectory]=fg=green,underline
      ZSH_HIGHLIGHT_STYLES[path]=bold
      ZSH_HIGHLIGHT_STYLES[path_pathseparator]=
      ZSH_HIGHLIGHT_STYLES[path_prefix_pathseparator]=
      ZSH_HIGHLIGHT_STYLES[globbing]=fg=blue,bold
      ZSH_HIGHLIGHT_STYLES[history-expansion]=fg=blue,bold
      ZSH_HIGHLIGHT_STYLES[command-substitution]=none
      ZSH_HIGHLIGHT_STYLES[command-substitution-delimiter]=fg=magenta,bold
      ZSH_HIGHLIGHT_STYLES[process-substitution]=none
      ZSH_HIGHLIGHT_STYLES[process-substitution-delimiter]=fg=magenta,bold
      ZSH_HIGHLIGHT_STYLES[single-hyphen-option]=fg=green
      ZSH_HIGHLIGHT_STYLES[double-hyphen-option]=fg=green
      ZSH_HIGHLIGHT_STYLES[back-quoted-argument]=none
      ZSH_HIGHLIGHT_STYLES[back-quoted-argument-delimiter]=fg=blue,bold
      ZSH_HIGHLIGHT_STYLES[single-quoted-argument]=fg=yellow
      ZSH_HIGHLIGHT_STYLES[double-quoted-argument]=fg=yellow
      ZSH_HIGHLIGHT_STYLES[dollar-quoted-argument]=fg=yellow
      ZSH_HIGHLIGHT_STYLES[rc-quote]=fg=magenta
      ZSH_HIGHLIGHT_STYLES[dollar-double-quoted-argument]=fg=magenta,bold
      ZSH_HIGHLIGHT_STYLES[back-double-quoted-argument]=fg=magenta,bold
      ZSH_HIGHLIGHT_STYLES[back-dollar-quoted-argument]=fg=magenta,bold
      ZSH_HIGHLIGHT_STYLES[assign]=none
      ZSH_HIGHLIGHT_STYLES[redirection]=fg=blue,bold
      ZSH_HIGHLIGHT_STYLES[comment]=fg=black,bold
      ZSH_HIGHLIGHT_STYLES[named-fd]=none
      ZSH_HIGHLIGHT_STYLES[numeric-fd]=none
      ZSH_HIGHLIGHT_STYLES[arg0]=fg=cyan
      ZSH_HIGHLIGHT_STYLES[bracket-error]=fg=red,bold
      ZSH_HIGHLIGHT_STYLES[bracket-level-1]=fg=blue,bold
      ZSH_HIGHLIGHT_STYLES[bracket-level-2]=fg=green,bold
      ZSH_HIGHLIGHT_STYLES[bracket-level-3]=fg=magenta,bold
      ZSH_HIGHLIGHT_STYLES[bracket-level-4]=fg=yellow,bold
      ZSH_HIGHLIGHT_STYLES[bracket-level-5]=fg=cyan,bold
      ZSH_HIGHLIGHT_STYLES[cursor-matchingbracket]=standout
   }
else
   PROMPT='%n@%m:%~%(#.#.$) '
fi
unset color_prompt force_color_prompt


# enable color support of ls, less and man, and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
   [[ -r ~/.dircolors ]] && \
      eval "$(dircolors -b ~/.dircolors)" || \
      eval "$(dircolors -b)"

   zcolors=1

   # fix ls color for folders with 777 permissions
   export LS_COLORS="$LS_COLORS:ow=30;44:"

   export LESS_TERMCAP_mb=$'\E[1;31m'  # begin blink
   export LESS_TERMCAP_md=$'\E[1;36m'  # begin bold
   export LESS_TERMCAP_me=$'\E[0m'     # reset bold/blink
   export LESS_TERMCAP_so=$'\E[01;33m' # begin reverse video
   export LESS_TERMCAP_se=$'\E[0m'     # reset reverse video
   export LESS_TERMCAP_us=$'\E[1;32m'  # begin underline
   export LESS_TERMCAP_ue=$'\E[0m'     # reset underline

   # Take advantage of $LS_COLORS for completion as well
   zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
   zstyle ':completion:*:*:kill:*:processes' list-colors '=(#b) #([0-9]#)*=0=01;31'
fi


# Default tools
(( ${+BROWSER} )) || export BROWSER="w3m"
(( ${+MAILER} ))  || export MAILER="mutt"
(( ${+EDITOR} ))  || export EDITOR="vim"
(( ${+PAGER} ))   || export PAGER="less"


## enable auto-suggestions based on the history
if [ -f $ZSH_PLUGINS/zsh-autosuggestions/zsh-autosuggestions.zsh ]; then
   . $ZSH_PLUGINS/zsh-autosuggestions/zsh-autosuggestions.zsh
   # change suggestion color
   ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=#999'
fi

### We don't need that under Linux !!!
[[ "$OSID" = 'msys2' ]] && {
   # Load oh-my-zsh plugins.
   source $ZSH/oh-my-zsh.sh
   plugins=(
     command-not-found
     git
   )
}


# Preparing my environment, loading zscripts. We do this at the end, because
# maybe we're loading oh-my-zsh settings here and do not need any disturbing
# settings from oh-my-zsh (i.e. not wanted aliases)
[[ -f ~/.zsh/zaliases ]]   && source ~/.zsh/zaliases
[[ -f ~/.zsh/zgaliases ]]  && source ~/.zsh/zgaliases
[[ -f ~/.zsh/zfunctions ]] && source ~/.zsh/zfunctions
[[ -f ~/.zsh/zdhashes ]]   && source ~/.zsh/zdhashes
#[[ -f ~/.zsh/ztest ]] && source ~/.zsh/ztest


# Increase Mozilla performance a bit.
export MOZ_DISABLE_PANGO=1


# EOF
