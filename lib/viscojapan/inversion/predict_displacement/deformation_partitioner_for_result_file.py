from .deformation_partitioner import DeformPartitioner
from .deformation_partitioner_no_Raslip import DeformPartitionerNoRaslip

from ..result_file import ResultFileReader

__author__ = 'zy'
__all__ = ['gen_deformation_partitioner_for_result_file',
           'gen_deformation_partitioner_no_Raslip_for_result_fiel']

def gen_deformation_partitioner_for_result_file(
        file_G0,
        result_file,
        files_Gs = None,
        file_slip0 = None,
        sites_for_prediction = None
):
    result_file_reader = ResultFileReader(result_file)

    return DeformPartitioner(file_G0 = file_G0,
                             epochs = result_file_reader.epochs,
                             slip = result_file_reader.get_slip(),
                             files_Gs = files_Gs,
                             nlin_pars = result_file_reader.nlin_par_solved_values,
                             nlin_par_names = result_file_reader.nlin_par_names,
                             file_slip0 = file_slip0,
                             sites_for_prediction = sites_for_prediction
                             )


def gen_deformation_partitioner_no_Raslip_for_result_fiel(
        file_G0,
        result_file,
        files_Gs = None,
        file_slip0 = None,
        sites_for_prediction = None
        ):
    result_file_reader = ResultFileReader(result_file)

    return DeformPartitionerNoRaslip(file_G0 = file_G0,
                                     epochs = result_file_reader.epochs,
                                     slip = result_file_reader.get_slip(),
                                     files_Gs = files_Gs,
                                     nlin_pars = result_file_reader.nlin_par_solved_values,
                                     nlin_par_names = result_file_reader.nlin_par_names,
                                     file_slip0 = file_slip0,
                                     sites_for_prediction = sites_for_prediction
                                     )