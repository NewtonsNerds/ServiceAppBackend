from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomUser

from django.utils import timezone


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


class UserLoginSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False, read_only=True)
    token = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'mobile',
            'password',
            'token'
        ]

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

        def validate(self, attrs):
            email = attrs['email']
            password = attrs['password']
            user = CustomUser.objects.get(email=email)
            if user is None:
                raise ValidationError("This email is not valid.")
            else:
                if not user.check_password(password):
                    raise ValidationError("Incorrect credentials. Please try again.")
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            attrs["id"] = user.id
            attrs["mobile"] = user.mobile
            attrs["token"] = "SOME RANDOM TOKEN"
            return attrs