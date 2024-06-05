from Operations.DN_ObsCount import DN_ObsCount
from Operations.DN_Mean import DN_Mean
from Operations.DN_Median import DN_Median
from Operations.DN_STD import DN_STD
from Operations.DN_Range import DN_Range
from Operations.DN_IQR import DN_IQR
from Operations.DN_MinMax import DN_MinMax
from Operations.DN_Mode import DN_Mode
from Operations.DN_Moments import DN_Moments
from Operations.DN_Cumulants import DN_Cumulants
from Operations.DN_Burstiness import DN_Burstiness
from Operations.DN_Unique import DN_Unique
from Operations.DN_Withinp import DN_Withinp
from Operations.EN_ShannonEn import EN_ShannonEn
from Operations.DN_pleft import DN_pleft
from Operations.DN_CustomSkewness import DN_CustomSkewness
from Operations.DN_HighLowMu import DN_HighLowMu
from Operations.DN_nlogL_norm import DN_nlogL_norm
from Operations.DN_Quantile import DN_Quantile
from Operations.DN_TrimmedMean import DN_TrimmedMean
from Operations.DN_cv import DN_cv
from Operations.DN_Spread import DN_Spread
from Operations.CO_AutoCorr import CO_AutoCorr
from Operations.CO_f1ecac import CO_f1ecac
from Operations.CO_FirstMin import CO_FirstMin
from Operations.CO_FirstZero import CO_FirstZero
from Operations.CO_glscf import CO_glscf
from Operations.CO_tc3 import CO_tc3
from Operations.CO_trev import CO_trev
from Operations.DN_CompareKSFit import DN_CompareKSFit
from Operations.DT_IsSeasonal import DT_IsSeasonal
from Operations.EN_ApEn import EN_ApEn
from Operations.EN_CID import EN_CID
from Operations.EN_PermEn import EN_PermEn
from Operations.EN_SampEn import EN_SampEn
from Operations.IN_AutoMutualInfo import IN_AutoMutualInfo
from Operations.SY_Trend import SY_Trend
from Operations.FC_Suprise import FC_Suprise
from Operations.MD_hrv_classic import MD_hrv_classic
from Operations.MD_pNN import MD_pNN
from Operations.SC_HurstExp import SC_HurstExp
from Operations.EN_mse import EN_mse
from Operations.SY_LocalGlobal import SY_LocalGlobal
from Operations.CO_RM_AMInformation import CO_RM_AMInformation
from Operations.SB_TransitionMatrix import SB_TransitionMatrix
from Operations.SY_SpreadRandomLocal import SY_SpreadRandomLocal
from Operations.ST_LocalExtrema import ST_LocalExtrema
from Operations.PH_Walker import PH_Walker
from Operations.SY_PeriodVital import SY_PeriodVital
from Operations.CO_Embed2_Basic import CO_Embed2_Basic
from Operations.DN_RemovePoints import DN_RemovePoints
from Operations.DK_crinkle import DK_crinkle
from Operations.DK_theilerQ import DK_theilerQ
from Operations.SB_BinaryMethod import SB_BinaryMethod
from Operations.SY_StatAv import SY_StatAv
from Operations.EX_MovingThreshold import EX_MovingThreshold
from Operations.SB_MotifTwo import SB_MotifTwo
from Operations.SB_MotifThree import SB_MotifThree
from Operations.SY_RangeEvolve import SY_RangeEvolve
from Operations.SY_StdNthDer import SY_StdNthDer
from Operations.CO_NonlinearAutocorr import CO_NonlinearAutocorr
from Operations.EN_wentropy import EN_wentropy
from Operations.SY_DriftingMean import SY_DriftingMean

OPERATIONS_MAP = {
    'DN_ObsCount':DN_ObsCount,
    'DN_Mean': DN_Mean,
    'DN_Median': DN_Median,
    'DN_STD': DN_STD,
    'DN_Range': DN_Range,
    'DN_IQR': DN_IQR,
    'DN_MinMax': DN_MinMax,
    'DN_Mode': DN_Mode,
    'DN_Moments':DN_Moments,
    'DN_Cumulants': DN_Cumulants,
    'DN_Burstiness': DN_Burstiness,
    'DN_Unique': DN_Unique,
    'DN_Withinp': DN_Withinp,
    'EN_ShannonEn': EN_ShannonEn,
    'DN_pleft': DN_pleft,
    'DN_CustomSkewness': DN_CustomSkewness,
    'DN_HighLowMu': DN_HighLowMu,
    'DN_nlogL_norm': DN_nlogL_norm,
    'DN_Quantile': DN_Quantile,
    'DN_TrimmedMean': DN_TrimmedMean,
    'DN_cv': DN_cv,
    'DN_Spread':DN_Spread,
    'CO_AutoCorr': CO_AutoCorr,
    'CO_f1ecac': CO_f1ecac,
    'CO_FirstMin': CO_FirstMin,
    'CO_FirstZero': CO_FirstZero,
    'CO_glscf': CO_glscf,
    'CO_tc3': CO_tc3,
    'CO_trev': CO_trev,
    'DN_CompareKSFit': DN_CompareKSFit,
    'DT_IsSeasonal': DT_IsSeasonal,
    'EN_ApEn': EN_ApEn,
    'EN_CID': EN_CID,
    'EN_PermEn': EN_PermEn,
    'EN_SampEn': EN_SampEn,
    'IN_AutoMutualInfo': IN_AutoMutualInfo,
    'SY_Trend': SY_Trend,
    'FC_Suprise': FC_Suprise,
    'MD_hrv_classic': MD_hrv_classic,
    'MD_pNN': MD_pNN,
    'SC_HurstExp': SC_HurstExp,
    'EN_mse': EN_mse,
    'SY_LocalGlobal': SY_LocalGlobal,
    'CO_RM_AMInformation': CO_RM_AMInformation,
    'SB_TransitionMatrix': SB_TransitionMatrix,
    'SY_SpreadRandomLocal': SY_SpreadRandomLocal,
    'ST_LocalExtrema': ST_LocalExtrema,
    'PH_Walker': PH_Walker,
    'SY_PeriodVital': SY_PeriodVital,
    'CO_Embed2_Basic': CO_Embed2_Basic,
    'DN_RemovePoints': DN_RemovePoints,
    'DK_crinkle': DK_crinkle,
    'DK_theilerQ': DK_theilerQ,
    'SB_BinaryMethod': SB_BinaryMethod,
    'SY_StatAv': SY_StatAv,
    'EX_MovingThreshold': EX_MovingThreshold,
    'SB_MotifTwo': SB_MotifTwo,
    'SB_MotifThree': SB_MotifThree,
    'SY_RangeEvolve': SY_RangeEvolve,
    'SY_StdNthDer': SY_StdNthDer,
    'CO_NonlinearAutocorr': CO_NonlinearAutocorr,
    'EN_wentropy': EN_wentropy,
    'SY_DriftingMean': SY_DriftingMean
}
