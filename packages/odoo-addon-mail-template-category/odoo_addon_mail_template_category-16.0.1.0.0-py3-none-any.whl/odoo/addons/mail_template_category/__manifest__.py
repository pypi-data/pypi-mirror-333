{
    'name': 'Mail Template Category',
    'version': '16.0.1.0.0',
    'depends': ['mail'],
    'author': 'Librecoop',
    'license': 'LGPL-3',
    'category': 'Productivity/Discuss',
    'description': '''
    Adds a category field to mail templates to be able to filter them
    ''',
    'installable': True,
    'auto_install': True,
    'data': [
        'security/ir.model.access.csv',
        'views/mail_template.xml',
        'views/mail_template_category.xml'
    ],
}
