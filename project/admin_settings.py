# 首页页面url和名称
SIMPLEUI_HOME_PAGE = '/data-analysis'
SIMPLEUI_HOME_TITLE = '数据分析'

SIMPLEUI_CONFIG = {
    'system_keep': False,
    'menu_display': ['业务管理', '用户管理', '系统配置'],
    'dynamic': True,
    'menus': [
        {
            'name': '业务管理',
            # 二级菜单
            'models': [{
                'name': '词组',
                'url': 'main/wordgroup/',
                "icon": "fa fa-layer-group"
            }, {
                'name': '词语',
                'url': 'main/keyword/',
                "icon": "fa fa-file-word"
            },
                {
                    'name': '数据',
                    'url': 'main/data/'
                }
            ]
        },
        {
            'app': 'auth',
            'name': '用户管理',
            'icon': 'fas fa-user-shield',
            'models': [{
                'name': '用户',
                'url': 'auth/user/'
            },
                {
                    'name': '用户组',
                    'url': 'auth/group/',
                    "icon": "fas fa-user-shield"
                }
            ]
        },
        {
            'app': 'main',
            'name': '系统配置',
            'icon': 'fas fa-user-shield',
            'url': 'main/config/'
        }
    ]
}