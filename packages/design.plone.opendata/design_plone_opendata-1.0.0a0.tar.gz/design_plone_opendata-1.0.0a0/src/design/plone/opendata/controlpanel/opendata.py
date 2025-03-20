from design.plone.opendata import _
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope import schema
from zope.component import adapter
from zope.interface import Interface


# from plone.schema.email import Email


class IControlPanel(Interface):
    org_email = schema.TextLine(
        title=_("Email Organizzazione"),
        required=True,
        max_length=1024,
    )
    org_title = schema.TextLine(
        title=_("Nome Organizzazione"),
        required=True,
        max_length=1024,
    )
    catalog_title = schema.TextLine(
        title=_("Titolo Catalogo"),
        required=True,
        max_length=1024,
    )
    catalog_description = schema.Text(
        title=_("Descrizione Catalogo"),
        required=True,
        max_length=4096,
    )
    catalog_homepage = schema.TextLine(
        title=_("Homepage Catalogo"),
        required=False,
        max_length=1024,
    )
    catalog_issued = schema.Date(
        title=_("Data prima pubblicazione del Catalogo"),
        required=False,
    )
    publisher_title = schema.TextLine(
        title=_("Publisher"),
        required=True,
        max_length=1024,
    )


@adapter(Interface, Interface)
class ControlPanelConfigletPanel(RegistryConfigletPanel):
    schema = IControlPanel
    schema_prefix = None
    configlet_id = "opendata-controlpanel"
    configlet_category_id = "Products"
    title = "Opendata"
    group = "Products"


class ControlPanel(RegistryEditForm):
    id = "opendata-controlpanel"
    label = _("Opendata")
    schema = IControlPanel
