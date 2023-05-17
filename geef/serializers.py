from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    reffered_by_link = serializers.CharField(allow_blank=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_confirm', 'reffered_by_link']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)
        self.reffered_by_link = attrs.pop('reffered_by_link', None)
        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        user.set_password(password)
        reffered_by_link = self.reffered_by_link
        user.save()
        if reffered_by_link:
            refferal = UserProfile.objects.filter(ref_link=reffered_by_link).get()
            user.userprofile.referred_by = refferal
            user.save()
        return user
