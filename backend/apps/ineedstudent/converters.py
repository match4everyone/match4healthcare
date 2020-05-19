class DecimalPointFloatConverter:
    """
    Custom Django converter for URLs.

    Parses floats with a decimal point (not with a comma!)
    Allows for integers too, parses values in this or similar form:
    - 100.0
    - 100

    Will NOT work for these forms:
    - 100.000.000
    - 100,0
    """

    regex = "[0-9]*[.]?[0-9]*"

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)
