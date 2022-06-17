from django.contrib import admin
from modules.module.models import SystemConfig
from project.settings import ADMIN_SITE_NAME


@admin.register(SystemConfig)
class ConfigAdmin(admin.ModelAdmin):
    list_display = (
        "name", "value", "create_time"
    )
    # 按字段排序 -表示降序
    ordering = ('-create_time',)
    # 每页显示10条
    list_per_page = 30
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('name',)

    fields = ("name", "value")


admin.site.site_title = ADMIN_SITE_NAME
admin.site.site_header = ADMIN_SITE_NAME
