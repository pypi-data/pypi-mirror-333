import numpy as np
import math
import time
import optuna
import torch
import piq
from polynomial_preprocessing import preprocesamiento_datos_a_grillar, procesamiento_datos_grillados
from polynomial_preprocessing.image_synthesis import conjugate_gradient
from optuna.visualization import plot_contour
from optuna.visualization import plot_edf
from optuna.visualization import plot_intermediate_values
from optuna.visualization import plot_optimization_history
from optuna.visualization import plot_parallel_coordinate
from optuna.visualization import plot_param_importances
from optuna.visualization import plot_rank
from optuna.visualization import plot_slice
from optuna.visualization import plot_timeline
from plotly.io import show

class OptimizacionParametrosGrillados:
	def __init__(self, fits_path, ms_path, poly_limits, division_limits, pixel_size = None, image_size = None, n_iter_gc = 100):
		self.fits_path = fits_path  # Ruta de archivo FITS
		self.ms_path = ms_path # Ruta de archivo MS
		self.poly_limits = poly_limits # [Lim. Inferior, Lim. Superior] -> Lista (Ej: [5, 20])
		self.division_limits = division_limits # [Lim. Inferior, Lim. Superior] -> Lista (Ej: [1e-3, 1e0])
		self.pixel_size = pixel_size # Tamaño del Pixel
		self.image_size = image_size # Cantidad de pixeles para la imagen
		self.n_iter_gc = n_iter_gc

		if self.pixel_size is None:
			pixel_size = preprocesamiento_datos_a_grillar.PreprocesamientoDatosAGrillar(fits_path=self.fits_path,
																						 ms_path=self.ms_path,
																						image_size=self.image_size)
			_, _, _, _, pixels_size = pixel_size.fits_header_info()
			print("Pixel size of FITS: ", pixels_size)
			self.pixel_size = pixels_size

		if self.image_size is None:
			fits_header = preprocesamiento_datos_a_grillar.PreprocesamientoDatosAGrillar(fits_path=self.fits_path,
																						 ms_path=self.ms_path,
																						 image_size=self.image_size)

			_, fits_dimensions, _, _, _ = fits_header.fits_header_info()
			print("Image size of FITS: ", fits_dimensions[1])
			self.image_size = fits_dimensions[1]

		grid_visibilities, grid_weights, _, grid_u, grid_v = (preprocesamiento_datos_a_grillar.
																PreprocesamientoDatosAGrillar(self.fits_path,
																								self.ms_path,																										
																									image_size = self.image_size).
																		  process_ms_file())
		
		self.gridded_visibilities = grid_visibilities

		self.gridded_weights = grid_weights

		self.grid_u = grid_u

		self.grid_v = grid_v
	


	@staticmethod
	def generate_filename(prefix, poly_limits, division_limits, pixel_size, num_pixels, object_name, extension):
		base_title = f"num_polynomial_{poly_limits[0]}_{poly_limits[1]}_division_sigma_{division_limits[0]}_{division_limits[1]}_pixel_size_{pixel_size}_image_size_{num_pixels}_{num_pixels}_{object_name}"
		return f"{prefix}{base_title}.{extension}"
	
	@staticmethod
	def create_mask(grid_shape, radius):
		"""
		Crea un arreglo de máscara basado en un filtro circular.

		Parameters:
		- grid_shape: tuple, las dimensiones de la grilla (rows, cols).
		- radius: float, el radio del círculo.

		Returns:
		- mask: numpy.ndarray, una matriz booleana donde True indica fuera del círculo y False dentro.
		"""
		# Crear coordenadas de la grilla
		rows, cols = grid_shape
		y, x = np.ogrid[:rows, :cols]

		# Calcular el centro de la grilla
		center_row, center_col = rows // 2, cols // 2

		# Calcular la distancia de cada punto al centro
		distance_from_center = np.sqrt((x - center_col) ** 2 + (y - center_row) ** 2)

		# Crear la máscara: True para fuera del círculo, False dentro
		mask = distance_from_center > radius
		return mask

	def mse(self, img_final, dim_grilla, radio):
		bool_arreglo = self.create_mask(dim_grilla, radio)
		# print(bool_arreglo)
		B = img_final * bool_arreglo
		mse = np.std(B) ** 2
		print(mse)
		return mse

	# Para minimizar se debe colocar un signo menos

	def psnr(self, img_fin):
		psnr_result = 20 * math.log10(np.max(np.max(img_fin)) / self.mse(img_fin, (self.image_size, self.image_size), 47))
		return psnr_result  # comentary mse need to be taken outside the object

	@staticmethod
	def compute_brisque(image):
	
		"""
		Calcula el score BRISQUE para una imagen dada.

		Parameters:
		- image: numpy.ndarray, la imagen a evaluar.

		Returns:
		- brisque_score: float, el score BRISQUE de la imagen.
		"""
		# Convertir la imagen a un tensor de PyTorch
		image_tensor = torch.from_numpy(image).unsqueeze(0).unsqueeze(0).float()

		# Calcular el score BRISQUE
		brisque_score = piq.brisque(image_tensor, data_range=255., reduction='none')

		return brisque_score.item()
	
	def grid_data(self):
		gridded_visibilities, gridded_weights, pixel_size, grid_u, grid_v = (preprocesamiento_datos_a_grillar.
																		  PreprocesamientoDatosAGrillar(self.fits_path,
																										self.ms_path,																										
																										image_size = self.image_size).
																		  process_ms_file())
		return gridded_visibilities, gridded_weights, pixel_size, grid_u, grid_v

	def optimize_parameters(self, trial):
		
		start_time = time.time()
		
		# Cargamos los archivos de entrada
		header, fits_dimensions, fits_data, du, pixel_size = (preprocesamiento_datos_a_grillar.
																	PreprocesamientoDatosAGrillar(self.fits_path,
																								  self.ms_path,																								  
																								  image_size = self.image_size).
																	fits_header_info())


		################# Parametros iniciales #############
		M = 1  # Multiplicador de Pixeles
		N1 = self.image_size  # Numero de pixeles
		N1 = N1 * M  # Numero de pixeles,  multiplicador #Version MS
		S = trial.suggest_int("S", self.poly_limits[0], self.poly_limits[1])  # Rango del número de polinomios
		sub_S = int(S)
		ini = 1  # Tamano inicial
		division = trial.suggest_float("division", self.division_limits[0], self.division_limits[1])
		pixel_size = self.pixel_size

		########################################## Cargar archivo de entrada Version MS
		# Eliminamos la dimension extra
		u_ind, v_ind = np.nonzero(self.gridded_visibilities[0])
		gridded_visibilities_2d = self.gridded_visibilities[0].flatten()  # (1,251,251)->(251,251)
		gridded_weights_2d = self.gridded_weights[0].flatten()  # (1,251,251)->(251,251)

		# Filtramos por los valores no nulos
		nonzero_indices = np.nonzero(gridded_weights_2d)
		gv_sparse = gridded_visibilities_2d[nonzero_indices]
		gw_sparse = gridded_weights_2d[nonzero_indices]

		# Normalizacion de los datos

		gv_sparse = (gv_sparse / np.sqrt(np.sum(gv_sparse ** 2)))
		gw_sparse = (gw_sparse / np.sqrt(np.sum(gw_sparse ** 2)))

		u_data = self.grid_u[u_ind]
		v_data = self.grid_v[v_ind]

		du = 1 / (N1 * pixel_size)

		umax = N1 * du / 2

		u_sparse = np.array(u_data) / umax
		v_sparse = np.array(v_data) / umax

		u_target = np.reshape(np.linspace(-ini, ini, N1), (1, N1)) * np.ones(shape=(N1, 1))
		v_target = np.reshape(np.linspace(-ini, ini, N1), (N1, 1)) * np.ones(shape=(1, N1))

		z_target = u_target + 1j * v_target
		z_sparse = u_sparse + 1j * v_sparse

		b = 1

		z_exp = np.exp(-z_target * np.conjugate(z_target) / (2 * b * b))

		max_memory = 120000000
		max_data = float(int(max_memory / (S * S)))

		divide_data = int(np.size(gv_sparse[np.absolute(gv_sparse) != 0].flatten()) / max_data) + 1
		divide_target = int(N1 * N1 / max_data) + 1

		if divide_target > divide_data:
			divide_data = int(divide_target)

		if divide_data > int(divide_data):
			divide_data = int(divide_data) + 1

		chunk_data = int(((S * S) / divide_data) ** (1 / 2)) + 1
		if chunk_data == 0:
			chunk_data = 1

		# chunk_data = 1
		#print(chunk_data)

		visibilities_model = np.zeros((N1, N1), dtype=np.complex128)

		print("New S:", S)
		print("Division:", division)

		visibilities_aux = np.zeros(N1 * N1, dtype=np.complex128)
		weights_aux = np.zeros(N1 * N1, dtype=float)

		

		# print(z_target.dtype)
		# print(z_sparse.dtype)
		# print(gw_sparse.dtype)
		# print(gv_sparse.dtype)
		# print(type(chunk_data))

		# Obtencion de los datos de la salida con G-S

		data_processing = procesamiento_datos_grillados.ProcesamientoDatosGrillados(self.fits_path, self.ms_path, S, division, self.pixel_size, self.image_size, verbose = False)

		try:
			visibilities_mini, err, residual, P_target, P = (data_processing.recurrence2d
															 (z_target.flatten(),
															  z_sparse.flatten(),
															  gw_sparse.flatten(),
															  gv_sparse.flatten(),
															  np.size(z_target.flatten()),
															  S,
															  division,
															  chunk_data)
															 )

			visibilities_mini = np.reshape(visibilities_mini, (N1, N1))

			visibilities_model = np.array(visibilities_mini)

			weights_model = np.zeros((N1, N1), dtype=float)

			sigma_weights = np.divide(1.0, gw_sparse, where=gw_sparse != 0,
									  out=np.zeros_like(gw_sparse))  # 1.0/gw_sparse
			sigma = np.max(sigma_weights) / division
			weights_mini = np.array(1 / err)
			weights_mini[np.isnan(weights_mini)] = 0.0
			weights_mini[np.isinf(weights_mini)] = 0.0

			weights_mini = np.reshape(weights_mini, (N1, N1))

			weights_model = np.array(weights_mini)

			

			####################################### GENERACION DE GRAFICOS DE SALIDA #####################################

			image_model = (np.fft.fftshift
						   (np.fft.ifft2
							(np.fft.ifftshift
							 (visibilities_model * weights_model / np.sum(weights_model.flatten())))) * N1 ** 2)
			image_model = np.array(image_model.real)
			
			reconstructed_image = conjugate_gradient.ConjugateGradient(visibilities_model, weights_model, self.n_iter_gc)

			reconstructed_image_cg = reconstructed_image.CG()
			# Procesamiento adicional para calcular métrica de evaluación (PSNR, MSE, etc.)
		
			# Normalizar imagen para las métricas
			synthesized_image = reconstructed_image_cg - reconstructed_image_cg.min()
			synthesized_image = (synthesized_image / synthesized_image.max()) * 255
			synthesized_image = synthesized_image.astype(np.uint8)

			# Calcular métricas
			brisque_score = self.compute_brisque(synthesized_image)

			print("El tiempo de ejecución fue de: ", time.time() - start_time)

			# Minimizar ambas métricas (menores valores indican mejor calidad)
			return brisque_score
		
		except Exception as e:
			print(f"Error en el cálculo: {e}")
			return float("inf")
		
		"""
			psnr_result = self.psnr(np.real(image_model))
			return -psnr_result  # Negativo porque Optuna minimiza la métrica
		except Exception as e:
			print(f"Error en el cálculo: {e}")
			return float("inf")  # Penalizar valores inválidos
		"""
		
	def initialize_optimization(self, num_trials):
		# Configuración del estudio de Optuna
		study = optuna.create_study(direction="minimize")
		study.optimize(self.optimize_parameters, n_trials=num_trials)

		# Resultados
		
		print("Mejores parametros:", study.best_params)
		print("Mejor valor (BRISQUE):", study.best_value)


		convergencia = plot_optimization_history(study)

		convergencia.update_layout(
			title="Optimización de parámetros usando BRISQUE",
			xaxis_title="Intento",
			yaxis_title="BRISQUE",
		)

		show(convergencia)

		interferometric_data = preprocesamiento_datos_a_grillar.PreprocesamientoDatosAGrillar(fits_path=self.fits_path,
																							   ms_path=self.ms_path)
		fits_header, _, _, _, _ = interferometric_data.fits_header_info()

		TITLE_1_OPTUNA = "gridded_optimimum_parameters_"

		# Buscar el atributo OBJECT en el header
		if 'OBJECT' in fits_header:
			object_name = fits_header['OBJECT']
			print(f"El objeto en el archivo FITS es: {object_name}")
		else:
			object_name = "no_object_name"
			print("El atributo OBJECT no se encuentra en el header.")

		# Generar nombres de archivos
		TITLE_OPTUNA_RESULT = self.generate_filename(TITLE_1_OPTUNA,
													self.poly_limits, 
													self.division_limits, 
													self.pixel_size,
													self.image_size, 
													object_name, 
													"txt")

		# Guardar el tiempo de ejecución en un archivo de texto
		with open(TITLE_OPTUNA_RESULT , "w") as file:
			file.write(f"Mejores parametros: {study.best_params}\n\n Mejor valor (BRISQUE): {study.best_value}")

		