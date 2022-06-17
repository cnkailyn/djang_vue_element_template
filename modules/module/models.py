from django.db import models


# Create your models here.
class SystemConfig(models.Model):
    """
    系统配置
    """
    name = models.CharField(max_length=50, verbose_name="名称")
    value = models.TextField(verbose_name="值")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "t_config"
        verbose_name = "系统配置"
        verbose_name_plural = "系统配置"
