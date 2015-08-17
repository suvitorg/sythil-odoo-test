{
    'name': "Entity SMS (CLICKATELL AND SMSGLOBAL)",
    'version': "1.0",
    'author': "Sythil",
    'category': "Tools",
    'summary': "Allows you send smses from any model",
    'data': [
        'views/qweb.xml',
        'esms.xml',
        'esms.gateways.csv',
        'clickatell/gateway_config.xml',
        'smsglobal/gateway_config.xml',
    ],
    'qweb': ['static/src/xml/esms_widget.xml'],
    'demo': [],
    'depends': ['web'],
    'installable': True,
}