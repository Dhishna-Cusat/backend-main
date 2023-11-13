import random
import string
from rest_framework.decorators import api_view
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.conf import settings
from .models import Event, CA
from .serializer import CASerializer
from django.core.mail import send_mail


def send_ca_mail(name, email):
    subject = 'Thank You for Becoming a Dhishna Campus Ambassador!'
    message = f"""Dear {name},

A big thank you for joining us as a Dhishna Campus Ambassador! Your support means the world to us and we're thrilled to have you on board.

Your role as a Campus Ambassador is vital in spreading the word about our event, sharing our vision, and inspiring others to get involved. Your passion and dedication will play a significant role in making Dhishna '23 a grand success.

We are outlining expected duties of a Dhishna Campus Ambassador:
- Campus ambassadors act as liaisons between their organization and the college community.
- They spread awareness about products, services, and opportunities offered by the organization.
- Ambassadors often organize events and engage in recruitment activities on campus.
- Providing feedback and insights to the organization helps improve their offerings.
- This role allows students to gain practical experience in marketing and networking.
- It also helps students build valuable relationships for future career opportunities.

If you have questions or ideas, we're here to help. Let's make Dhishna '23 unforgettable together!

Best regards,
Dhishna '23 Team."""

    from_email = 'ca@dhishna.org'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=settings.EMAIL_HOST_USER_ACCOUNT1, auth_password=settings.EMAIL_HOST_PASSWORD_ACCOUNT1)




@api_view(['POST'])
def get_referral(request):
    if hasattr(request, 'firebase_user') and request.firebase_user:
        id = request.firebase_user['user_id']

        ca = get_object_or_404(CA, id=id)
        return JsonResponse({'referral': ca.referral})

    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_points(request):
    if hasattr(request, 'firebase_user') and request.firebase_user:
        id = request.firebase_user['user_id']

        ca = get_object_or_404(CA, id=id)
        return JsonResponse({'points': ca.points})

    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_top_ten(request):
        cas = CA.objects.order_by('-points')[:9]
        ret = []
        for ca in cas:
            ret.append({'points':ca.points, 'name': ca.name, 'college': ca.college})

        return JsonResponse(ret)



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
                send_ca_mail(request.data['name'], request.data['email'])
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
    response['X-Accel-Redirect'] = '/protected/' + path
    return response
