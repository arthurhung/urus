from flask_restful import Resource, Api
from urus_api.v1.ris_gov.views import IDcardValidator, HelloWorld, HouseholdCertRecord, FamilyLitigation
from flask import Blueprint
from urus_api.config import Config

gov_bp = Blueprint('gov', __name__, url_prefix=f'/Urus/{Config.API_VERSION}/gov')
api = Api(gov_bp)

# add resource
api.add_resource(HelloWorld, '/hi')
api.add_resource(IDcardValidator, '/IDcardValidator')
api.add_resource(HouseholdCertRecord, '/HouseholdCertRecord')
api.add_resource(FamilyLitigation, '/FamilyLitigation')
