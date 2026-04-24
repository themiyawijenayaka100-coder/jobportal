from accounts.models import DirectMessage, Notification


def unread_notifications_count(request):
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return {
            "unread_notifications_count": 0,
            "unread_message_count": 0,
            "recent_messages": [],
        }

    return {
        "unread_notifications_count": Notification.objects.filter(
            recipient=request.user, is_read=False
        ).count(),
        "unread_message_count": DirectMessage.objects.filter(
            recipient=request.user, is_read=False
        ).count(),
        "recent_messages": DirectMessage.objects.filter(recipient=request.user)
        .select_related("sender")
        .only("id", "sender__username", "subject", "body", "sent_at", "is_read")
        [:10],
    }

