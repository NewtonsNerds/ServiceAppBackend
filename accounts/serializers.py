from rest_framework import serializers

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

        user = CustomUser(
            email=email,
            mobile=mobile
        )

        user.set_password(password)
        user.save()
        return user

    # TODO: Define validate functions for UserRegisterSerializer