 - Création d'un fichier de config., si non existant.
 - Suivant options, reconfig.
 - Vérif. des prog. tiers :
   - /usr/bin/binstats <<--- doit être soit éxecutable par M. Toutlemonde, soit via sudo (!! attention au mot de passe !!)
   - A voir au fil de la prog
 - Vérif des exécutables dans d'autres répertoires que ceux vérifiés par binstats.
 - Pour chaque exécutable, vérif de son man. Sinon récup de son help.
 - Vérification si le programme n'est pas graphique (exécutable dans le répertoire X11, présent dans le menu de type Freedesktop ou autre, le magique).
 - Affichage du résultat.

-------------------------

 - import :
   - hashlib
   - argparse
   - pycurl (3rd party)
