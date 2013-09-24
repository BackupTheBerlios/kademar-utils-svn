 

#Print how to reinstall graphic card if errors
if [ -n "$(grep -Ei '*no screens found|No devices detected|Fatal server error.' /var/log/Xorg.0.log 2>/dev/null)" ]; then
    
    DESTI="$1"
    . $DESTI/etc/locale.conf
    case "$LANG" in
    ca_ES*)
      var_exec="executa"
      var_line='Si estàs aquí perquè hi ha hagut un problema (probablement has canviat la tarja gràfica), pots instal·lar els controladors, després de fer login, amb:'
    ;;
    es*)
      var_exec="ejecuta"
      var_line='Si estás aquí porque ha habido un problema (probablemente has cambiado la tarjeta gráfica), puedes instalar los controladores, después de hacer login, con:'
    ;;
    *)
      var_exec="run"
      var_line='If you are here because you had a problem (probably you changed graphic card), you can install graphic drivers, after login, with:'
    ;;
    esac

    echo "Kademar Linux \r (\l)
    
*******

$var_line
 
   - Nvidia Cards, $var_exec:  sudo install-nvidia-drivers
   - Ati    Cards, $var_exec:  sudo install-ati-drivers
   - Other  Cards, $var_exec:  sudo install-other-drivers

*******

"
fi