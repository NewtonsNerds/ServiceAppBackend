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

    def validate(self,attrs):
        email = attrs("email")
        user = CustomUser.objects.get(email=email)
        if user is not None:
            raise ValidationError("This email is already exist")
        else:
            return attrs