from sqlalchemy import Integer
from sqlalchemy.dialects.mysql import MEDIUMINT

MediumInteger = Integer()
MediumInteger = MediumInteger.with_variant(Integer, "sqlite").with_variant(MEDIUMINT(), "mysql", "mariadb")
