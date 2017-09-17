from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import common_flavour, finalise_markup
from .serializers import MarkupSerializer


@api_view(['POST'])
def parse_markup(request):
    serializer = MarkupSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'detail': serializer.errors['non_field_errors'][0]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    parsing_result = common_flavour(
        request,
        request.user,
        serializer.data['post'],
        force_shva=True,
    )
    finalised = finalise_markup(parsing_result['parsed_text'])

    return Response({'parsed': finalised})
