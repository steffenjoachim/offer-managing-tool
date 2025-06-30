from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet, basename='conversation')

urlpatterns = [
    path('', include(router.urls)),
    path('conversations/<int:conversation_pk>/messages/', views.MessageViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='conversation-messages'),
    path('send_message_to_listing/', views.MessageViewSet.as_view({'post': 'send_message'}), name='send-message-to-listing'),
] 