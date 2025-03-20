#================================================================================================
#libraries:
import matplotlib.pyplot as plt 


from snl_regression_quality.modules.methods.scaling_data import ScalingData
from snl_regression_quality.modules.methods.remove_outlier import OutlierData
from snl_regression_quality.modules.metrics.calculate_assumptions import Assumptions
from snl_regression_quality.modules.metrics.calculate_quality import Quality
from snl_regression_quality.modules.methods.user_messages_initial import initial_message
from snl_regression_quality.modules.utils.global_constants import GREEN, RED, BLUE,  RESET   
#=================================================================================================



class SnlRegression:
    def __init__(self,x_data,y_data,x_data_mean, y_data_mean, waveform,significance_level):
        self.x_data = x_data
        self.y_data = y_data
        self.x_data_mean = x_data_mean
        self.y_data_mean = y_data_mean 
        self.waveform = waveform
        self.significance_level = significance_level

        initial_message()

    def run(self):

        #1) Initialization: 
        x_mean = self.x_data_mean
        y_mean = self.y_data_mean
        y_values = self.y_data

        #--------------------------------------------------------------------------------------------------
        # 2): standardization
        #--------------------------------------------------------------------------------------------------

        x_scaling, y_scaling = ScalingData(x_mean, y_mean ).run()

        #--------------------------------------------------------------------------------------------------
        # 3): remove_outlier
        #--------------------------------------------------------------------------------------------------                     

        x_deescalated, y_deescalated, indexes = OutlierData(self.waveform ,x_scaling, y_scaling,x_mean, y_mean).run()

        #--------------------------------------------------------------------------------------------------
        # 3): calculate Assumptions:
        #--------------------------------------------------------------------------------------------------
        
        enable_assumptions = Assumptions(y_mean,indexes,y_deescalated,self.significance_level).run()
        
        #--------------------------------------------------------------------------------------------------
        # 3): calculate Quality:
        #--------------------------------------------------------------------------------------------------
        if enable_assumptions:
            Quality(y_values,x_mean,y_mean,indexes,x_deescalated,y_deescalated,self.significance_level,self.waveform ).run()
        else: 
            print(RED+ f'Does not satisfies Assumption calculation!' +RESET)

