# invenio-initial-theses-conversion

Data conversion from MarcXML to JSON


* Stažení dat:

```curl 'https://invenio.nusl.cz/search?ln=cs&p=&f=&action_search=Hledej&c=Vysoko%C5%A1kolsk%C3%A9+kvalifika%C4%8Dn%C3%AD+pr%C3%A1ce&rg=10&sc=0&of=xm' > /tmp/blah.xml```

* Vytištění dat v JSON:

```dojson -i /tmp/blah.xml -l marcxml do theses | json_pp -json_opt pretty,canonical```

* Zobrazení chybějících Marc políček, které ještě nebyly konvertovány do JSON

``` dojson -i /tmp/blah.xml -l marcxml missing theses```