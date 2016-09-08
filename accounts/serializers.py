from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'mobile',
            'password',
            'address',
        ]

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def create(self, validated_data):
        email = validated_data['email']
        mobile = validated_data['mobile']
        password = validated_data['password']
        address = validated_data['address']

        user = CustomUser(
            email=email,
            mobile=mobile,

        )

        if address is not None or not address:
            user.address = address

        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        email = attrs["email"]
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return attrs
        raise ValidationError("This email is already exist")
