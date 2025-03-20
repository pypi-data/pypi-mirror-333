from Modul_Wrapper import Wrap
import inspect, uvicorn

class Processing(Wrap):
	def __init__(kimin, **parameter):
		kimin.parameter = parameter
		super().__init__(modul_path=parameter.get('path_modul', {"modul":[]}), debug=False)
		kimin.config = kimin.modul['ext'](modul=kimin.modul).ReadFile(path=kimin.parameter['config_path'], tipe='json', mode='r')['data']
		kimin.base_dir = kimin.Base_Dir()
		kimin.modul['colorama'].init()
	
	def Base_Dir(kimin):
		stack = inspect.stack()
		for frame_info in stack:
			# Menghindari frame dari modul ini sendiri
			if frame_info.filename != __file__:
				# Mendapatkan path dari file yang memanggil fungsi ini
				caller_file = frame_info.filename
				# Mendapatkan base path dari file pemanggil
				caller_base_path = kimin.modul['os'].path.dirname(kimin.modul['os'].path.abspath(caller_file))
				return caller_base_path
		return None
	
	def Run_Server(kimin):
		x = kimin.modul['server'](config=kimin.parameter['config_path'], modul=kimin.modul, base_dir=kimin.base_dir)
		# if len(kimin.modul['sys'].argv) > 1 and kimin.modul['sys'].argv[1] == 'generate':
			# x.Prepare()
			# print("File Routes Berhasil Di Generate\nSilahkan Jalankan Ulang!!")
			# kimin.modul['sys'].exit(1)
		
		# elif len(kimin.modul['sys'].argv) > 1 and kimin.modul['sys'].argv[1] == 'set-fe':
			# x.Set_FE()
			# print("File File Berhasil Di Generate\nSilahkan Jalankan Ulang!!")
			# kimin.modul['sys'].exit(1)
		
		server = x.Server()
		x.Routes(server)
		if 'ssl' in kimin.config['server'] and 'cert' in kimin.config['server']['ssl'] and 'key' in kimin.config['server']['ssl'] and kimin.config['server']['ssl']['cert'] and kimin.config['server']['ssl']['key']:
			uvicorn.run(server, host=kimin.config['server']['host'], port=kimin.config['server']['port'], ssl_keyfile=kimin.config['server']['ssl']['key'], ssl_certfile=kimin.config['server']['ssl']['cert'])
		else:
			uvicorn.run(server, host=kimin.config['server']['host'], port=kimin.config['server']['port'])