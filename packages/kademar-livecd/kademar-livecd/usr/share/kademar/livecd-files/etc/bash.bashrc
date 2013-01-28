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


for i in a2ps awk bash bc bison cat colordiff cp csplit curl cut date df diff dir du enscript env expand fmt fold gperf gprof     grep grub head indent irb ld ldd less ln ls m4 md5sum mkdir mkfifo mknod man mv netstat nl nm objcopy objdump od paste patch pr ptx readelf rm rmdir sed seq sha{,1,224,256,384,512}sum shar sort split sudo strip tac tail tee texindex touch tr uname unexpand uniq units vdir wc wget who
do
   complete -cf $i
done



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
alias nano="nano -w -c"
alias mkdir="mkdir -p -v"
alias more="less"
alias grep='grep --color=auto'
alias change-to-utf8-filenames="convmv -r -f ISO-8859-1 -t UTF-8 --notest *"
# alias mplayer="mplayer -zoom"
# alias gmplayer="gmplayer -zoom"

# privileged access
if [ $UID -ne 0 ]; then
    alias sudo='sudo '
    alias scat='sudo cat'
    alias svim='sudo vim'
    alias root='sudo su'
    alias reboot='sudo reboot'
    alias halt='sudo halt'
    alias update='sudo pacman -Su'
    fi

export SPEECHD_ADDRESS=unix_socket:/var/run/speech-dispatcher/speechd.sock


#autocd  if you write   /etc  it will do  cd /etc
shopt -s autocd

#[ -r /usr/share/bash-completion/bash_completion   ] && . /usr/share/bash-completion/bash_completion
