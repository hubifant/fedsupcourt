# fedsupcourt
For analysing the use of international law at the _Federal Supreme Court of Switzerland_.


## Setup
### Conda Environment
Install [Anaconda or Miniconda](https://www.continuum.io/downloads) and use Conda for installing all the necessary libraries.

1. For creating the environment, navigate to the project directory and execute `conda env create -f environment.yml`.
2. Activate it: `source activate fedsupcourt_env`.

[More](http://conda.pydata.org/docs/using/envs.html) about managing Conda environments...


### Database
[Install MongoDB](https://www.mongodb.com/download-center) and start the [mongod process](https://docs.mongodb.com/manual/tutorial/manage-mongodb-processes/?): `mongod --dbpath path/to/dataDir`


### Further...
Make sure that the locales `de_CH.utf8`, `fr_CH.utf8`, `it_CH.utf8` are installed.


## References
### Federal Supreme Court of Switzerland
- [The Court's Homepage](https://www.bger.ch/)
- [Court Organisation](http://www.bger.ch/gerichtsorganisation.pdf)
- [Jurivoc](http://www.bger.ch/index/juridiction/jurisdiction-inherit-template/jurisdiction-jurivoc-home/jurisdiction-jurivoc.htm): a trilingual thesaurus (De, Fr, It) of the Federal Supreme Court's social law department.


### Rulings
- [Index of all rulings of the Federal Supreme Court](http://relevancy.bger.ch/cgi-bin/IndexCGI?lang=de)
- [Entscheidungen des Schweizerischen Bundesgerichts (Wikipedia)](https://de.wikipedia.org/wiki/Entscheidungen_des_Schweizerischen_Bundesgerichts)
- [Nummerierung der Dossiers ab 2007 (BGG)](http://www.bger.ch/uebersicht_numm_dossiers_internet_d_ab_2007.pdf)
- [Relevante Urteile des Bundesgerichts finden: Urteile mit Dossiernummer finden](www.eurospider.com/fileadmin/pdf/SucheMitDossierNummer.pdf)


### International Law
- [Index of all International Laws concerning Switzerland](https://www.admin.ch/opc/de/classified-compilation/international.html)
- [Zitierregeln (Citing Rules)](http://www.bger.ch/01_zitierregeln_d.pdf)
