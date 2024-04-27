from .models import WeChatUser, Status
from django.shortcuts import redirect, render
from config import APP_CODE


def home(request):
    return render(request, 'homepage.html')


def show_user(request):
    # 获取蓝鲸⽤户id
    user_id = request.user.id
    # 获取 WeChatUser 对象
    wechat_user = WeChatUser.objects.get(user_id=user_id)
    return render(request, 'user.html', {'user': wechat_user})


def show_status(request):
    statuses = Status.objects.all()
    return render(request, 'status.html', {'statuses': statuses})


def submit_post(request):
    user = WeChatUser.objects.get(user=request.user)
    text = request.POST.get('text')
    if text:
        status = Status(user=user, text=text)
        status.save()
        return redirect(f'/stag--{APP_CODE}/status')
    return render(request, 'my_post.html')


from django.conf import settings
from django.http import HttpResponse

from blueapps.account import get_user_model


def set_super_user(request):
    """
    添加用户为管理员
    """
    User = get_user_model()
    for name in settings.INIT_SUPERUSER:
        User.objects.update_or_create(
            username=name,
            defaults={'is_staff': True, 'is_active': True, 'is_superuser': True}
        )
    return HttpResponse('Success')
