# django-app-metadata

Django数据字典管理应用。

## 安装

```shell
pip install django-app-metadata
```

## 使用

*app/views.py*

```python
from django_app_metadata.models import Config

def get_config(request):
    key = reqeust.GET.get("key")
    value = Config.get(key, default=None, default_published=True, frontend_flag=True)
    return value
```

## 版本记录

### v0.1.0

- 版本首发。
- 数据字典管理。
- 数据字典获取支持缓存。

### v0.1.1

- 修改：使用`django-environment-settings`获取系统配置以增强应用的兼容性。
- 修改：`AccessToUnpublishedConfigIsForbidden`添加错误信息，支持中英双语。
- 修正：添加`django-model-helper`依赖关系。

### v0.1.2

- 修正：`Config.Meta.permissions`添加其它基础类的相关`permissions`。

### v0.1.3

- 改进：配置项管理界面。
- 改进：配置项导出文件中category使用title取代原来的id。
