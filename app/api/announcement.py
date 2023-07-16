from flask_restful import Resource, reqparse, inputs
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.subjects import Announcement


class AnnouncementApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, type=str)
    parser.add_argument("subject_id", required=True, type=int)
    parser.add_argument("activity_type_id", required=True, type=int)
    parser.add_argument("lecturer_id", required=True, type=int)
    parser.add_argument("regitration_start", required=True, type=inputs.datetime_from_iso8601)
    parser.add_argument("regitration_end", required=True, type=inputs.datetime_from_iso8601)

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        if not user.check_permission("can_create_activity"):
            return "Bad request", 400

        announcements = [announcement.to_json() for announcement in Announcement.query.all()]

        return announcements, 200

    @jwt_required()
    def post(self):

        request_parser = self.parser.parse_args()

        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        if not user.check_permission("can_create_activity"):
            return "Bad request", 400

        new_announcement = Announcement(
            name=request_parser["name"],
            subject_id=request_parser["subject_id"],
            activity_type_id=request_parser["activity_type_id"],
            lecturer_id=request_parser["lecturer_id"],
            regitration_start=request_parser["regitration_start"],
            regitration_end=request_parser["regitration_end"],
        )
        new_announcement.create()
        new_announcement.save()
        return "Success", 200

    @jwt_required()
    def put(self, id):
        result = Announcement.query.get(id)

        request_parser = self.parser.parse_args()

        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        if not user.check_permission("can_create_activity"):
            return "Bad request", 400


        if not result:
            return "Bad request", 400

        result.name = request_parser["name"]
        result.subject_id = request_parser["subject_id"]
        result.activity_type_id = request_parser["activity_type_id"]
        result.lecturer_id = request_parser["lecturer_id"]
        result.regitration_start = request_parser["regitration_start"]
        result.regitration_end = request_parser["regitration_end"]
        result.save()
        return "Success", 200

    @jwt_required()
    def delete(self, id):
        result = Announcement.query.get(id)

        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        if not user.check_permission("can_create_activity"):
            return "Bad request", 400


        if not result:
            return "Bad request", 400

        result.delete()
        result.save()
        return "Success", 200
