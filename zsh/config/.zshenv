################################################################################
# $Id: zshenv 48 2025-01-10 08:39:43 +0100 .m0rph $
################################################################################
# At first we need to determine which system we are on !!!
OSID=$(/usr/bin/grep '^ID=' /etc/os-release | /usr/bin/awk -F'=' '{ print $2 }')

[[ "$OSID" = 'msys2' ]] && {

	# MINGW64 stuff !!!
   export LC_ALL=de_DE.UTF-8
   export LC_CTYPE=de_DE.UTF-8
   export LANG=DE

   # oh-my-zsh home directory
   export ZSH='/usr/share/zsh/.oh-my-zsh'
   export ZSH_PLUGINS="$ZSH/plugins"
   export ENABLE_CORRECTION='true'
   export CASE_SENSITIVE='true'

   # And my additional PATH
   mypath='/c/.cmd:/c/.man:/c/.pwsh:/c/Users/m0rph/.ssh:/c/Users/m0rph/.gnupg'
   mypath="$mypath:/d/shell/zsh/:/d/shell/powershell"
   mypath="$mypath:/d/python:/d/perl:/d/javascript"
   export PATH="$mypath:$PATH"
} || {
   # under linux there is no need for oh-my-zsh
   export ZSH='/usr/share'
   export ZSH_PLUGINS=$ZSH

   # but yes, we need some additional PATH information
   mypath="$HOME/scripts:$HOME/.ssh:$HOME/.gnupg"
   export PATH="$mypath:$PATH"
}


# History mechanism
HISTFILE=~/.zhistory
HISTSIZE=1000
SAVEHIST=2000
HIST_STAMPS="yyyy-mm-dd"


# Don't consider certain characters part of the word
WORDCHARS=${WORDCHARS//\/}

# hide EOL sign ('%')
PROMPT_EOL_MARK=""

# configure `time` format
TIMEFMT=$'\nreal\t%E\nuser\t%U\nsys\t%S\ncpu\t%P'

# EOF
