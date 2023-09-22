from rest_framework import serializers

from airport.models import Airport, AirplaneType, Airplane


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = "__all__"


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = (
            "name",
            "rows",
            "seats_in_row",
            "airplane_type",
        )


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.CharField(
        max_length=255, source="airplane_type.name", read_only=True,
    )

    class Meta:
        model = Airplane
        fields = (
            "name",
            "rows",
            "seats_in_row",
            "airplane_type",
        )
