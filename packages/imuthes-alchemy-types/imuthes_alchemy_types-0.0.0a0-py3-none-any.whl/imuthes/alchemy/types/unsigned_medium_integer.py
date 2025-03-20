from sqlalchemy import Integer
from sqlalchemy.dialects.mysql import MEDIUMINT

UnsignedMediumInteger = Integer()
UnsignedMediumInteger = UnsignedMediumInteger.with_variant(Integer, "sqlite").with_variant(
    MEDIUMINT(unsigned=True), "mysql", "mariadb"
)
