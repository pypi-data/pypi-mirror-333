from tal.enums import FileFormat, GridFormat, HFormat, VolumeFormat
from tal.log import log, LogLevel
from tal.util import SPEED_OF_LIGHT
import numpy as np


def __convert_dict_znlos_to_tal(capture_data: dict) -> dict:
    H = capture_data['data']
    if H.ndim == 7:
        # Exhaustive/single - convert to (colors, bounces, t, lx, ly, sx, sy)
        if H.shape[4] == 6:
            # assume (ly, lx, sy, sx, bounces, t, colors)
            H = np.moveaxis(H, list(range(7)), (4, 3, 6, 5, 1, 2, 0))
        elif H.shape[2] == 6:
            # assume (colors, t, bounces, sx, sy, lx, ly)
            H = np.moveaxis(H, list(range(7)), (0, 2, 1, 6, 5, 4, 3))
        else:
            raise AssertionError(
                'Conversion not detected for this H.ndim = 7 case')
    elif H.ndim == 5:
        # Confocal - convert to (colors, bounces, t, sx, sy)
        if H.shape[0] == H.shape[1]:
            # assume (sy, sx, bounces, t, colors)
            H = np.moveaxis(H, list(range(5)), (3, 4, 1, 2, 0))
        elif H.shape[3] == H.shape[4]:
            # assume (colors, t, bounces, sx, sy)
            H = np.moveaxis(H, list(range(5)), (0, 2, 1, 4, 3))
        else:
            raise AssertionError(
                'Conversion not detected for this H.ndim = 5 case')
    else:
        raise AssertionError('Conversion not implemented for H.ndim != 5 or 7')
    # sum colors and bounces dims (t, lx, ly, sx, sy)
    H = np.sum(H, axis=(0, 1))
    # remove (1, 1) dims (e.g. laser in single capture 1x1x256x256)
    H = np.squeeze(H)
    H_format = HFormat.T_Sx_Sy if H.ndim == 3 else HFormat.T_Lx_Ly_Sx_Sy

    def conv_to_xy3(arr):
        if arr.shape[0] == 3:
            return np.transpose(arr)
        else:
            return arr

    def parse_volume_size(volume_size):
        volume_size = np.array(volume_size, dtype=np.float32)
        if volume_size.size == 1:
            volume_size = np.repeat(volume_size, 3)
        return volume_size

    return {
        'H': H,
        'H_format': H_format,
        'sensor_xyz': capture_data['cameraPosition'].reshape(3),
        'sensor_grid_xyz': conv_to_xy3(capture_data['cameraGridPositions']),
        'sensor_grid_normals': conv_to_xy3(capture_data['cameraGridNormals']),
        'sensor_grid_format': GridFormat.X_Y_3,
        'laser_xyz': capture_data['laserPosition'].reshape(3),
        'laser_grid_xyz': conv_to_xy3(capture_data['laserGridPositions']),
        'laser_grid_normals': conv_to_xy3(capture_data['laserGridNormals']),
        'laser_grid_format': GridFormat.X_Y_3,
        'volume_format': VolumeFormat.X_Y_Z_3,
        'delta_t': capture_data['deltaT'],
        't_start': capture_data['t0'],
        't_accounts_first_and_last_bounces': True,
        'scene_info': {
            'original_format': 'HDF5_ZNLOS',
            'volume': {
                'center': capture_data['hiddenVolumePosition'].reshape(3),
                'rotation': capture_data['hiddenVolumeRotation'].reshape(3),
                'size': parse_volume_size(capture_data['hiddenVolumeSize']),
            }
        },
    }


def __convert_dict_dirac_to_tal(capture_data: dict) -> dict:
    t_accounts_first_and_last_bounces = np.isclose(
        0.0, np.linalg.norm(capture_data['offset_laser']))

    nx = len(capture_data['xa'])
    ny = len(capture_data['ya'])
    da = capture_data['da']
    nt = len(da)

    sensor_grid = np.stack(
        (capture_data['xg'],
         capture_data['yg'],
         np.zeros((nx, ny), dtype=np.float32)),
        axis=-1)
    laser_grid = np.copy(sensor_grid)

    def expand(vec, x, y):
        assert len(vec) == 3
        return vec.reshape(1, 1, 3).repeat(x, axis=0).repeat(y, axis=1)

    log(LogLevel.WARNING, 'Converting from HDF5_NLOS_DIRAC does some assumptions '
        'on the positions of the laser and sensor. If your data has '
        't_accounts_first_and_last_bounces = True, it has a chance to be wrong.')

    return {
        'H': capture_data['data_t'],
        'H_format': HFormat.T_Sx_Sy,
        'sensor_xyz': np.array([-0.5, 0, 0.25], dtype=np.float32),
        'sensor_grid_xyz': sensor_grid,
        'sensor_grid_normals': expand(np.array([0.0, 0.0, 1.0], dtype=np.float32), nx, ny),
        'sensor_grid_format': GridFormat.X_Y_3,
        'laser_xyz': np.array([-0.5, 0, 0.25], dtype=np.float32),
        'laser_grid_xyz': laser_grid,
        'laser_grid_normals': expand(np.array([0.0, 0.0, 1.0], dtype=np.float32), nx, ny),
        'laser_grid_format': GridFormat.X_Y_3,
        'volume_format': VolumeFormat.X_Y_Z_3,
        'delta_t': da[1] - da[0],
        't_start': None if t_accounts_first_and_last_bounces else 0.0,
        't_accounts_first_and_last_bounces': t_accounts_first_and_last_bounces,
        'scene_info': {
            'original_format': 'HDF5_NLOS_DIRAC',
            'offset': {
                'sensor': capture_data['offset_camera'].reshape(nx, ny),
                'laser': capture_data['offset_laser'].reshape(1, 1),
            },
            'sample_wavelength': {
                'x': capture_data['sample_x'],
                'y': capture_data['sample_y'],
            }
        },
    }


def __convert_dict_pfmat_to_tal(capture_data: dict) -> dict:
    dataset = capture_data['dataset']

    nt_expected = dataset['t']
    H = dataset['data']
    nt, ns, nl = H.shape
    assert H.ndim == 3 and nt == nt_expected and ns == 1, \
        'Conversion assumes H to be of shape (nt, ns, nl)'
    # convert to (nt, nl)
    H = np.squeeze(H)

    def conv_to_n3(arr, expected_len=None):
        if arr.shape[0] == 3:
            arr = np.transpose(arr)
        if expected_len is not None and arr.shape[0] == 1:
            arr = np.stack((arr,) * expected_len, axis=0)
        return arr

    # NOTE(diego): this data typically uses one camera position,
    # and multiple laser positions, taking advantage of the fact that
    # light propagation in both path directions (laser->sensor and sensor->laser)
    # is equivalent. We invert laser and sensors to be more consistent with
    # other dataset types and existing code
    return {
        'H': H,
        'H_format': HFormat.T_Si,
        'sensor_xyz': dataset['laserOrigin'].reshape(3),
        'sensor_grid_xyz': conv_to_n3(dataset['laserPos']),
        'sensor_grid_normals': conv_to_n3(dataset['laserNorm'], expected_len=nl),
        'sensor_grid_format': GridFormat.N_3,
        'laser_xyz': dataset['cameraOrigin'].reshape(3),
        'laser_grid_xyz': conv_to_n3(dataset['cameraPos']),
        'laser_grid_normals': conv_to_n3(dataset['cameraNorm'], expected_len=ns),
        'laser_grid_format': GridFormat.N_3,
        'volume_format': VolumeFormat.X_Y_Z_3,
        'delta_t': dataset['deltat'],
        't_start': dataset['t0'],
        't_accounts_first_and_last_bounces': True,
        'scene_info': {
            'original_format': 'MAT_PHASOR_FIELDS',
            'volume': {
                'minimal_pos': capture_data['minimalpos'].reshape(3),
                'maximal_pos': capture_data['maximalpos'].reshape(3),
                'sampling_grid_spacing': capture_data['sampling_grid_spacing'],
            }
        },
    }


def __convert_dict_pfdiffmat_to_tal(capture_data: dict) -> dict:
    H = capture_data['rect_data']

    _, nsx, nsy = H.shape
    sampling_grid_spacing = np.array(
        capture_data['sampling_spacing']).item()
    delta_t = np.array(capture_data['ts']).item()
    delta_t *= SPEED_OF_LIGHT
    spad_x, spad_y = np.array(
        capture_data['SPAD_index'], dtype=np.int32).flatten()

    grid_x = (np.arange(nsx) - nsx / 2) * sampling_grid_spacing
    grid_y = (np.arange(nsy) - nsy / 2) * sampling_grid_spacing
    sensor_grid_xyz = np.stack(np.meshgrid(
        grid_x, grid_y, [0], indexing='ij'), axis=-1)
    sensor_grid_xyz = sensor_grid_xyz.squeeze()

    return {
        'H': H,
        'H_format': HFormat.T_Sx_Sy,
        'sensor_xyz': None,
        'sensor_grid_xyz': sensor_grid_xyz,
        'sensor_grid_normals': None,
        'sensor_grid_format': GridFormat.X_Y_3,
        'laser_xyz': None,
        'laser_grid_xyz': sensor_grid_xyz[spad_x:spad_x+1, spad_y:spad_y+1],
        'laser_grid_normals': None,
        'laser_grid_format': GridFormat.X_Y_3,
        'volume_format': VolumeFormat.X_Y_Z_3,
        'delta_t': delta_t,
        't_start': 0,
        't_accounts_first_and_last_bounces': False,
        'scene_info': {
            'original_format': 'MAT_PHASOR_FIELD_DIFFRACTION',
            'volume': {
                'sampling_grid_spacing': capture_data['sampling_spacing'],
            }
        },
    }


def __convert_dict_tal_to_znlos(capture_data: dict) -> dict:
    raise NotImplementedError('Conversion to HDF5_ZNLOS not implemented')


def __convert_dict_tal_to_dirac(capture_data: dict) -> dict:
    raise NotImplementedError('Conversion to HDF5_NLOS_DIRAC not implemented')


def __convert_dict_tal_to_pfmat(capture_data: dict) -> dict:
    raise NotImplementedError(
        'Conversion to MAT_PHASOR_FIELDS not implemented')


def __convert_dict_tal_to_pfdiffmat(capture_data: dict) -> dict:
    raise NotImplementedError(
        'Conversion to MAT_PHASOR_FIELD_DIFFRACTION not implemented')


def detect_dict_format(raw_data: dict) -> FileFormat:
    if 'data' in raw_data:
        return FileFormat.HDF5_ZNLOS
    elif 'data_t' in raw_data:
        return FileFormat.HDF5_NLOS_DIRAC
    elif 'H' in raw_data:
        return FileFormat.HDF5_TAL
    elif 'dataset' in raw_data:
        return FileFormat.MAT_PHASOR_FIELDS
    elif 'rect_data' in raw_data:
        return FileFormat.MAT_PHASOR_FIELD_DIFFRACTION
    else:
        raise AssertionError('Unable to detect capture data file format')


def convert_dict(capture_data: dict,
                 format_to: FileFormat) -> dict:
    """
    Convert raw data from one format to another
    """
    # convert to HDF5_TAL
    file_format = detect_dict_format(capture_data)
    if file_format == FileFormat.HDF5_TAL:
        capture_data_tal = capture_data
    elif file_format == FileFormat.HDF5_ZNLOS:
        capture_data_tal = __convert_dict_znlos_to_tal(capture_data)
    elif file_format == FileFormat.HDF5_NLOS_DIRAC:
        capture_data_tal = __convert_dict_dirac_to_tal(capture_data)
    elif file_format == FileFormat.MAT_PHASOR_FIELDS:
        capture_data_tal = __convert_dict_pfmat_to_tal(capture_data)
    elif file_format == FileFormat.MAT_PHASOR_FIELD_DIFFRACTION:
        capture_data_tal = __convert_dict_pfdiffmat_to_tal(capture_data)
    else:
        raise AssertionError(
            'convert_dict not implemented for this file format')

    # convert from HDF5_TAL to output format
    if format_to == FileFormat.HDF5_TAL:
        return capture_data_tal
    elif format_to == FileFormat.HDF5_ZNLOS:
        return __convert_dict_tal_to_znlos(capture_data_tal)
    elif format_to == FileFormat.HDF5_NLOS_DIRAC:
        return __convert_dict_tal_to_dirac(capture_data_tal)
    elif format_to == FileFormat.MAT_PHASOR_FIELDS:
        return __convert_dict_tal_to_pfmat(capture_data_tal)
    elif format_to == FileFormat.MAT_PHASOR_FIELD_DIFFRACTION:
        return __convert_dict_tal_to_pfdiffmat(capture_data_tal)
    else:
        raise AssertionError(
            'convert_dict not implemented for this file format')
