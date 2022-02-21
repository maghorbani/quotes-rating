from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt import authentication
from django.shortcuts import get_object_or_404

from .serializers import QuoteSerializer, RateSerializer
from .models import Quote, Rate

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class QuoteView(ViewSet):

    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = QuoteSerializer

    req_param = openapi.Parameter('Authorization', in_=openapi.IN_HEADER, description="Bearer access-token. use the token from token/ route and prefix it with 'Bearer'", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[req_param], responses={200: QuoteSerializer(many=True)})
    def list(self, request):
        queryset = Quote.objects.all()
        serializer = QuoteSerializer(queryset, context={'user': request.user},many=True)
        return Response(serializer.data)


class RateView(ViewSet):

    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = RateSerializer
    def create(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)

        if "score" not in request.data:
            return Response({
                "message":"'score' key is required"
            },
            status=400)

        score = int(request.data.get("score", "0"))

        if score > 5 or score < 0 :
            return Response({
                "message":"'score' should be an integer between 0 and 5"
            },
            status=400)

    
        num_rates = quote.rate_set.count()

        rate = Rate(quote=quote, user=request.user, score=score)
        try:
            rate.save()
            quote.average_score = (quote.average_score * num_rates + score) / (num_rates + 1)
            quote.save()
        except Exception as e:
            rate = Rate.objects.filter(quote__pk=quote.id).filter(user__pk=request.user.id)[0]
            rate.score = score
            rate.save()
            quote.average_score = (quote.average_score * num_rates + score - quote.average_score) / num_rates
            quote.save()

        return Response([score])


