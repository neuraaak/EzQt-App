# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [2.3.1] - 2025-07-27

### Modifié
- Mise à jour de la version et améliorations diverses

## [2.3.0] - 2025-07-26

### Ajouté
- Barre inférieure (bottom bar) pour l'interface utilisateur

## [2.2.1] - 2025-07-26

### Ajouté
- Système de traduction global avec support multi-langues
- Support pour l'anglais, français, espagnol et allemand
- API de traduction simple : `tr()`, `set_tr()`, `change_language()`
- Retraduction automatique des widgets lors du changement de langue

## [2.1.0] - 2025-07-26

### Ajouté
- Amélioration du panneau de paramètres
- Nouvelles fonctionnalités de configuration

## [2.0.5] - 2025-07-25

### Ajouté
- Widget MenuButton avec support des animations
- Amélioration de l'expérience utilisateur

## [2.0.4] - 2025-07-24

### Ajouté
- Script build/upload pour automatiser le processus de déploiement

### Modifié
- Exclusion du fichier .bat du package dans MANIFEST.in

## [2.0.3] - 2025-07-24

### Modifié
- Mise à jour générale de la version 2.0.3

## [2.0.2] - 2025-07-23

### Modifié
- Mise à jour de la version dans pyproject.toml et ezqt_app/__init__.py
- Amélioration de la configuration du projet

## [2.0.0] - 2025-07-23

### Ajouté
- Fichiers initiaux du projet
- Configuration complète avec .gitignore, LICENSE, MANIFEST.in, pyproject.toml
- Ressources et icônes pour l'application ezqt_app
- Structure de base du framework EzQt_App

### Modifié
- Mise à jour de pyproject.toml avec la configuration initiale

## [1.0.0] - 2025-07-23

### Ajouté
- Premier commit du projet
- Structure de base du framework EzQt_App
- Support de PySide6 pour les applications Qt modernes
- Système de thèmes clair/sombre
- Gestion automatique des ressources
- CLI `ezqt_init` pour l'initialisation de projets

---

## Types de modifications

- **Ajouté** : pour les nouvelles fonctionnalités
- **Modifié** : pour les changements dans les fonctionnalités existantes
- **Déprécié** : pour les fonctionnalités qui seront bientôt supprimées
- **Supprimé** : pour les fonctionnalités supprimées
- **Corrigé** : pour les corrections de bugs
- **Sécurité** : en cas de vulnérabilités corrigées 