from django.db.models import Max, Case, When, Value, CharField, DecimalField
from django.db.models.functions import TruncDay
from rest_framework.views import APIView
from .models import PriceRecords
from django.utils.timezone import now, timedelta
from django.http import JsonResponse


class PriceHistory(APIView):
    def get(self, request):
        # Define the time frame
        end_date = now()
        start_date = end_date - timedelta(days=30)

        # Aggregate latest price information by day
        price_data = PriceRecords.objects.filter(
            timestamp__range=[start_date, end_date],
            symbol='ETH'
        ).annotate(
            day=TruncDay('timestamp')
        ).values('day').annotate(
            priceUniswapV3=Max(Case(
                When(source__name='UniSwap', then='price_decimal'),
                output_field=DecimalField(),
            )),
            priceCoingecko=Max(Case(
                When(source__name='CoinGecko', then='price_decimal'),
                output_field=DecimalField(),
            )),
            blockNo=Max(Case(
                When(source__name='UniSwap', then='block_no'),
                output_field=CharField(),
            ))
        ).order_by('-day')

        # Convert the QuerySet to a list of dicts
        data = list(price_data)

        # Return data as JSON
        return JsonResponse(data, safe=False)
