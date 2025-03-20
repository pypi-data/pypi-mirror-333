# flake8: noqa: E501

# from design.plone.opendata import _
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


# https://op.europa.eu/web/eu-vocabularies/dataset/-/resource?uri=http://publications.europa.eu/resource/dataset/frequency

# import xml.etree.ElementTree as ET
# file_path = "/mnt/data/frequencies.xml"
# tree = ET.parse(file_path)
# root = tree.getroot()
# records = []
# for record in root.findall("record"):
#     record_id = record.get("id")
#     authority_code = record.find("authority-code").text if record.find("authority-code") is not None else None
#     label = None
#     for label in record.findall(".//lg.version[@lg='ita']"):
#         label = label.text
#         break  # Prende solo la prima occorrenza
#     records.append({
#         "record_id": record_id,
#         "authority_code": authority_code,
#         "label": label
#     })

FREQUENCIES = [
    {"record_id": "FRQ018", "authority_code": "UNKNOWN", "label": "sconosciuta"},
    {"record_id": "FRQ001", "authority_code": "TRIENNIAL", "label": "triennale"},
    {"record_id": "FRQ002", "authority_code": "BIENNIAL", "label": "biennale"},
    {"record_id": "FRQ003", "authority_code": "ANNUAL", "label": "annuale"},
    {"record_id": "FRQ004", "authority_code": "ANNUAL_2", "label": "semestrale"},
    {
        "record_id": "FRQ005",
        "authority_code": "ANNUAL_3",
        "label": "tre volte all'anno",
    },
    {"record_id": "FRQ006", "authority_code": "QUARTERLY", "label": "trimestrale"},
    {"record_id": "FRQ007", "authority_code": "BIMONTHLY", "label": "bimestrale"},
    {"record_id": "FRQ008", "authority_code": "MONTHLY", "label": "mensile"},
    {"record_id": "FRQ009", "authority_code": "MONTHLY_2", "label": "bimensile"},
    {"record_id": "FRQ010", "authority_code": "BIWEEKLY", "label": "quindicinale"},
    {
        "record_id": "FRQ011",
        "authority_code": "MONTHLY_3",
        "label": "tre volte al mese",
    },
    {"record_id": "FRQ012", "authority_code": "WEEKLY", "label": "settimanale"},
    {"record_id": "FRQ013", "authority_code": "WEEKLY_2", "label": "bisettimanale"},
    {
        "record_id": "FRQ014",
        "authority_code": "WEEKLY_3",
        "label": "tre volte a settimana",
    },
    {"record_id": "FRQ015", "authority_code": "DAILY", "label": "quotidiana"},
    {
        "record_id": "FRQ016",
        "authority_code": "UPDATE_CONT",
        "label": "in continuo aggiornamento",
    },
    {"record_id": "FRQ017", "authority_code": "IRREG", "label": "irregolare"},
    {"record_id": "FRQ019", "authority_code": "OTHER", "label": "altro"},
    {
        "record_id": "FRQ020",
        "authority_code": "DAILY_2",
        "label": "due volte al giorno",
    },
    {"record_id": "FRQ021", "authority_code": "CONT", "label": "continua"},
    {"record_id": "FRQ022", "authority_code": "NEVER", "label": "mai"},
    {
        "record_id": "FRQ023",
        "authority_code": "QUADRENNIAL",
        "label": "ogni quattro anni",
    },
    {
        "record_id": "FRQ024",
        "authority_code": "QUINQUENNIAL",
        "label": "ogni cinque anni",
    },
    {"record_id": "FRQ025", "authority_code": "HOURLY", "label": "ogni ora"},
    {"record_id": "FRQ026", "authority_code": "DECENNIAL", "label": "decennale"},
    {"record_id": "FRQ027", "authority_code": "BIHOURLY", "label": "ogni due ore"},
    {"record_id": "FRQ028", "authority_code": "TRIHOURLY", "label": "ogni tre ore"},
    {"record_id": "FRQ029", "authority_code": "BIDECENNIAL", "label": "bidecennale"},
    {"record_id": "FRQ030", "authority_code": "TRIDECENNIAL", "label": "tridecennale"},
    {"record_id": "FRQ031", "authority_code": "NOT_PLANNED", "label": "non previsto"},
    {
        "record_id": "FRQ032",
        "authority_code": "AS_NEEDED",
        "label": "in base alla necessità",
    },
    {"record_id": "FRQ033", "authority_code": "15MIN", "label": "ogni quindici minuti"},
    {"record_id": "FRQ034", "authority_code": "30MIN", "label": "ogni trenta minuti"},
    {"record_id": "FRQ035", "authority_code": "12HRS", "label": "ogni dodici ore"},
    {"record_id": "FRQ036", "authority_code": "10MIN", "label": "ogni dieci minuti"},
    {"record_id": "FRQ037", "authority_code": "1MIN", "label": "ogni minuto"},
    {"record_id": "FRQ038", "authority_code": "5MIN", "label": "ogni cinque minuti"},
]


@provider(IVocabularyFactory)
class DataFrequenciesVocabulary:
    def __call__(self, context):
        terms = [
            SimpleTerm(
                value=f"http://publications.europa.eu/resource/authority/frequency/{row['authority_code']}",
                title=row["label"],
            )
            for row in FREQUENCIES
        ]
        return SimpleVocabulary(terms)
