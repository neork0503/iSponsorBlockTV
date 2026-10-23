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

## Reconstruire l'APK
    python3 tools/repack.py Kick-v115.apk unsigned.apk assets
    # signature v1 (jarsigner) puis v2 :
    python3 tools/v2sign.py v1.apk Kick-v115-ui.apk <keystore.p12> <mot_de_passe>

`Kick-v115-ui.apk` est signé avec une **nouvelle clé** (l'originale n'est pas disponible) :
désinstalle l'ancienne version avant d'installer celle-ci (Android refuse une mise à jour signée avec une autre clé).
