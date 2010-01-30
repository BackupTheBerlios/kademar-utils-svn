service system/kademar-mounter {
	need = system/initial system/mountfs;
	script start = {

		echo "WOW IS WOOORKIIING!!! LOOOL"

		for i in `grep /dev/ /etc/fstab | awk ' { print $2 } ' `
		do
		# 	echo $i
			case "$i" in
				'/mnt/'*)
				;;
				/)
				;;
				'none')
				;;
				*)
				mount -rw $i
				;;
			esac
		done
		echo hola > /JODER_FUNCIONA
		exit 0
	};
}
