from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from .serializers import NotificationsSerializer
from .models import Notification
from permissions import IsRestaurantOnly

# Create your views here.


class NotificationDetail(APIView):
    permission_classes = [IsRestaurantOnly]

    def get(self, request):
        response = {'status': False}
        user = request.user.restaurant
        try:
            notifications = Notification.objects.filter(
                user=user).order_by('-created_at')
            if notifications.exists():
                notifications_serializer = NotificationsSerializer(
                    notifications, many=True)
                response['notifications'] = notifications_serializer.data
            else:
                response['notifications'] = "You do" \
                                            "not have any notifications"
            response['status'] = True

        except Exception as e:
            response['error'] = {
                f"{e.__class__.__name__}": f"{e}"
            }
        return Response(response)

    def delete(self, request):
        response = {'status': False}
        user = request.user.restaurant
        data = request.data
        try:
            for notification_id in data["notification_ids"]:
                notification = Notification.objects.get(id=notification_id)
                if notification.user != user:
                    raise PermissionError("This notification is not for you")
                notification.delete()
            response['status'] = True
        except Exception as e:
            response['error'] = {
                f"{e.__class__.__name__}": f"{e}"
            }
        return Response(response)


@api_view(['POST'])
@permission_classes([IsRestaurantOnly])
def mark_all_notifications_as_read(request):
    user = request.user.restaurant
    response = {"status": False}
    try:
        notifications = Notification.objects.filter(
            user=user, status="U").order_by('-created_at')
        if notifications.exists():
            for notification in notifications:
                notification.status = "R"
                notification.save()
        response['status'] = True
    except Exception as e:
        response['error'] = {
            f"{e.__class__.__name__}": f"{e}"
        }
    return Response(response)


@api_view(['GET'])
@permission_classes([IsRestaurantOnly])
def mark_a_notification_as_read(request, pk):
    user = request.user.restaurant
    response = {"status": False}
    try:
        notification = Notification.objects.get(id=pk)
        if notification.user != user:
            raise PermissionError("This notification is not for you")
        notification.status = "R"
        notification.save()
        response['status'] = True
    except Exception as e:
        response['error'] = {
            f"{e.__class__.__name__}": f"{e}"
        }
    return Response(response)
