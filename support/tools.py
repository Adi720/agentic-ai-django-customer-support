from orders.models import Order, RefundRequest
from django.utils import timezone
from .tracking_data import DELIVERY_DATA

def get_order_details(order_id):
    """
    Fetches the order details for a given order ID.

    Args:
        order_id (int): The ID of the order.

    Returns:
        Order: The order object if found, otherwise None.
    """
    try:
        order = Order.objects.get(id=order_id)
        return {
            "order_id": order.id,
            "product_name": order.product_name,
            "amount": str(order.amount),
            "status": order.status,
            "carrier": order.carrier,
            "tracking_number": order.tracking_number,
            "delivery_address": order.delivery,
            "ordered_on": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "days_since_ordered": (timezone.now() - order.created_at).days,
        }
    except Order.DoesNotExist:
        return {"error": f"Order {order_id} not found."}


def get_refund_history(user_id):
    """
    Fetches the refund request history for a given user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of refund request details for the user.

    """
    refunds = RefundRequest.objects.filter(user_id=user_id).order_by('-created_at')

    history = []
    for refund in refunds:
        history.append({
            "order_id": refund.order.id,
            "product_name": refund.order.product_name,
            "reason": refund.reason,
            "status": refund.status,
            "requested_on": refund.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            })
    return {
        "total_refund_requests": len(history),
        "history": history,
    }

def check_delivery_status(tracking_number, carrier):
    default_response = {
        "status": "Unknown",
        "last_location": "Tracking info unavailable",
        "last_update": "N/A",
        "estimated_delivery": "Contact carrier directly",
        "delay_reason": "No updates from carrier",
    }
    result = DELIVERY_DATA.get(tracking_number, default_response)
    result["tracking_number"] = tracking_number
    result["carrier"] = carrier
    return result