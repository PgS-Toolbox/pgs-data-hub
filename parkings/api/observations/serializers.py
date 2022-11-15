from rest_framework import serializers

from parkings.models import ParkingCheck
from parkings.api.constants import CREDENTIAL_TYPES
from parkings.api.common import VersionedReferenceSerializer
from parkings.api.enforcement.check_parking import CheckParkingSerializer


class ObservationsSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    version = serializers.SerializerMethodField()
    method = serializers.SerializerMethodField()
    observer = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    observedCredentialId = serializers.SerializerMethodField()
    observationStartTime = serializers.SerializerMethodField()
    creationDateTime = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    observerOrganisation = serializers.SerializerMethodField()

    class Meta:
        model = ParkingCheck
        fields(
            "id",
            "version",
            "method",
            "observer",
            "type",
            "observedCredentialId",
            "observationStartTime",
            "creationDateTime",
            "location",
            "observerOrganisation"
        )

    def get_id(self, obj):
        return obj.pk

    def get_version(self, obj):
        return 1

    def get_method(self, obj):
        return "visual"

    def get_observer(self, obj):
        return obj.performer.name

    def get_type(self, obj):
        return "licensePlate"

    def get_observedCredentialId(self, obj):
        return obj.registration_number

    def get_observationStartTime(self, obj):
        return obj.time

    def get_creationDateTime(self, obj):
        return obj.created_at

    def get_location(self, obj):
        return {
            "observerLocation": obj.location
        }

    def get_observerOrganisation(self, obj):
        return {
            "id": obj.performer.enforced_domain.code,
            "version": 1,
            "className": "EnforcementDomain"
        }


class LocationSerializer(serializers.Serializer):
    observerLocation = 


class ObservationsCreateUpdateSerializer(serializers.ModelSerializer):
    method = serializers.ChoiceField(choices=("anpr", "chalk", "rfTransponder", "scanner", "visual"))
    observer = serializers.CharField(required=False)
    type = serializers.ChoiceField(choices=CREDENTIAL_TYPES, required=True)
    observedCredentialId = serializers.CharField(max_length=20, required=True)
    observationStartTime = serializers.DateTimeField(required=True)
    location = LocationSerializer()
    observerOrganisation = VersionedReferenceSerializer()

    class Meta:
        model = ParkingCheck
        fields(
            "method",
            "observer",
            "type",
            "observedCredentialId",
            "observationStartTime",
            "location",
            "observerOrganisation"
        )

    def create(self, validated_data):
        return CheckParkingSerializer(**validated_data)

    def validated_data(self, data):
        if data["type"] != "licensePlate":
            raise serializers.ValidationError("Type is different than `licensePlate`")

        check_parking_data = {
            "registration_number": data["observedCredentialId"],
            "location": {
                "latitude": data["location"][""],
                "longitude": data["location"][""]
            },
            "time": data["observationStartTime"]
        }
        CheckParkingSerializer.validate(check_parking_data)
        return check_parking_data