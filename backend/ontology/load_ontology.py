from rdflib import Graph


GRAPH = Graph()

GRAPH.parse("./ontology/ontology.ttl", format="turtle")
GRAPH.parse("./ontology/store.ttl", format="turtle")
