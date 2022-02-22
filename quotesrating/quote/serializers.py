from dataclasses import field, fields
from rest_framework import serializers
from .models import Quote, Rate


class CreateQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ('id', 'title', 'body')


class QuoteSerializer(serializers.ModelSerializer):
    number_of_ratings = serializers.SerializerMethodField('get_number_of_ratings')
    your_score = serializers.SerializerMethodField('get_your_score')

    class Meta:
        model = Quote
        fields = ('id', 'title', 'body', 'user', 'average_score', 'number_of_ratings', 'your_score')

    def get_number_of_ratings(self, quote):
        return quote.rate_set.count()

    def get_your_score(self, quote):
        rate = quote.rate_set.filter(user__pk=self.context['user'].id)

        if rate.count() > 0:
            return rate[0].score

        return "not rated"


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'
