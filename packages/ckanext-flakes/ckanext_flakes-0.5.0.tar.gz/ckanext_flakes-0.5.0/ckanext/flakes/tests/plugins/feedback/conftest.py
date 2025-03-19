from ckan.tests.factories import CKANFactory, Dataset
from ckanext.flakes.model import Flake
from pytest_factoryboy import register
import factory

@register(_name="flakes_feedback")
class FlakesFeedbackFactory(CKANFactory):
    class Meta:
        model = Flake
        action = "flakes_feedback_feedback_create"

    package_id = factory.LazyFunction(lambda: Dataset()["id"])
    data = factory.LazyFunction(dict)
    secondary_key = None
