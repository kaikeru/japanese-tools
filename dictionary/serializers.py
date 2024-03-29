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
    Kotoba,
    KotobaKanji,
    KotobaMeaningDefinition,
    KotobaMeaningField,
    KotobaMeaningLoanSource,
    KotobaReading,
    KotobaMeaning,
)

### KANJI


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


### KOTOBA


class KotobaKanjiReadingIdField(serializers.RelatedField):
    def to_representation(self, value):
        return value.reading.id

class KotobaKanjiMeaningIdField(serializers.RelatedField):
    def to_representation(self, value):
        return value.meaning.id


class KotobaKanjiSerializer(serializers.ModelSerializer):
    related_kana = KotobaKanjiReadingIdField(many=True, read_only=True)
    meanings = KotobaKanjiMeaningIdField(many=True, read_only=True)

    class Meta:
        model = KotobaKanji
        fields = ["id", "value", "related_kana", "meanings", "information", "priority"]


class KotobaReadingKanjiIdField(serializers.RelatedField):
    def to_representation(self, value):
        return value.kanji.id


class KotobaReadingSerializer(serializers.ModelSerializer):

    related_kanji = KotobaReadingKanjiIdField(many=True, read_only=True)
    meanings = KotobaKanjiMeaningIdField(many=True, read_only=True)


    class Meta:
        model = KotobaReading
        fields = ["id", "value", "related_kanji", "meanings", "information", "priority"]


class KotobaMeaningFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = KotobaMeaningField
        fields = ["type", "value"]


class KotobaMeaningLoanSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = KotobaMeaningLoanSource
        fields = ["language", "word", "type"]


class KotobaMeaningDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KotobaMeaningDefinition
        fields = ["value", "type", "language"]


class KotobaMeaningSerializer(serializers.ModelSerializer):
    fields = KotobaMeaningFieldSerializer(many=True, read_only=True)
    loan_sources = KotobaMeaningLoanSourceSerializer(many=True, read_only=True)
    definitions = KotobaMeaningDefinitionSerializer(many=True, read_only=True)

    class Meta:
        model = KotobaMeaning
        fields = ["id", "definitions", "information", "fields", "loan_sources"]


class KotobaSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="kotoba-detail")
    kanji = KotobaKanjiSerializer(many=True, read_only=True)
    kana = KotobaReadingSerializer(many=True, read_only=True)
    meanings = KotobaMeaningSerializer(many=True, read_only=True)

    class Meta:
        model = Kotoba
        fields = ["id", "url", "kanji", "kana", "meanings"]
