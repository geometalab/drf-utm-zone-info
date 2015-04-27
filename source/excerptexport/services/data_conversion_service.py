import os
from django.core.files import File
from excerptexport import settings
from excerptexport.models import OutputFile


def trigger_data_conversion(extraction_order, export_options):
    """
    Run data conversion script

    :param export_options: dictionary
    """
    export_formats_configuration = {}
    for export_configuration_group_key, export_configuration_group in settings.EXPORT_OPTIONS.items():
        export_formats_configuration.update(export_configuration_group['formats'])
    """
    'gis': {
        'formats': {
            'file_gdb': {
                'name': 'FileGDB',
                'file_extension': 'gdb'
            },
            'geo_package': {
                'name': 'GeoPackage',
                'file_extension': 'geo'
            }
        }
    },
    'routing': {
        'name': 'Routing',
        'formats': {
            'img': {
                'name': 'IMG',
                'file_extension': 'img'
            }
        }
    }
    """
    for export_type_key, export_type in export_options.items():
        for format_key in export_type['formats']:
            output_file = OutputFile.objects.create(
                mime_type=export_formats_configuration[format_key]['mime_type'],
                extraction_order=extraction_order
            )

            data_directory = settings.APPLICATION_SETTINGS['data_directory']
            if not os.path.exists(data_directory):
                os.makedirs(data_directory)
            file_path = data_directory + '/' \
                + str(output_file.public_identifier) + '.' + export_formats_configuration[format_key]['file_extension']

            with open(file_path, 'w') as file_reference:
                new_file = File(file_reference)
                new_file.write(str(output_file.public_identifier))

            # file must be committed, so reopen to attach to model
            output_file.file = file_path
            output_file.save()
