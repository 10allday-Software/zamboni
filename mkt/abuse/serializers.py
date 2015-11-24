from rest_framework import serializers

from mkt.abuse.models import AbuseReport
from mkt.account.serializers import UserSerializer
from mkt.api.fields import SlugOrPrimaryKeyRelatedField, SplitField
from mkt.api.serializers import PotatoCaptchaSerializer
from mkt.extensions.models import Extension
from mkt.extensions.serializers import ExtensionSerializer
from mkt.webapps.models import Webapp
from mkt.webapps.serializers import SimpleAppSerializer
from mkt.websites.serializers import WebsiteSerializer


class BaseAbuseSerializer(PotatoCaptchaSerializer,
                          serializers.ModelSerializer):
    text = serializers.CharField(source='message')
    reporter = SplitField(serializers.PrimaryKeyRelatedField(required=False),
                          UserSerializer())

    class Meta:
        model = AbuseReport
        fields = ('text', 'reporter')

    def validate(self, attrs):
        request = self.context['request']
        if request.user.is_authenticated():
            attrs['reporter'] = request.user
        else:
            attrs['reporter'] = None
        attrs['ip_address'] = request.META.get('REMOTE_ADDR', '')
        return super(BaseAbuseSerializer, self).validate(attrs)


class UserAbuseSerializer(BaseAbuseSerializer):
    user = SplitField(serializers.PrimaryKeyRelatedField(), UserSerializer())

    class Meta(BaseAbuseSerializer.Meta):
        fields = BaseAbuseSerializer.Meta.fields + ('user',)


class AppAbuseSerializer(BaseAbuseSerializer):
    app = SplitField(
        SlugOrPrimaryKeyRelatedField(source='addon', slug_field='app_slug',
                                     queryset=Webapp.objects.all()),
        SimpleAppSerializer(source='addon'))

    class Meta(BaseAbuseSerializer.Meta):
        fields = BaseAbuseSerializer.Meta.fields + ('app',)


class WebsiteAbuseSerializer(BaseAbuseSerializer):
    website = SplitField(serializers.PrimaryKeyRelatedField(),
                         WebsiteSerializer())

    class Meta(BaseAbuseSerializer.Meta):
        fields = BaseAbuseSerializer.Meta.fields + ('website',)


class ExtensionAbuseSerializer(BaseAbuseSerializer):
    extension = SplitField(
        SlugOrPrimaryKeyRelatedField(
            source='extension', slug_field='slug',
            queryset=Extension.objects.without_deleted().public()),
        ExtensionSerializer())

    class Meta(BaseAbuseSerializer.Meta):
        fields = BaseAbuseSerializer.Meta.fields + ('extension',)
