from ast import Mod
from datetime import datetime
from django.db.models import (
    Model,
    CharField,
    IntegerField,
    ForeignKey,
    DateField,
    DateTimeField,
    TextField,
    CASCADE,
)

### KANJI ###


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
    kanji = ForeignKey(Kanji, on_delete=CASCADE, related_name="meanings")

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
    kanji_reference_index = ForeignKey(
        KanjiReferenceIndex, on_delete=CASCADE, related_name="reference_diakanwajiten"
    )

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


### KOTOBA ###


class Kotoba(Model):
    """
    A Japanese word.
    Kind of weird because there can be multiple readings for a single entry.
    This model is more of a glue to keep the entries together.
    """

    created = DateTimeField(auto_now_add=True)
    jmdict_sequence = CharField(max_length=64)

    class Meta:
        db_table = "kotoba"


class KotobaKanji(Model):
    """
    A Kanji meaning associated with the kotoba.
    May not be part of the Kotoba or not.
    """

    kotoba = ForeignKey(Kotoba, on_delete=CASCADE, related_name="kanji")
    value = CharField(max_length=128)
    information = CharField(max_length=32, null=True, default=None)
    priority = CharField(max_length=32, null=True, default=None)

    class Meta:
        db_table = "kotoba_kanji"


class KotobaReading(Model):
    """
    Reading for a kotoba
    A Kotoba entry will always have at least one reading.
    """

    kotoba = ForeignKey(Kotoba, on_delete=CASCADE, related_name="kana")
    value = CharField(max_length=128)
    information = CharField(max_length=32, null=True, default=None)
    priority = CharField(max_length=32, null=True, default=None)

    class Meta:
        db_table = "kotoba_reading"


class KotobaKanjiToReading(Model):
    """
    A mapping of Kanji to Readings
    """

    kanji = ForeignKey(KotobaKanji, on_delete=CASCADE, related_name="related_kana")
    reading = ForeignKey(KotobaReading, on_delete=CASCADE, related_name="related_kanji")

    class Meta:
        db_table = "kotoba_kanji_to_reading"


class KotobaMeaning(Model):
    """
    The overall meaning of the kotoba with grouped definitions.
    Think of these as the word feel. There can be multiple meanings depending on the
    usage of the kotoba. Each meaning can have concreate definitions associated.
    """

    kotoba = ForeignKey(Kotoba, on_delete=CASCADE, related_name="meanings")
    information = TextField(null=True, default=None)

    class Meta:
        db_table = "kotoba_meaning"


class KotobaMeaningField(Model):
    """
    Fields for various meanings
    """

    meaning = ForeignKey(KotobaMeaning, on_delete=CASCADE, related_name="fields")
    value = CharField(max_length=32)
    type = CharField(max_length=32)

    class Meta:
        db_table = "kotoba_meaning_field"


class KotobaMeaningLoanSource(Model):
    """
    Loan word source information about the meaning.
    """

    meaning = ForeignKey(KotobaMeaning, on_delete=CASCADE, related_name="loan_sources")
    language = CharField(max_length=32, null=True, default=None)
    word = CharField(max_length=128, null=True, default=None)
    type = CharField(max_length=32, null=True, default=None)

    class Meta:
        db_table = "kotoba_meaning_loan_source"


class KotobaMeaningDefinition(Model):
    """
    The various concrete definitions for a meaning.
    """

    meaning = ForeignKey(KotobaMeaning, on_delete=CASCADE, related_name="definitions")
    value = TextField()
    language = CharField(max_length=32, default="eng")
    type = CharField(max_length=32, null=True, default=None)

    class Meta:
        db_table = "kotoba_meaning_definition"
