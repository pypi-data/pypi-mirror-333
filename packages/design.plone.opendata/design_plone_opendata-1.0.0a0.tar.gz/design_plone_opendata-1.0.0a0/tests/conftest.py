from design.plone.opendata.testing import ACCEPTANCE_TESTING
from design.plone.opendata.testing import FUNCTIONAL_TESTING
from design.plone.opendata.testing import INTEGRATION_TESTING
from pytest_plone import fixtures_factory


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory(
        (
            (ACCEPTANCE_TESTING, "acceptance"),
            (FUNCTIONAL_TESTING, "functional"),
            (INTEGRATION_TESTING, "integration"),
        )
    )
)
