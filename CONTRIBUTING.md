# Contribuer à GNU Cadet World

Merci de contribuer à un répertoire mondial exact et utile.

## Signaler une information

Utilisez l’icône 🔄 du README ou une issue de correction / nouvelle organisation. Indiquez le pays ou territoire, le nom, le niveau national ou territorial, l’élément, les URL directes et une source institutionnelle qui permet de les authentifier. Un compte non trouvé ne doit pas être déclaré inexistant.

## Proposer une modification

1. Créez une branche depuis la version actuelle du dépôt.
2. Modifiez `data/organizations.json`. Conservez les identifiants existants; attribuez aux nouvelles lignes un identifiant CW unique et jamais réutilisé.
3. Renseignez les statuts `confirme_source_officielle`, `a_confirmer` ou `non_identifie` pour chaque plateforme. Un statut confirmé exige une source institutionnelle qui renvoie au compte exact. Ajoutez une date de revue et une note factuelle.
4. Exécutez `python scripts/directory.py`, puis `python scripts/directory.py --check` et `python scripts/check_links.py`.
5. Examinez le rapport réseau : une réponse HTTP réussie n’authentifie pas un compte. Ne supprimez pas une adresse sur la seule base d’un blocage automatique.
6. Ouvrez une pull request décrivant les modifications et leurs preuves.

Ne modifiez pas directement le tableau généré. Ne publiez aucune coordonnée privée ni information personnelle concernant des mineurs. Respectez le [code de conduite](CODE_OF_CONDUCT.md). Les contributions au dépôt sont proposées sous sa [licence existante](LICENSE).
