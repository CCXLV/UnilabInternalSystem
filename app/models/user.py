from app.extensions import db
from app.models.base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class Country(BaseModel):
    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String)

    user = db.relationship("User", backref="country")


class Region(BaseModel):
    __tablename__ = "regions"

    id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String)

    user = db.relationship("User", backref="region")


class City(BaseModel):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String)

    user = db.relationship("User", backref="city")


class University(BaseModel):
    __tablename__ = "universities"

    id = db.Column(db.Integer, primary_key=True)
    university_name = db.Column(db.String)

    user = db.relationship("User", backref="university")


class User(BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)  #
    name = db.Column(db.String)  #
    lastname = db.Column(db.String)  #
    email = db.Column(db.String)  #
    _password = db.Column("password", db.String)
    personal_id = db.Column(db.String)  #
    number = db.Column(db.String)  #
    date = db.Column(db.Date)  #
    gender = db.Column(db.String)  #
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"))  #
    region_id = db.Column(db.Integer, db.ForeignKey("regions.id"))  #
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"))  #
    address = db.Column(db.String)  #
    confirmed = db.Column(db.Boolean, default=False)
    reset_password = db.Column(db.Integer, default=False)
    role = db.relationship("Role", secondary="user_roles", backref="roles")  #
    announcements = db.relationship("Announcement", secondary="announcement_user", backref="announcements")
    question = db.relationship("Question", backref="user")

    # Pupil #
    school = db.Column(db.String)
    grade = db.Column(db.String)
    parent_name = db.Column(db.String)
    parent_lastname = db.Column(db.String)
    parent_number = db.Column(db.String)

    # student #
    university_id = db.Column(db.Integer, db.ForeignKey("universities.id"))
    faculty = db.Column(db.String)
    program = db.Column(db.String)
    semester = db.Column(db.String)
    degree_level = db.Column(db.String)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    password = db.synonym('_password', descriptor=property(
        _get_password, _set_password))

    def check_permission(self, request):
        permisions = [getattr(permision, request) for permision in self.role]

        return any(permisions)

    def to_json(self):
        user_data = {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            "number": self.number,
            "personal_id": self.personal_id,
            "date": str(self.date),
            "gender": self.gender,
            "country_id": self.country_id,
            "region_id": self.region_id,
            "city_id": self.city_id,
            "address": self.address,
            "role": [role.name for role in self.role],
            "school": self.school,
            "grade": self.grade,
            "parent_name": self.parent_name,
            "parent_lastname": self.parent_lastname,
            "parent_number": self.parent_number,
            "university_id": self.university_id,
            "faculty": self.faculty,
            "program": self.program,
            "semester": self.semester,
            "degree_level": self.degree_level
        }

        return user_data
