################################################################################
# $Id: zshenv 47 2024-01-21 14:58:27 +0100 .m0rph $
################################################################################
# Note:
#  Be carful what to initialize here in .zshenv !!!
#  First law in zsh configuration is to keep .zshenv as small as possible,
#  since it is loaded for every single shell, i.e. not only for
#  interactive or login shells! Environment variables are also initialized
#  for non-interactive shells and that is every single shell script you write!
#  So keep in mind to initialize environment varliables you want to have set
#  for your interactive zsh session in .zshrc.
################################################################################
# MINGW64 stuff !!!
export LC_ALL=de_DE.UTF-8
export LC_CTYPE=de_DE.UTF-8
export LANG=DE

# oh-my-zsh home directory
export ZSH="/usr/share/zsh/.oh-my-zsh"


# And my additional PATH
mypath="$mypath:/path/to:/your/work/files"
export PATH="$mypath:$PATH"


WORDCHARS=${WORDCHARS//\/} # Don't consider certain characters part of the word

# hide EOL sign ('%')
PROMPT_EOL_MARK=""

# configure `time` format
TIMEFMT=$'\nreal\t%E\nuser\t%U\nsys\t%S\ncpu\t%P'


# EOF
