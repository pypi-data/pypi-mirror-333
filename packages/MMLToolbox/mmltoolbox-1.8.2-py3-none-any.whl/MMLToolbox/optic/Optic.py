
import chrpy
import time

from chrpy.chr_cmd_id import *
from chrpy.chr_connection import *
from chrpy.chr_utils import Data

class Optic:

    def __init__(self,IPAdress = '192.168.170.2'):
        self.IPAdresse = IPAdress
    
    def getDistance(self):
        
        config = ConnectionConfig()
        config.address = self.IPAdresse    
        output_format = OutputDataMode.DOUBLE

        with connection_from_config(config=config) as conn:
            conn.set_output_data_format_mode(output_format)
            # Set the signals.
            resp = conn.exec('SODX', 83, 256)
            #print(resp)

            signals = conn.get_device_output_signals()
            #print("Signals:", signals)

            
                 # Do it oneself, without waiting
            _ = conn.activate_auto_buffer_mode(1, flush_buffer=True)
            data = conn.get_auto_buffer_new_samples()
            
            status = conn.get_auto_buffer_status()
            if status == AutoBuffer.ERROR:
                raise Exception("Bla")
            elif status != AutoBuffer.FINISHED:
                time.sleep(0.01)


            conn.deactivate_auto_buffer_mode()
            print("Finished getting samples without waiting")
            print(data.signal_info)
            value = data.get_signal_values_all(256)
            return (value[0])
