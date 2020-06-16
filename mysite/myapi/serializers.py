from rest_framework import serializers
from .models import Person
from .models import Admin


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='person-highlight', format='html')

    class Meta:
        model = Person
        fields = ('url', 'highlight', 'first_name', 'last_name', 'email', 'gender', 'image_url')


class AdminSerializer(serializers.HyperlinkedModelSerializer):
    # people = serializers.HyperlinkedRelatedField(many=True, view_name='person-detail', read_only=True)
    # owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Admin
        fields = ('url', 'username', 'password')


