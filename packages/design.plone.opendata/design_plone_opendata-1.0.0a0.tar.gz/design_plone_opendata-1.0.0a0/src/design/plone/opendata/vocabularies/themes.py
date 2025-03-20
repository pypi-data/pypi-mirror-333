# flake8: noqa: E501

from . import dcatapit as resources
from plone.memoize import forever
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import importlib.resources
import rdflib


with importlib.resources.open_text(resources, "data-theme-filtered.rdf") as rdf_file:
    g = rdflib.Graph()
    g.parse(rdf_file, format="xml")


def get_triples(ref):
    return g.triples((ref, None, None))


@forever.memoize
def vocabulary_terms(lang):
    query = f"""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?ref ?name
        WHERE {{
            ?ref a skos:Concept ;
            skos:prefLabel ?name .
            FILTER (lang(?name) = "{lang}")
        }}
        ORDER BY ?name
        """
    return [(str(ref), str(name)) for (ref, name) in g.query(query)]


@provider(IVocabularyFactory)
class DataThemesVocabulary:
    def __call__(self, context):
        lang = context.Language() or "it"
        terms = [
            SimpleTerm(value=value, title=title)
            for (value, title) in vocabulary_terms(lang)
        ]
        return SimpleVocabulary(terms)
