from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


def str_to_bool(val):
    if isinstance(val, bool):
        return val
    if val is None:
        return False
    return str(val).lower() in ("true", "1", "yes", "on")


with app.app_context():
    db.create_all()
    # Seed initial data if the database is empty
    if not db.session.execute(db.select(Cafe)).scalars().first():
        sample_cafes = [
            Cafe(
                name="Science Gallery London",
                map_url="https://goo.gl/maps/22",
                img_url="https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=800&q=80",
                location="London Bridge",
                seats="50+",
                has_toilet=True,
                has_wifi=True,
                has_sockets=True,
                can_take_calls=True,
                coffee_price="£2.40",
            ),
            Cafe(
                name="Social - Copeland Social",
                map_url="https://goo.gl/maps/33",
                img_url="https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=800&q=80",
                location="Peckham",
                seats="20-30",
                has_toilet=True,
                has_wifi=True,
                has_sockets=False,
                can_take_calls=True,
                coffee_price="£2.75",
            ),
            Cafe(
                name="One & All Cafe",
                map_url="https://goo.gl/maps/44",
                img_url="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=800&q=80",
                location="Peckham",
                seats="30-40",
                has_toilet=True,
                has_wifi=True,
                has_sockets=True,
                can_take_calls=False,
                coffee_price="£2.60",
            ),
        ]
        db.session.add_all(sample_cafes)
        db.session.commit()


# --- WEB FRONTEND ROUTE ---
@app.route("/")
def home():
    return render_template("index.html")


# --- REST API ROUTES ---
@app.route("/random", methods=["GET"])
def get_random_coffee():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    if not all_cafes:
        return jsonify(error={"Not Found": "No cafes available in the database."}), 404
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def search_cafes():
    location = request.args.get("loc", "")
    # Case-insensitive partial match makes web searching much friendlier
    result = db.session.execute(
        db.select(Cafe).where(Cafe.location.ilike(f"%{location}%"))
    )
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404


@app.route("/add", methods=["POST"])
def post_new_cafe():
    data = request.get_json(silent=True) or request.form

    # Check for missing required fields
    required_fields = ["name", "map_url", "img_url", "loc", "seats"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify(error={"Bad Request": f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        new_cafe = Cafe(
            name=data.get("name").strip(),
            map_url=data.get("map_url").strip(),
            img_url=data.get("img_url").strip(),
            location=data.get("loc").strip(),
            has_sockets=str_to_bool(data.get("sockets")),
            has_toilet=str_to_bool(data.get("toilet")),
            has_wifi=str_to_bool(data.get("wifi")),
            can_take_calls=str_to_bool(data.get("calls")),
            seats=data.get("seats").strip(),
            coffee_price=data.get("coffee_price", "").strip() or None,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify(error={"Bad Request": "A cafe with that name already exists."}), 400
    except Exception as e:
        db.session.rollback()
        print("DB Error:", e)  # Prints exact error in your Flask console
        return jsonify(error={"Bad Request": str(e)}), 400


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.session.get(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        cafe = db.session.get(Cafe, cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api-key."}), 403


if __name__ == "__main__":
    app.run(debug=True)