from sqlalchemy import Integer, BigInteger

BigInteger = BigInteger()
BigInteger = BigInteger.with_variant(Integer, "sqlite")
