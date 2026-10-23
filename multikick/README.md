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

## Reconstruire l'APK
    tools/build.sh Kick-v115.apk <keystore.p12> <mot_de_passe> <alias>
    # produit Kick-v115-ui.apk et Kick-v115-ui-cote-a-cote.apk

`Kick-v115-ui.apk` est signé avec une **nouvelle clé** (l'originale n'est pas disponible) :
il ne peut pas mettre à jour l'appli d'origine (Android refuse une autre clé). Utilise la variante ci-dessous, ou désinstalle l'ancienne version.

## Variante « côte à côte »
`Kick-v115-ui-cote-a-cote.apk` a un autre identifiant (`app.multikick.kic2`, nom « Kic2 ») : elle s'installe **à côté** de l'appli d'origine, sans désinstallation ni conflit de signature (mais sans reprendre ses réglages). Générée avec `tools/rename_package.py`.
