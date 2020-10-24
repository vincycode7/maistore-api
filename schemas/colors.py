from ma import ma
from models.colors import ColorsModel
from marshmallow_sqlalchemy import fields


class ColorsSchema(ma.SQLAlchemyAutoSchema):
    productcol = fields.Nested(
        "ProductColorSchema",
        many=True,
        exclude=("colors",),
    )

    class Meta:
        model = ColorsModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True
