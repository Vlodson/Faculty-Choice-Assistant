from typing import Dict
import re

from rdflib.query import Result

from backend.ontology.load_ontology import GRAPH


def __apply_prefix(query: str) -> str:
    """
    Fallback function if there is no edu prefix
    """
    return (
        (
            r"PREFIX edu: <YOUR_ONTOLOGY.TTL_FILE_PATH_HERE>"
            + query
        )
        if r"PREFIX edu: <YOUR_ONTOLOGY.TTL_FILE_PATH_HERE>"
        not in query
        else query
    )


def __fix_prefix(query: str) -> str:
    return query.replace("ont", "edu")


def apply_query(query: str) -> Result:
    print(query)
    return GRAPH.query(query_object=query)


def __readable_property_name(prop: str) -> str:
    camel_regex = r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])"
    return re.sub(camel_regex, " ", prop).capitalize()


def __clean_property_value(val: str) -> str:
    """
    Fallback function for if a class comes through
    """
    return val.split("#")[-1]


# keep in mind there can be ASK and SELECT queries
# ASK returns a boolean to your question, SELECT returns a Result with ResultRows
def query_results_to_table(results: Result) -> Dict:
    return {
        __readable_property_name(str(key)): [
            __clean_property_value(str(row[key])) for row in results
        ]
        for key in results.__dict__["vars"]
    }
