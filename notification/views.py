from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from user.customer_utils import customer_details
from .utils import notification_details
from .models import Notification as NotificationModel
from permissions import IsRestaurantOnly

# Create your views here.


class Notifications(APIView):
    permission_classes = [IsRestaurantOnly]

    def get(self, request):
        response = {'status': False}
        user = request.user.restaurant
        try:
            notifications = NotificationModel.objects.filter(
                user=user).order_by('created_at')
            if notifications.exists():
                response['notifications'] = notification_details(notifications)
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
        """
        Takes a list of notification ids:\n
        {

            "notification_ids": [1, 3, 5]

        }
        """
        response = {'status': False}
        user = request.user.restaurant
        data = request.data
        try:
            for notification_id in data["notification_ids"]:
                notification = NotificationModel.objects.get(
                    id=notification_id)
                if notification.user != user:
                    raise PermissionError("This notification is not for you")
                notification.delete()
            response['status'] = True
        except Exception as e:
            response['error'] = {
                f"{e.__class__.__name__}": f"{e}"
            }
        return Response(response)


class NotificationDetail(APIView):
    permission_classes = [IsRestaurantOnly]

    def get(self, request, pk):
        response = {'status': False}
        user = request.user.restaurant
        try:
            notification = NotificationModel.objects.get(id=pk)
            if user != notification.user:
                raise PermissionError(
                    "You are not allowed to view this notification.")
            order_item = notification.order_item
            response["food_item_name"] = order_item.food_item.name
            response["quantity"] = order_item.quantity
            customer_email = order_item.user.customer.email
            response['delivery_address'] = notification.shipping_address
            response['customer'] = customer_details(customer_email)
            response['customer'].pop('address')
            response['status'] = True
        except Exception as e:
            response['error'] = {
                f"{e.__class__.__name__}": f"{e}"
            }
        return Response(response)


@api_view(['POST'])
@permission_classes([IsRestaurantOnly])
def mark_all_notifications_as_read(request):
    """
    A post request to this link marks all notifications as read
    """
    user = request.user.restaurant
    response = {"status": False}
    try:
        notifications = NotificationModel.objects.filter(
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
        notification = NotificationModel.objects.get(id=pk)
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
