from drf_compound_fields.fields import ListField
from rest_framework import serializers

from mkt.constants.base import CONTENT_ICON_SIZES
from mkt.api.fields import (GuessLanguageTranslationField,
                            TranslationSerializerField)
from mkt.search.serializers import BaseESSerializer
from mkt.tags.models import attach_tags
from mkt.websites.models import Website, WebsiteSubmission


class WebsiteSerializer(serializers.ModelSerializer):
    categories = ListField(serializers.CharField())
    description = TranslationSerializerField()
    device_types = ListField(serializers.CharField(), source='device_names')
    id = serializers.IntegerField(source='pk')
    short_name = TranslationSerializerField()
    keywords = serializers.SerializerMethodField('get_keywords')
    name = TranslationSerializerField()
    title = TranslationSerializerField()
    icons = serializers.SerializerMethodField('get_icons')

    class Meta:
        model = Website
        fields = ['categories', 'description', 'device_types', 'icons', 'id',
                  'keywords', 'mobile_url', 'name', 'short_name', 'title',
                  'url']

    def get_icons(self, obj):
        return {icon_size: obj.get_icon_url(icon_size)
                for icon_size in CONTENT_ICON_SIZES}

    def get_keywords(self, obj):
        if not hasattr(obj, 'keywords_list'):
            attach_tags([obj])
        return getattr(obj, 'keywords_list', [])


class ESWebsiteSerializer(BaseESSerializer, WebsiteSerializer):
    def fake_object(self, data):
        """Create a fake instance of Website from ES data."""
        obj = Website(id=data['id'])

        # Set basic attributes on the fake instance using the data from ES.
        self._attach_fields(
            obj, data, ('default_locale', 'icon_hash', 'mobile_url', 'url'))

        # Set attributes with names that don't exactly match the one on the
        # model.
        obj.categories = data['category']
        obj.devices = data['device']
        obj.keywords_list = data['tags']

        if obj.icon_hash:
            # If we have an icon_hash, then we have an icon. All the icons we
            # store are PNGs.
            obj.icon_type = 'image/png'

        # Attach translations for all translated attributes. obj.default_locale
        # should be set first for this to work.
        self._attach_translations(
            obj, data, ('description', 'name', 'short_name', 'title'))

        # Some methods might need the raw data from ES, put it on obj.
        obj.es_data = data

        return obj


class ReviewerESWebsiteSerializer(ESWebsiteSerializer):
    class Meta(ESWebsiteSerializer.Meta):
        model = Website
        fields = ESWebsiteSerializer.Meta.fields + ['status']


class PublicWebsiteSubmissionSerializer(serializers.ModelSerializer):
    categories = ListField(serializers.CharField())
    description = GuessLanguageTranslationField()
    id = serializers.IntegerField(source='pk', required=False)
    keywords = ListField(serializers.CharField())
    name = GuessLanguageTranslationField()
    preferred_regions = ListField(serializers.CharField(), required=False)
    works_well = serializers.IntegerField()

    class Meta:
        model = WebsiteSubmission
        fields = ['canonical_url', 'categories', 'description',
                  'detected_icon', 'id', 'keywords', 'name',
                  'preferred_regions', 'public_credit', 'url', 'why_relevant',
                  'works_well']
