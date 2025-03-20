from sqlalchemy import Integer, BigInteger
from sqlalchemy.dialects.mysql import BIGINT

UnsignedBigInteger = BigInteger()
UnsignedBigInteger = UnsignedBigInteger.with_variant(Integer, "sqlite").with_variant(
    BIGINT(unsigned=True), "mysql", "mariadb"
)
