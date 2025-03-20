# flake8: noqa: E501

from . import dcatapit as resources
from plone.memoize import forever
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import importlib.resources
import rdflib


# https://github.com/italia/daf-ontologie-vocabolari-controllati/blob/master/VocabolariControllati/licences/licences.csv
with importlib.resources.open_text(resources, "licences.rdf") as rdf_file:
    g = rdflib.Graph()
    g.parse(rdf_file, format="xml")


def get_license_ref(name):
    query = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcatapit: <http://dati.gov.it/onto/dcatapit#>
    SELECT ?concept
    WHERE {{
    ?concept a skos:Concept ;
            dcatapit:referenceDoc \"{name}\"^^<http://www.w3.org/2001/XMLSchema#anyURI> .
    }}"""
    refs = [ref for ref in g.query(query.format(name=name))]
    if refs:
        return refs[0].concept


def get_triples(ref):
    return g.triples((ref, None, None))


@forever.memoize
def vocabulary_terms(lang):
    query = f"""
        PREFIX dcatapit: <http://dati.gov.it/onto/dcatapit#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT ?ref ?name
        WHERE {{
            ?s dcatapit:referenceDoc ?ref ;
            foaf:name ?name .
            FILTER (lang(?name) = "{lang}")
        }}
        ORDER BY ?name
        """
    return [(str(ref), str(name)) for (ref, name) in g.query(query)]


@provider(IVocabularyFactory)
class LicensesVocabulary:
    def __call__(self, context):
        lang = context.Language() or "it"
        terms = [
            SimpleTerm(value=value, title=title)
            for (value, title) in vocabulary_terms(lang)
        ]
        return SimpleVocabulary(terms)
