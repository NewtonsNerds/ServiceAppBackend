from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CustomUser

from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings

from django.utils import timezone
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserDetailSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'mobile',
            'address',
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    token = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'mobile',
            'password',
            'address',
            'token',
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

        user.last_login = timezone.now()
        user.set_password(password)
        user.save()
        validated_data["id"] = user.id
        payload = jwt_payload_handler(user)
        validated_data["token"] = jwt_encode_handler(payload)
        return validated_data

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
            'address',
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

            payload = jwt_payload_handler(user)

            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            attrs["id"] = user.id
            attrs["token"] = jwt_encode_handler(payload)
            return attrs


class CustomJSONWebTokenSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            'username': attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = _('Unable to login with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)