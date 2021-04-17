from flask import Blueprint, request
from flask_restplus import Resource, Api
from results_reporting.schema import ProgramResultSchema, UniResultSchema, ResultSchema
from results_reporting.dal import ProgramUpdatesDAL
from results_reporting.scrap_gc_job import ScrapGCJob

results_controller = Blueprint('results_controller', __name__)
api = Api(results_controller)
program_result_schema = ProgramResultSchema(many=True)


@api.route("/api/user/<string:deviceId>/updates")
class ResultsController(Resource):
    def get(self, deviceId):
        try:
            program_updates = ProgramUpdatesDAL.getProgramUpdates(deviceId)
            return program_result_schema.dump(program_updates)
        except Exception as ex:
            return {'Error': ex.__str__()}, 500

@api.route("/api/updates")
class UpdatesController(Resource):
    def get(self, deviceId):
        try:
            ScrapGCJob.loadDataFromGCJob() #Eventually make this async
            return
        except Exception as ex:
            return {'Error': ex.__str__()}, 500

