# Timesketch to DFIR-IRIS Sync Tool

Usage : 
```
python timesketch2iris.py --ts_sketch_id 2 --iris_case_id 1    
```

## 📌 Objectif du projet

Ce projet a pour objectif de faciliter et automatiser la synchronisation des événements identifiés comme **malveillants** ou **pertinents** dans la solution **[Timesketch](https://github.com/google/timesketch)** vers la plateforme **[DFIR-IRIS](https://www.dfir-iris.org/)**.

L’enjeu principal est d’**éviter la saisie manuelle** des données issues de l’analyse de timeline dans IRIS.

---

## 🎯 Cas d’usage

* Un analyste utilise **Timesketch** pour traiter une timeline et y identifie des événements suspects ou malveillants (tagués ou filtrés).
* Au lieu de recopier manuellement ces événements dans une investigation active dans **DFIR-IRIS**, cet outil permet de **les synchroniser automatiquement**.
* Cela permet de **centraliser les données de l'enquête** dans IRIS tout en capitalisant sur la puissance de traitement de Timesketch.

---

## ⚙️ Fonctionnalités principales

* 🔍 **Extraction automatique** des événements tagués "Starred" dans Timesketch
* 📤 **Injection directe** dans une investigation IRIS existante via l’API REST
* ✅ Gestion des doublons 
---

## 🧰 Technologies utilisées

* Python 3.x
* API Timesketch
* API DFIR-IRIS
* Librairies : `requests`, `json`, etc.

---

## 🚧 État du projet

> Ce projet est en cours de développement 

Les contributions sont les bienvenues ! Voir la section [Contribuer](#️contribuer) ci-dessous.
