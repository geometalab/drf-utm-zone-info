import subprocess

import os
import tempfile
from django.utils import timezone
from rq import get_current_job

from osmaxx.conversion._settings import CONVERSION_SETTINGS

from osmaxx.conversion.converters.utils import zip_folders_relative, recursive_getsize

_path_to_commandline_utils = os.path.join(os.path.dirname(__file__), 'command_line_utils')


class Garmin:
    def __init__(self, *, out_zip_file_path, area_name, polyfile_string):
        self._resulting_zip_file_path = out_zip_file_path
        self._map_description = area_name
        self._osmosis_polygon_file = tempfile.NamedTemporaryFile(suffix='.poly', mode='w')
        self._osmosis_polygon_file.write(polyfile_string)
        self._osmosis_polygon_file.flush()
        self._polyfile_path = self._osmosis_polygon_file.name
        self._start_time = None

    def create_garmin_export(self):
        self._start_time = timezone.now()
        unzipped_result_size = self._to_garmin()
        self._osmosis_polygon_file.close()
        job = get_current_job()
        if job:
            job.meta['duration'] = timezone.now() - self._start_time
            job.meta['unzipped_result_size'] = unzipped_result_size
            job.save()

    def _to_garmin(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_out_dir = os.path.join(tmp_dir, 'garmin')
            config_file_path = self._split(tmp_dir)
            unzipped_result_size = self._produce_garmin(config_file_path, tmp_out_dir)
            self._create_zip(tmp_out_dir)
        return unzipped_result_size

    def _split(self, workdir):
        _splitter_path = os.path.abspath(os.path.join(_path_to_commandline_utils, 'splitter', 'splitter.jar'))
        subprocess.check_call([
            'java',
            '-jar', _splitter_path,
            '--output-dir={0}'.format(workdir),
            '--description={0}'.format(self._map_description),
            '--polygon-file={}'.format(self._polyfile_path),
            CONVERSION_SETTINGS.get('PBF_PLANET_FILE_PATH'),
        ])
        config_file_path = os.path.join(workdir, 'template.args')
        return config_file_path

    def _produce_garmin(self, config_file_path, out_dir):
        out_dir = os.path.join(out_dir, 'garmin')  # hack to get a subdirectory in the zipfile.
        os.makedirs(out_dir, exist_ok=True)

        _mkgmap_path = os.path.abspath(os.path.join(_path_to_commandline_utils, 'mkgmap', 'mkgmap.jar'))
        mkg_map_command = ['java', '-jar', _mkgmap_path]
        output_dir = ['--output-dir={0}'.format(out_dir)]
        config = ['--read-config={0}'.format(config_file_path)]

        subprocess.check_call(
            mkg_map_command +
            output_dir +
            config
        )
        unzipped_result_size = recursive_getsize(out_dir)
        return unzipped_result_size

    def _create_zip(self, data_dir):
        zip_folders_relative([data_dir], self._resulting_zip_file_path)
