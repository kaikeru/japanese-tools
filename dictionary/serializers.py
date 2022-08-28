from rest_framework import serializers
from .models import (
    Kanji,
    KanjiMeaning,
    KanjiCodepoint,
    KanjiQueryCode,
    KanjiReading,
    KanjiReferenceIndex,
    KanjiReferenceDaikanwajiten,
    KanjiVariant,
)


class KanjiMeaningSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanjiMeaning
        fields = ["lang", "meaning"]


class KanjiCodepointSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanjiCodepoint
        fields = ["cp_value", "cp_type"]


class KanjiQueryCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanjiQueryCode
        fields = ["qc_value", "qc_type", "skip_misclass"]


class KanjiReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanjiReading
        fields = ["reading_type", "reading"]


class KanjiReferenceIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanjiReferenceIndex
        fields = ["reference", "index_number"]


class KanjiReferenceDaikanwajitenSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanjiReferenceDaikanwajiten
        fields = ["volume", "page"]


class KanjiVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanjiVariant
        fields = ["var_type", "var_value"]


class KanjiSerializer(serializers.ModelSerializer):
    readings = KanjiReadingSerializer(many=True, read_only=True)
    meanings = KanjiMeaningSerializer(many=True, read_only=True)
    codepoints = KanjiCodepointSerializer(many=True, read_only=True)
    query_codes = KanjiQueryCodeSerializer(many=True, read_only=True)
    reference_indexes = KanjiReferenceIndexSerializer(many=True, read_only=True)
    reference_diakanwajiten = KanjiReferenceDaikanwajitenSerializer(
        many=True, read_only=True
    )
    stroke_miscounts = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="stroke_count"
    )
    variants = KanjiVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Kanji
        fields = [
            "literal",
            "readings",
            "meanings",
            "grade",
            "stroke_count",
            "stroke_miscounts",
            "frequency",
            "radical_name",
            "jlpt_old",
            "variants",
            "codepoints",
            "query_codes",
            "reference_indexes",
            "reference_diakanwajiten",
        ]
