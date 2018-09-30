from retdec.decompiler import Decompiler

decompiler = Decompiler(api_key='YOUR-API-KEY')
decompilation = decompiler.start_decompilation(input_file='activator.exe')
decompilation.wait_until_finished()
decompilation.save_hll_code()
