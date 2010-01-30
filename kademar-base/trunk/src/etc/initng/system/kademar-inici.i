service system/kademar-inici {
	need = system/initial system/mountfs;
	script start = {

		echo "Loading kademar-installed"
		sh /etc/init.d/kademar-installed
		exit 0
	};
}
