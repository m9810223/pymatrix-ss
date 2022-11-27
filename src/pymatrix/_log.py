import logging
import logging.config
import pathlib


filename_width = 11
logging.config.dictConfig(
    {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                '()': 'logging.Formatter',
                'style': '{',
                'fmt': f'{{levelname:<5}} {{asctime}} {{filename:>{filename_width}}}:{{lineno:<3}} {{message}} ({{name}})',
                'datefmt': '%X',
            },
            'formatter-message': {
                '()': 'logging.Formatter',
                'style': '{',
                'fmt': f'{{levelname:<5}} {{asctime}} {{filename:>{filename_width}}}:{{lineno:<3}} {{message}} ({{name}})',
                'datefmt': '%Y-%m-%d %X',
            },
        },
        'handlers': {
            'default': {
                'formatter': 'default',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
            'handler-rotate': {
                'class': 'logging.FileHandler',
                'filename': f'{pathlib.Path.cwd()}/logfile.log',
                'formatter': 'formatter-message',
                'level': 'DEBUG',
            },
        },
        'loggers': {
            '': {
                'handlers': [
                    # 'default',
                    'handler-rotate',
                ],
                'level': 'DEBUG',
            },
        },
    }
)
logger = logging.getLogger(__name__.rsplit('.', 1)[0])
