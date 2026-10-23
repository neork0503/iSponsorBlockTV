# MultiKick – interface mobile & tablette (v115)

Fichiers modifiés par rapport à `Kick-v115.apk` : `assets/home.html` et `assets/player.html`
(l'interface de l'appli est une WebView). Le code Java (`classes.dex`) n'a pas été touché.

## Ce qui change
- **Barre de navigation** : ancrée en bas (opaque) au lieu de flotter par-dessus les cartes ; en **paysage** (téléphone et tablette) elle devient un **rail vertical à gauche**, la hauteur reste au contenu.
- **Vignettes de live** : compteur + durée groupés en haut à gauche, bouton « bloquer » en haut à droite, « + Multi » seul en bas à droite (plus d'éléments empilés).
- **Grilles** : 2 colonnes en téléphone paysage, 3-4 sur tablette ; contenu centré sur tablette portrait.
- **Mini-lecteur** : posé au-dessus de la barre de navigation.
- **Titres de section** : bouton « Actualiser » discret, texte des favoris aligné.
- **Lecteur** (`player.html`) : commandes réduites à **une seule barre fine** (⏪30 · ⏯ · 10⏩ · qualité · barre de progression · spectateurs · EN DIRECT · ⋯). Les actions rares (plein écran, MultiKick, choisir un live, profil, infos) sont repliées dans le menu **⋯**. Toucher « EN DIRECT » quand on est en retard revient au direct. Plus de chevauchement entre le nombre de spectateurs et « EN DIRECT ».

- **Icône** : logo Kick (K vert en blocs sur fond noir), voir `tools/patch_icon.py`.

## Refonte 2026 (accueil)
- **Barre du haut** : logo Kick, recherche, bouton Multi (avec compteur) ; elle se masque en défilant vers le bas.
- **Raccourcis en tuiles** (Lives, Rediffs, Clips, Drops), titres de section avec liseré d'accent, catégories avec le titre sur l'image, vignettes avec dégradé et point « live » rouge.
- **Squelettes de chargement** à la place des « Chargement… ».
- **Récemment regardés** : les dernières chaînes ouvertes (effaçable).
- **Dernières recherches** sous la barre de recherche.
- **Tirer vers le bas pour actualiser**, bouton « haut de page », bandeau « Hors connexion », retour haptique sur la barre du bas.
- **Profil › Apparence** : 6 couleurs d'accent (vert Kick, cyan, violet, rose, orange, blanc), cartes grandes ou compactes, effacer l'historique.
- Le mini-lecteur ne se pose plus jamais sur la barre de navigation.

## Chat (refait)
- **Chat commun du multi** (`mix.html`) : texte lisible (14 px, réglable A−/A+), barre fixe avec une **puce par chaîne** (couleur, état de connexion ; toucher = masquer/afficher cette chaîne, ou relancer si la connexion est tombée), **heure** en option, **pause**, bouton « ↓ N nouveaux messages » quand on remonte, **badges** (modo, VIP, abonné, streamer…), **réponses** (↪ @pseudo). Les connexions sont **réessayées sans limite** (avant : abandon définitif après 5 échecs). Réglages mémorisés.
- **Chat d'un live** : barre d'outils (A−/A+, recharger, masquer en grand écran), écran de chargement, message d'erreur avec « Réessayer » (chat vide ou page de vérification), hauteur qui suit le clavier (`dvh`). En **portrait**, la page remonte pour que le chat remplisse tout le reste de l'écran (la zone de saisie reste visible). En **paysage sur téléphone**, vidéo à gauche et chat à droite (comme sur tablette).
- Messages d'état de l'accueil (suivis indisponibles, aucun favori…) : petites cartes sobres.

## Vérifications (automatiques, téléphone/tablette, portrait/paysage)
- Aucun bouton recouvert par un autre élément, aucune zone de toucher trop petite, aucun débordement horizontal, sur tous les écrans (accueil, parcourir, suivis, profil, lives, rediffs, clips, drops, favoris, bloquées, catégorie, créateur, chaîne).
- 43 scénarios réussis sur chacun des 4 formats : navigation, tuiles, puces de langue, cartes, + Multi, bloquer, profil créateur, recherche et historique, apparence, onglets de la chaîne, et toutes les commandes du lecteur.
- Correctifs issus de ces tests : la poignée de hauteur du lecteur recouvrait ses boutons du bas (téléphone portrait) → bande dédiée sous la vidéo ; le menu « ⋯ » du lecteur dépassait du cadre → grille de tuiles plein cadre ; ajout d'un bouton « ← Retour » dans ce menu ; zones de toucher agrandies (noms de streamers, « Tout voir »).

## Reconstruire l'APK
    tools/build.sh Kick-v115.apk <keystore.p12> <mot_de_passe> <alias>
    # produit Kick-v115-ui.apk et Kick-v115-ui-cote-a-cote.apk

`Kick-v115-ui.apk` est signé avec une **nouvelle clé** (l'originale n'est pas disponible) :
il ne peut pas mettre à jour l'appli d'origine (Android refuse une autre clé). Utilise la variante ci-dessous, ou désinstalle l'ancienne version.

## Variante « côte à côte »
`Kick-v115-ui-cote-a-cote.apk` a un autre identifiant (`app.multikick.kic2`, nom « Kic2 ») : elle s'installe **à côté** de l'appli d'origine, sans désinstallation ni conflit de signature (mais sans reprendre ses réglages). Générée avec `tools/rename_package.py`.
