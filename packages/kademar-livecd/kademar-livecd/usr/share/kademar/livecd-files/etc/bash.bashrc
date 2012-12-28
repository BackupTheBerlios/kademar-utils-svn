#
# /etc/bash.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

PATH="/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin"
export PATH

PS1='[\u@\h \W]\$ '
PS2='> '
PS3='> '
PS4='+ '

case ${TERM} in
  xterm*|rxvt*|Eterm|aterm|kterm|gnome*)
    PROMPT_COMMAND=${PROMPT_COMMAND:+$PROMPT_COMMAND; }'printf "\033]0;%s@%s:%s\007" "${USER}" "${HOSTNAME%%.*}" "${PWD/#$HOME/~}"'
                                                        
    ;;
  screen)
    PROMPT_COMMAND=${PROMPT_COMMAND:+$PROMPT_COMMAND; }'printf "\033_%s@%s:%s\033\\" "${USER}" "${HOSTNAME%%.*}" "${PWD/#$HOME/~}"'
    ;;
esac

export EDITOR=nano

#Alias Zone
alias which="type -path"
alias where="type -all"
alias ll="ls -l --color=auto"
alias l="ls -a --color=auto"
alias ..="cd .."
alias rm="rm -i"
alias mv="mv -i"
alias cp="cp -i"
alias la="ls -la --color=auto"
alias ls="ls --color=auto"
alias cd..="cd .."
alias grep="grep --colour=auto"
alias change-to-utf8-filenames="convmv -r -f ISO-8859-1 -t UTF-8 --notest *"
# alias mplayer="mplayer -zoom"
# alias gmplayer="gmplayer -zoom"

export SPEECHD_ADDRESS=unix_socket:/var/run/speech-dispatcher/speechd.sock

[ -r /usr/share/bash-completion/bash_completion   ] && . /usr/share/bash-completion/bash_completion
