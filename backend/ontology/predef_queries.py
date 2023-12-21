UNIVERSITIES = """
PREFIX edu: <file:///C:/Users/vlada/Desktop/Faks/SW/source/ontology/ontology.ttl#>
SELECT ?universityName ?city ?country
WHERE {
  ?university rdf:type edu:University ;
               edu:isNamed ?universityName ;
               edu:isInCity ?city ;
               edu:isInCountry ?country .
}
"""

FACULTIES_IN_NOVI_SAD = """
PREFIX edu: <file:///C:/Users/vlada/Desktop/Faks/SW/source/ontology/ontology.ttl#>
SELECT ?facultyName ?facultyStreet
WHERE {
  ?university rdf:type edu:University ;
               edu:isInCity "Novi Sad" .
  ?faculty rdf:type edu:Faculty ;
           edu:FacultyisPartOf ?university ;
           edu:isNamed ?facultyName ;
           edu:isOnStreet ?facultyStreet .
}
"""

FTN_NS_KNOWLEDGE_AREAS = """
PREFIX edu: <file:///C:/Users/vlada/Desktop/Faks/SW/source/ontology/ontology.ttl#>
SELECT ?knowledgeAreaName
WHERE {
  ?faculty rdf:type edu:Faculty ;
           edu:isNamed "Fakultet tehnickih nauka u Novom Sadu" ;
           edu:FacultyTeaches ?knowledgeArea .

  ?knowledgeArea rdf:type edu:KnowledgeArea ;
           edu:isNamed ?knowledgeAreaName .
}
"""
