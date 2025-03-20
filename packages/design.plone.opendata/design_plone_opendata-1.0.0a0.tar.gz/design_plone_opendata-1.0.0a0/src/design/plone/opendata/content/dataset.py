# flake8: noqa: E501
# from collective.volto.blocksfield.field import BlocksField
# from design.plone.contenttypes.interfaces import IDesignPloneContentType
from design.plone.opendata import _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer


class IOpendataDataset(model.Schema):
    # https://www.dati.gov.it/sites/default/files/2020-02/linee-guida-cataloghi-dati-profilo-dcat-ap-it-2.pdf
    # DATASET ( “M” indica che la classe è obbligatoria, “R” indica che è raccomandata e “O” indica che è opzionale)
    # Dataset identificativo M --> url o UID ?
    # Dataset titolo M --> plone.basic
    # Dataset descrizione M  --> plone.basic (TODO: deve essere obbligatorio? Oppure lo pubblichiamo ripetendo
    #                                               il titolo, se non compilato, nell'RDF)

    # Dataset data di rilascio
    # Volto fa casino con la timezone, metto per ora una data anzichè un dattetime
    release_date = schema.Date(title=_("Data di rilascio"), required=False)

    # Dataset data ultima modifica M  --> dato redazionale !!!
    # Volto fa casino con la timezone, metto per ora una data anzichè un dattetime
    last_update_date = schema.Date(title=_("Data di ultima modifica"), required=True)

    # Dataset temi M
    themes = schema.Set(
        title=_("Temi"),
        description=_(
            "I temi attraverso cui classificare il Dataset. La proprietà lega l’oggetto "
            "Dataset a uno o più oggetti di tipo skos:Concept "
            "(specificato mediante un URI - Uniform Resource Identifier)"
        ),
        value_type=schema.Choice(
            title=_("Temi"), vocabulary="design.plone.opendata.themes"
        ),
    )
    # Dataset sottotema R
    # La sottocategoria in cui può essere classificato il Dataset.
    # La proprietà lega l’oggetto (dominio)
    # Dataset a uno o più oggetti (codominio) di tipo skos:Concept (specificato mediante un URI - Uniform Resource Identifier)
    # dct.subject

    # Non implementato

    # Dataset titolare M
    # TODO: definire entità di tipo Agent e un vocabolario per cercarli, il valore è la url
    # rightsHolder = schema.Choice(..., vocabulary="design.plone.opendata.agents")
    # possiamo puntare ad una unità organizzativa però ...
    rightsHolder = RelationList(
        title=_(
            "opendata_holder_label",
            default="Titolare",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_("Titolare"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    form.widget(
        "rightsHolder",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )

    # Dataset frequenza di aggiornamento M
    frequency = schema.Choice(
        title=_("Frequenza di aggiornamento"),
        vocabulary="design.plone.opendata.frequencies",
    )

    # XXX: questi sono le url dei file allegati
    # Dataset distribuzione M (nel caso di dati aperti)

    # TODO:
    # Dataset punto di contatto R
    # Dataset editore R
    # Dataset autore O
    # Dataset versione O

    # Dataset pagina di accesso O
    # Dataset lingua O
    # Dataset parole chiave O
    # Dataset dataset correlato O
    # Dataset estensione temporale O
    # Dataset copertura geografica O
    # Dataset conformità O

    # Distribuzione (il file avrebbe bisogno anche di questi metadati)

    # Distribuzione formato M -- ricavato dal mime_type
    # Distribuzione URL di accesso M -- url @@download/file

    # Distribuzione licenza M
    # TODO: questa la mettiamo temporaneamente sul dataset, poi valutiamo di spostarla sul file
    #       ma anche per la redazione credo sia più semplice efficace aaverla qui
    license = schema.Choice(
        title=_("Licenza"), vocabulary="design.plone.opendata.licenses"
    )

    # Distribuzione descrizione R -- plone.basic
    # Distribuzione titolo O -- plone.basic
    # Distribuzione URL di download O
    # Distribuzione data ultima modifica O
    # Distribuzione dimensione in byte O


@implementer(IOpendataDataset)
class OpendataDataset(Container):
    """ """
