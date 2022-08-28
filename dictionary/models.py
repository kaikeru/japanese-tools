from ast import Mod
from datetime import datetime
from django.db.models import (
    Model,
    CharField,
    IntegerField,
    ForeignKey,
    DateField,
    DateTimeField,
    CASCADE,
)


class KanjidictVersion(Model):
    """The version information for the KanjiDict."""

    file_version = IntegerField()
    database_version = CharField(max_length=32)
    date_of_creation = DateField()
    created_on = DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "kanjidict_version"


class Kanji(Model):
    """Kanji"""

    literal = CharField(max_length=1, primary_key=True)
    grade = IntegerField(default=0)
    stroke_count = IntegerField(default=0)
    frequency = IntegerField(default=0)
    radical_name = CharField(max_length=16, default="")
    jlpt_old = IntegerField(default=0)

    class Meta:
        db_table = "kanji"


class KanjiCodepoint(Model):
    """Kanji codepoint"""

    cp_value = CharField(max_length=32)
    cp_type = CharField(max_length=32)
    kanji = ForeignKey(Kanji, on_delete=CASCADE, related_name="codepoints")

    class Meta:
        db_table = "kanji_codepoint"


class KanjiMeaning(Model):
    """Kanji meaning"""

    lang = CharField(max_length=16)
    meaning = CharField(max_length=128)
    kanji = ForeignKey(Kanji, on_delete=CASCADE, related_name='meanings')

    class Meta:
        db_table = "kanji_meaning"


class KanjiQueryCode(Model):
    """Kanji query code"""

    qc_value = CharField(max_length=32)
    qc_type = CharField(max_length=32)
    skip_misclass = CharField(max_length=32, default="")
    kanji = ForeignKey(Kanji, on_delete=CASCADE, related_name="query_codes")

    class Meta:
        db_table = "kanji_query_code"


class KanjiRadical(Model):
    """Kanji radical"""

    rad_type = CharField(max_length=32)
    rad_value = IntegerField()

    class Meta:
        db_table = "kanji_radical"


class KanjiReading(Model):
    """Kanji readings"""

    reading_type = CharField(max_length=32)
    reading = CharField(max_length=32)
    kanji = ForeignKey(Kanji, on_delete=CASCADE, related_name="readings")

    class Meta:
        """Model Meta"""

        db_table = "kanji_reading"


class KanjiReferenceIndex(Model):
    """Kanji"""

    index_number = CharField(max_length=32, null=False)
    reference = CharField(max_length=32, null=False)
    kanji = ForeignKey(Kanji, on_delete=CASCADE, related_name="reference_indexes")

    class Meta:
        """Meta class for model."""

        db_table = "kanji_reference_index"


class KanjiReferenceDaikanwajiten(Model):
    """Kanji"""

    volume = CharField(max_length=32)
    page = CharField(max_length=32)
    kanji_reference_index = ForeignKey(KanjiReferenceIndex, on_delete=CASCADE, related_name="reference_diakanwajiten")

    class Meta:
        """Model metadata"""

        db_table = "kanji_reference_daikanwajiten"


class KanjiStrokeMiscount(Model):
    """Kanji stroke miscount"""

    stroke_count = IntegerField(null=False)
    kanji = ForeignKey(Kanji, on_delete=CASCADE, related_name="stroke_miscounts")

    class Meta:
        """Model Meta."""

        db_table = "kanji_stroke_miscount"


class KanjiToRadical(Model):
    """Kanji to radical"""

    kanji = ForeignKey(Kanji, on_delete=CASCADE)
    radical = ForeignKey(KanjiRadical, on_delete=CASCADE)

    class Meta:
        """Meta Class"""

        db_table = "kanji_to_radical"


class KanjiVariant(Model):
    """Kanji"""

    var_value = CharField(max_length=32)
    var_type = CharField(max_length=32)
    kanji = ForeignKey(Kanji, on_delete=CASCADE, related_name="variants")

    class Meta:
        """Meta class"""

        db_table = "kanji_variant"
