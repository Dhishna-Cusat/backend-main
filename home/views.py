from django.utils import timezone
from rest_framework import viewsets, status
from django.http import Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.contrib.staticfiles.views import serve
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from .models import Event, CA
from .serializer import CASerializer
import random
import string




def test_view(request):
    # print(request.firebase_user['uid'])
    today = timezone.now()  # Get the current date and time
    events = Event.objects.filter(end_date__gt=today)
    for event in events:
        print(event.yep_id)
    return HttpResponse("Hello, this is my route!")


class CACreateViewSet(viewsets.ModelViewSet):
    queryset = CA.objects.all()
    serializer_class = CASerializer

    def create(self, request, *args, **kwargs):
        if hasattr(request, 'firebase_user') and request.firebase_user:
            request.data['id'] = request.firebase_user['user_id']
            request.data['referral'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Save the CA object
                serializer.save()
                return Response({"message": "created"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)



    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@login_required
@user_passes_test(lambda user: user.is_staff, login_url=settings.LOGIN_URL)
def protected_serve(request, path, document_root=None, show_indexes=False):
    # Use user_passes_test decorator to ensure the user is staff
    # if not request.user.has_perm("auth.view_permission_for_staff"):
    #     raise Http404("Not found")

    response = HttpResponse()
    # Content-type will be detected by nginx
    del response['Content-Type']
    response['X-Accel-Redirect'] = '/protected-static/' + path
    return response
