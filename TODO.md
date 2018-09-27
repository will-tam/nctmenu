 - Création d'un fichier de config., si non existant.
 - Suivant option, reconfig.
 - Vérif. des prog. tiers :
   - /usr/bin/binstats <<--- doit être soit éxecutable par M. Toutlemonde, soit via sudo (!! attention au mot de passe !!)
   - A voir au fil de la prog
 - Vérif des exécutables dans d'autres répertoires que ceux vérifiés par binstats.
 - Pour chaque exécutable, vérif de son man. Sinon récup de son help.
 - Vérification si le programme n'est pas graphique (exécutable dans le répertoire X11, présent dans le menu de type Freedesktop ou autre, le magique).
 - Affichage du résultat.

 - Nettoyage code :
    - import non utilisés
    - print() non pertinant
    - commentaires non pertinants

-------------------------

 - imports :
     - sys (https://docs.python.org/3.5/library/sys.html?highlight=sys#module-sys)
     - os (https://docs.python.org/3.5/library/os.html?highlight=os#module-os)
     - hashlib (https://docs.python.org/3.5/library/hashlib.html?highlight=hashlib#module-hashlib)
     - re (https://docs.python.org/3.5/library/re.html?highlight=re#module-re)
     - subprocess (https://docs.python.org/3.5/library/subprocess.html?highlight=subprocess#subprocess.Popen)
     - shlex (https://docs.python.org/3.5/library/shlex.html#shlex.split)
     - docopt (3rd party - mboersma) || argparse (https://docs.python.org/3.5/library/argparse.html?highlight=argparse#module-argparse)
     - curses-menu (3rd party - pmbarrett314) || ncurse (Si création de 0 - https://docs.python.org/3.5/library/curses.html?highlight=ncurse)
