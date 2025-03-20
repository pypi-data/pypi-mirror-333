from polynomial_preprocessing import preprocesamiento_datos_a_grillar
from astropy.io import fits
import cupy as cp
import numpy as np
import time
import matplotlib.pyplot as plt
from numba import jit, prange

class ProcesamientoDatosGrillados:
	def __init__(self, fits_path, ms_path, num_polynomial, division_sigma, pixel_size=None, image_size=None, verbose = True, plots = False):
		self.fits_path = fits_path
		self.ms_path = ms_path
		self.num_polynomial = num_polynomial
		self.division_sigma = division_sigma
		self.pixel_size = pixel_size
		self.image_size = image_size
		self.verbose = verbose
		self.plots = plots

		if self.pixel_size is None:
			pixel_size = preprocesamiento_datos_a_grillar.PreprocesamientoDatosAGrillar(fits_path=self.fits_path,
																						ms_path=self.ms_path)
			_, _, _, _, pixels_size = pixel_size.fits_header_info()
			print("Pixel size of FITS: ", pixels_size)
			self.pixel_size = pixels_size



		if self.image_size is None:
			fits_header = preprocesamiento_datos_a_grillar.PreprocesamientoDatosAGrillar(fits_path=self.fits_path,
																						 ms_path=self.ms_path)

			_, fits_dimensions, _, _, _ = fits_header.fits_header_info()
			print("Image size of FITS: ", fits_dimensions[1])
			self.image_size = fits_dimensions[1]

	def data_processing(self):
		gridded_visibilities, gridded_weights, pixel_size, grid_u, grid_v = self.grid_data()
		image_model, visibilities_model, weights_model, u_target, v_target = self.gridded_data_processing(gridded_visibilities, gridded_weights, pixel_size, grid_u, grid_v)
		return image_model, visibilities_model, weights_model, u_target, v_target


	def grid_data(self):

		print("self.pixel_size: ", self.pixel_size)
		print("self.image_size: ", self.image_size)

		gridded_visibilities, gridded_weights, pixel_size, grid_u, grid_v = (preprocesamiento_datos_a_grillar.
																		  PreprocesamientoDatosAGrillar(self.fits_path,
																										self.ms_path,																										
																										image_size = self.image_size,
																										pixel_size = self.pixel_size,
																										plots = self.plots
																										).
																		  process_ms_file())
		
		return gridded_visibilities, gridded_weights, pixel_size,  grid_u, grid_v


	def gridded_data_processing(self, gridded_visibilities, gridded_weights, pixel_size, grid_u, grid_v):

		start_time = time.time()

		# Cargamos los archivos de entrada
		fits_header, _, _, du, pixel_size = (preprocesamiento_datos_a_grillar.
																	PreprocesamientoDatosAGrillar(self.fits_path,
																								self.ms_path,																									
																								image_size = self.image_size,
																								pixel_size = self.pixel_size,
																								plots = self.plots
																								).
																	fits_header_info())


		################# Parametros iniciales #############
		M = 1  # Multiplicador de Pixeles
		pixel_num = self.image_size  # Numero de pixeles
		pixel_num = pixel_num * M  # Numero de pixeles,  multiplicador #Version MS
		num_polynomial = self.num_polynomial # Numero de polinomios
		sub_S = int(num_polynomial)
		ini = 1  # Tamano inicial
		division = self.division_sigma # division_sigma
		pixel_size = self.pixel_size

		# Constantes para archivos de salida
		TITLE_1 = "gridded_visibility_model_natural_"
		TITLE_1_DIRTY_IMAGE = "dirty_image_gridded_model_natural_"
		TITLE_1_WEIGHTS = "gridded_weights_model_natural_"
		TITLE_1_TIME = "execution_time_gridded_"

		########################################## Cargar archivo de entrada Version MS
		# Eliminamos la dimension extra
		u_ind, v_ind = np.nonzero(gridded_visibilities[0])
		gridded_visibilities_2d = gridded_visibilities[0].flatten()  # (1,251,251)->(251,251)
		gridded_weights_2d = gridded_weights[0].flatten()  # (1,251,251)->(251,251)

		# Filtramos por los valores no nulos
		nonzero_indices = np.nonzero(gridded_weights_2d)
		gv_sparse = gridded_visibilities_2d[nonzero_indices]
		gw_sparse = gridded_weights_2d[nonzero_indices]

		# Normalizacion de los datos

		gv_sparse = (gv_sparse / np.sqrt(np.sum(gv_sparse ** 2)))
		gw_sparse = (gw_sparse / np.sqrt(np.sum(gw_sparse ** 2)))

		print("gw_sparse.shape: ", gw_sparse.shape)

		u_data = grid_u[u_ind]
		v_data = grid_v[v_ind]

		############################################# Ploteo del Primary beam
		if self.plots == True:
			plt.figure()
			plt.plot(gv_sparse, color='r')
			plt.title("Gridded visibilities distribution")

		du = 1 / (pixel_num * pixel_size)

		umax = pixel_num * du / 2

		u_sparse = np.array(u_data) / umax
		v_sparse = np.array(v_data) / umax

		if self.plots == True:
			plt.figure()
			plt.xlim(-1, 1)
			plt.ylim(-1, 1)
			plt.scatter(u_sparse, v_sparse, s=1)
			plt.title("Gridded uv coverage")

		u_target = np.reshape(np.linspace(-ini, ini, pixel_num), (1, pixel_num)) * np.ones(shape=(pixel_num, 1))
		v_target = np.reshape(np.linspace(-ini, ini, pixel_num), (pixel_num, 1)) * np.ones(shape=(1, pixel_num))

		z_target = u_target + 1j * v_target
		z_sparse = u_sparse + 1j * v_sparse

		print("u_sparse: ", u_sparse.shape)
		print("v_sparse: ", v_sparse.shape)

		print("z_sparse.shape: ", z_sparse.shape)

		b = 1

		z_exp = np.exp(-z_target * np.conjugate(z_target) / (2 * b * b))

		if self.plots == True:
			title = "Z exp"
			fig = plt.figure(title)
			plt.title(title)
			im = plt.imshow(np.abs(z_exp))  # Usar np.abs para evitar el warning
			plt.colorbar(im)
			plt.show()
			
		
		max_memory = 120000000
		max_data = float(int(max_memory / (num_polynomial * num_polynomial)))

		divide_data = int(np.size(gv_sparse[np.absolute(gv_sparse) != 0].flatten()) / max_data) + 1
		divide_target = int(pixel_num * pixel_num / max_data) + 1

		if divide_target > divide_data:
			divide_data = int(divide_target)

		if divide_data > int(divide_data):
			divide_data = int(divide_data) + 1

		chunk_data = int(((num_polynomial * num_polynomial) / divide_data) ** (1 / 2)) + 1
		if chunk_data == 0:
			chunk_data = 1

		# chunk_data = 1
		print(chunk_data)

		visibilities_model = np.zeros((pixel_num, pixel_num), dtype=np.complex128)

		print("Max. polynomial degree:", num_polynomial)
		print("Division:", division)

		visibilities_aux = np.zeros(pixel_num * pixel_num, dtype=np.complex128)
		weights_aux = np.zeros(pixel_num * pixel_num, dtype=float)


		# print(z_target.dtype)
		# print(z_sparse.dtype)
		# print(gw_sparse.dtype)
		# print(gv_sparse.dtype)
		# print(type(chunk_data))

		# Obtencion de los datos de la salida con G-S

		visibilities_mini, err, residual, P_target, P = (self.recurrence2d
														 (z_target.flatten(),
														  z_sparse.flatten(),
														  gw_sparse.flatten(),
														  gv_sparse.flatten(),
														  np.size(z_target.flatten()),
														  num_polynomial,
														  division,
														  chunk_data)
														 )

		print("visibilities_mini.shape: ", visibilities_mini.shape)

		print("residual.shape: ", residual.shape)

		visibilities_mini = np.reshape(visibilities_mini, (pixel_num, pixel_num))

		visibilities_model = np.array(visibilities_mini)

		#residual_mini = np.reshape(residual, (pixel_num, pixel_num))

		#residual_model = np.array(residual_mini)

		if self.plots == True:
			plt.figure()
			plt.plot(visibilities_model.flatten(), color='g')

		
		weights_model = np.zeros((pixel_num, pixel_num), dtype=float)

		sigma_weights = np.divide(1.0, gw_sparse, where=gw_sparse != 0, out=np.zeros_like(gw_sparse))  # 1.0/gw_sparse
		sigma = np.max(sigma_weights) / division
		weights_mini = np.array(1 / err)
		weights_mini[np.isnan(weights_mini)] = 0.0
		weights_mini[np.isinf(weights_mini)] = 0.0

		weights_mini = np.reshape(weights_mini, (pixel_num, pixel_num))

		weights_model = np.array(weights_mini)

		# Finalizar el contador de tiempo
		end_time = time.time()

		# Calcular el tiempo de ejecución
		execution_time = end_time - start_time

		print(f"Tiempo de ejecución: {execution_time:.2f} segundos")

		####################################### GENERACION DE GRAFICOS DE SALIDA #####################################

		image_model = (np.fft.fftshift
					   (np.fft.ifft2
						(np.fft.ifftshift
						 (visibilities_model * weights_model / np.sum(weights_model.flatten())))) * pixel_num ** 2)
		image_model = np.array(image_model.real)

		print("residual.shape: ", residual.shape)

		if self.plots == True:
			title = "Image model (division sigma: " + str(division) + ")"; fig = plt.figure(title); plt.title(title); im = plt.imshow(image_model)
			plt.colorbar(im)

			title = "Visibility model (division sigma: " + str(division) + ")"; fig = plt.figure(title); plt.title(title); im = plt.imshow(np.log(np.absolute(visibilities_model) + 0.00001))
			plt.colorbar(im)

			title = "Weights model (division sigma: " + str(division) + ")"; fig = plt.figure(title); plt.title(title); im = plt.imshow(weights_model)
			plt.colorbar(im)

			#title="Residual model (division sigma: "+str(division)+")"; fig=plt.figure(title); plt.title(title); im=plt.imshow(residual_model)
			#plt.colorbar(im)

			plt.show()

		if self.verbose == True:

			# Buscar el atributo OBJECT en el header
			if 'OBJECT' in fits_header:
				object_name = fits_header['OBJECT']
				print(f"El objeto en el archivo FITS es: {object_name}")
			else:
				object_name = "no_object_name"
				print("El atributo OBJECT no se encuentra en el header.")

			# Generar nombres de archivos
			TITLE_TIME_RESULT = self.generate_filename(TITLE_1_TIME, 
														num_polynomial, 
														division,
														pixel_size, 
														pixel_num, 
														object_name, 
														"txt")

			# Guardar el tiempo de ejecución en un archivo de texto
			with open(TITLE_TIME_RESULT , "w") as file:
				file.write(f"Tiempo de ejecucion: {execution_time:.2f} segundos\n")

			# Generar nombres de archivos
			TITLE_VISIBILITIES_RESULT = self.generate_filename(TITLE_1, 
													  num_polynomial, 
													  division,
													  pixel_size, 
													  pixel_num, 
													  object_name, 
													  "npz")
			
			TITLE_WEIGHTS_RESULT = self.generate_filename(TITLE_1_WEIGHTS, 
												 num_polynomial, 
												 division,
												 pixel_size, 
												 pixel_num, 
												 object_name, 
												 "npz")
			
			TITLE_DIRTY_IMAGE_FITS = self.generate_filename(TITLE_1_DIRTY_IMAGE, 
												   num_polynomial, 
												   division,
												   pixel_size, 
												   pixel_num, 
												   object_name, 
												   "fits")

			# Guardar archivos
			np.savez(TITLE_VISIBILITIES_RESULT, visibilities_model)
			np.savez(TITLE_WEIGHTS_RESULT, weights_model)
			fits.writeto(TITLE_DIRTY_IMAGE_FITS, image_model, fits_header, overwrite=True)

		return image_model, visibilities_model, weights_model, u_target, v_target

	# Función para generar nombres de archivos
	@staticmethod
	def generate_filename(prefix, num_polynomials, division, pixel_size, num_pixels, object_name, extension):
		base_title = f"num_polynomial_{num_polynomials}_division_sigma_{division}_pixel_size_{pixel_size}_image_size_{num_pixels}_{num_pixels}_{object_name}"
		return f"{prefix}{base_title}.{extension}"

	@staticmethod
	def dot2x2_gpu(weights, matrix, pol, chunk_data):
		"""
		Calcula el producto punto ponderado de una matriz y un polinomio en GPU.

		Parámetros:
		- weights: CuPy array de pesos complejos (1D).
		- matrix: CuPy array de polinomios complejos (3D).
		- pol: CuPy array de polinomio de referencia (1D).
		- chunk_data: Tamaño de bloque para procesamiento por partes.

		Retorna:
		- final_dot: Producto punto ponderado (3D CuPy array de forma (N1, N2, 1)).
		"""
		# Dimensiones de la matriz
		N1, N2, n = matrix.shape
		sub_size = (N1 // chunk_data) + 1
		final_dot = cp.zeros((N1, N2, 1), dtype=cp.complex128)

		for chunk1 in range(sub_size):
			for chunk2 in range(sub_size):
				if chunk1 + chunk2 < sub_size:
					# Tamaños de bloque, asegurando límites
					N3 = min(chunk_data, N1 - chunk1 * chunk_data)
					N4 = min(chunk_data, N2 - chunk2 * chunk_data)

					# Operación sobre el bloque de datos
					subsum = cp.zeros((N3, N4, 1), dtype=cp.complex128)

					# Operación de suma ponderada en la GPU para el bloque actual
					sub_matrix = matrix[chunk1 * chunk_data:(chunk1 + 1) * chunk_data,
								 chunk2 * chunk_data:(chunk2 + 1) * chunk_data, :]
					sub_weights = cp.broadcast_to(weights, sub_matrix.shape)
					sub_pol = cp.broadcast_to(cp.conjugate(pol), sub_matrix.shape)

					# Suma ponderada en la última dimensión
					subsum = cp.sum(sub_matrix * sub_weights * sub_pol, axis=2, keepdims=True)

					# Asignar el resultado al bloque en la matriz final
					final_dot[chunk1 * chunk_data:(chunk1 + 1) * chunk_data,
					chunk2 * chunk_data:(chunk2 + 1) * chunk_data, :] = subsum

		return final_dot
	
	@staticmethod
	@jit(parallel=True)
	def initialize_polynomials_cpu(z, z_target, w, s):
		P = np.zeros((s, s, len(z)), dtype=np.complex128)
		P_target = np.zeros((s, s, len(z_target)), dtype=np.complex128)

		for j in prange(s):
			for k in range(s):
				P[k, j, :] = (z ** k) * np.conjugate(z) ** j
				P_target[k, j, :] = (z_target ** k) * np.conjugate(z_target) ** j

				# Normalización
				no = np.sqrt(np.sum(w * np.abs(P[k, j, :]) ** 2))
				if no != 0:
					P[k, j, :] /= no
					P_target[k, j, :] /= no

		return P, P_target
	

	
	"""
		@staticmethod
	def dot2x2_gpu_optimized(weights, matrix, pol, chunk_data):
		N1, N2, n = matrix.shape
		sub_size = max(1, (N1 // chunk_data) + 1)

		# Obtener la memoria total y usada en la GPU
		total_mem = cp.cuda.Device(0).mem_info[1]  # Memoria total de la GPU 0 en bytes
		used_mem = total_mem - cp.cuda.Device(0).mem_info[0]  # Memoria ya utilizada
		available_mem = total_mem - used_mem  # Memoria real disponible
		mem_usage_factor = 0.9  # Usar hasta el 90% de la memoria disponible

		# Ajustar chunk_data usando memoria real disponible
		chunk_data = max(1, min(chunk_data, int(mem_usage_factor * available_mem)))

		# Inicializar matriz de salida en menor precisión para reducir uso de memoria
		final_dot = cp.zeros((N1, N2, 1), dtype=cp.complex64)  # Usar complex64

		# Procesamiento por fragmentos para evitar OOM
		for chunk1 in range(sub_size):
			for chunk2 in range(sub_size):
				if chunk1 + chunk2 < sub_size:
					N3 = min(chunk_data, N1 - chunk1 * chunk_data)
					N4 = min(chunk_data, N2 - chunk2 * chunk_data)

					if N3 <= 0 or N4 <= 0:
						continue

					# Extraer submatrices de forma más eficiente
					sub_matrix = matrix[chunk1 * chunk_data:(chunk1 + 1) * chunk_data,
										chunk2 * chunk_data:(chunk2 + 1) * chunk_data, :]

					# Usar cp.einsum para multiplicación y suma eficiente
					subsum = cp.einsum('ijk,k->ij', sub_matrix * weights, cp.conjugate(pol))
					final_dot[chunk1 * chunk_data:(chunk1 + 1) * chunk_data,
							chunk2 * chunk_data:(chunk2 + 1) * chunk_data, 0] += subsum

					# Liberar memoria intermedia
					del sub_matrix, subsum
					cp.get_default_memory_pool().free_all_blocks()

		# Liberar memoria global al final
		cp.get_default_memory_pool().free_all_blocks()

		return final_dot
	"""
	
	@staticmethod
	@jit(parallel=True)
	def norm2x2(weights, matrix, chunk_data):
		N1, N2, n = matrix.shape
		sub_size = (N1 // chunk_data) + 1
		final_norm = np.zeros((N1, N2, 1), dtype=np.complex128)

		for chunk1 in prange(sub_size):
			for chunk2 in prange(sub_size):
				if chunk1 + chunk2 < sub_size:
					# Extraer el subarray de matrix
					start1 = chunk1 * chunk_data
					end1 = min((chunk1 + 1) * chunk_data, N1)
					start2 = chunk2 * chunk_data
					end2 = min((chunk2 + 1) * chunk_data, N2)
					
					sub_m = matrix[start1:end1, start2:end2, :]
					N3, N4, n2 = sub_m.shape

					# Calcular subsum directamente sin broadcast
					subsum = np.zeros((N3, N4), dtype=np.float64)
					for i in prange(N3):
						for j in prange(N4):
							for k in range(n2):
								subsum[i, j] += weights[k] * np.abs(sub_m[i, j, k])**2
							subsum[i, j] = np.sqrt(subsum[i, j])

					# Asignar el resultado a la matriz final_norm
					final_norm[start1:end1, start2:end2, 0] = subsum

		return final_norm

	def normalize_initial_polynomials_cpu(self, w, P, P_target, V, s, chunk_data):
		no_data = self.norm2x2(w, P, chunk_data)

		# Dividimos por no_data solo en posiciones donde no_data no es cero
		for i in range(P.shape[0]):
			for j in range(P.shape[1]):
				if V[i, j, 0] != 0:  # Solo si el valor en V es distinto de cero
					if no_data[i, j] != 0:  # Evitar división por cero
						P[i, j, :] = P[i, j, :] / no_data[i, j]
						P_target[i, j, :] = P_target[i, j, :] / no_data[i, j]

		return P, P_target

	@staticmethod
	def norm2x2_gpu(weights, matrix, chunk_data):
		"""
		Calcula la norma ponderada de una matriz en GPU.

		Parámetros:
		- weights: CuPy array de pesos complejos (1D).
		- matrix: CuPy array de polinomios complejos (3D).
		- chunk_data: Tamaño de bloque para procesamiento por partes.

		Retorna:
		- final_norm: Norma ponderada (3D CuPy array de forma (N1, N2, 1)).
		"""
		# Dimensiones de la matriz
		N1, N2, n = matrix.shape
		sub_size = (N1 // chunk_data) + 1
		final_norm = cp.zeros((N1, N2, 1), dtype=cp.complex128)

		for chunk1 in range(sub_size):
			for chunk2 in range(sub_size):
				if chunk1 + chunk2 < sub_size:
					# Tamaños de bloque, asegurando límites
					N3 = min(chunk_data, N1 - chunk1 * chunk_data)
					N4 = min(chunk_data, N2 - chunk2 * chunk_data)

					# Submatriz en el bloque actual
					sub_m = matrix[chunk1 * chunk_data:(chunk1 + 1) * chunk_data,
							chunk2 * chunk_data:(chunk2 + 1) * chunk_data, :]

					# Aplicar los pesos sobre la submatriz y calcular la norma ponderada
					sub_weights = cp.broadcast_to(weights, sub_m.shape)
					subsum = sub_weights * cp.abs(sub_m) ** 2
					subsum = cp.sum(subsum, axis=2)
					subsum = cp.sqrt(subsum)
					subsum = subsum.reshape((N3, N4, 1))

					# Asignar el resultado al bloque correspondiente en la matriz final
					final_norm[chunk1 * chunk_data:(chunk1 + 1) * chunk_data,
					chunk2 * chunk_data:(chunk2 + 1) * chunk_data, :] = subsum

		return final_norm

	def normalize_initial_polynomials_gpu(self, w, P, P_target, V, s, chunk_data):
		"""
		Normaliza los polinomios iniciales P y P_target usando CuPy para operaciones en GPU.

		Parámetros:
		- w: CuPy array 1D de pesos complejos.
		- P: CuPy array 3D de polinomios iniciales.
		- P_target: CuPy array 3D de polinomios objetivos.
		- V: CuPy array 3D de enteros para validación.
		- s: Dimensión de los polinomios.
		- chunk_data: Tamaño de los bloques para procesamiento.

		Retorna:
		- P: CuPy array normalizado.
		- P_target: CuPy array normalizado.
		"""
		# Asegurarse de que todos los datos estén en CuPy
		w = cp.asarray(w)
		P = cp.asarray(P)
		P_target = cp.asarray(P_target)

		# Calcular las normas para la normalización
		no_data = self.norm2x2_gpu(w, P, chunk_data)

		# Evitar divisiones por cero asignando 1 a los elementos de no_data que son cero
		no_data[no_data == 0] = 1

		# Normalizar P y P_target
		P = P / no_data
		P_target = P_target / no_data

		# Limpieza de valores NaN e Inf
		P = cp.nan_to_num(P, nan=0.0, posinf=0.0, neginf=0.0)
		P_target = cp.nan_to_num(P_target, nan=0.0, posinf=0.0, neginf=0.0)

		del w

		# Se libera la memoria utilizada por la GPU, para evitar un sobreconsumo de
		# esta (y se restringa el uso de Google Colab).
		mempool = cp.get_default_memory_pool()
		mempool.free_all_blocks()

		return P, P_target

	def gram_schmidt_and_estimation_gpu(self, w, P, P_target, V, D, D_target, residual, final_data, err, s, sigma2,
										max_rep,
										chunk_data):
		"""
		Realiza el proceso de ortogonalización de Gram-Schmidt y estimación usando GPU.

		Parámetros:
		- w: CuPy array 1D de pesos complejos.
		- P: CuPy array 3D de polinomios complejos.
		- P_target: CuPy array 3D de polinomios extrapolados.
		- V: CuPy array 3D de enteros, matriz de validación.
		- D: CuPy array 1D complejo, polinomio de referencia actual.
		- D_target: CuPy array 1D complejo, polinomio extrapolado de referencia.
		- residual: CuPy array 1D complejo, datos residuales.
		- final_data: CuPy array 1D complejo, resultado final.
		- err: CuPy array 1D flotante, errores estimados.
		- s: tamaño de la matriz de polinomios (entero).
		- sigma2: criterio de selección sigma al cuadrado.
		- max_rep: número de repeticiones para la ortogonalización de Gram-Schmidt.
		- chunk_data: tamaño de los bloques de datos.

		Retorna:
		- final_data, residual, err, P_target, P: Arrays finales con los resultados.
		"""
		# Asegurarse de que todas las variables estén en CuPy
		w = cp.asarray(w)
		P = cp.asarray(P)
		P_target = cp.asarray(P_target)
		V = cp.asarray(V)
		D = cp.asarray(D)
		D_target = cp.asarray(D_target)
		residual = cp.asarray(residual)
		final_data = cp.asarray(final_data)
		err = cp.asarray(err)

		for k in range(s):  # Nivel de grado de los polinomios
			for j in range(k + 1):  # Grado de cada polinomio en la contradiagonal
				for repeat in range(max_rep):
					if repeat > 0 or (k == 0 and j == 0):
						# Normalización
						no = cp.sqrt(cp.sum(w * cp.abs(P[k - j, j, :]) ** 2))
						if no != 0:
							P[k - j, j, :] /= no
							P_target[k - j, j, :] /= no

						# Almacenar polinomios iniciales
						if k == 0 and j == 0:
							D = cp.array(P[k - j, j, :])
							D_target = cp.array(P_target[k - j, j, :])
							V[k - j, j, :] = 0

					# Evitar normalización innecesaria si el grado es superior a 1
					if j == 1 and k > 0 and repeat == 0:
						no_data = self.norm2x2_gpu(w, P, chunk_data)
						V_mask = cp.where(V == 0, 1, 0)  # Crear una máscara para V
						no_data *= V_mask  # Aplicar la máscara
						P /= cp.where(no_data != 0, no_data, 1)
						P_target /= cp.where(no_data != 0, no_data, 1)

					# Ortogonalización Gram-Schmidt
					if repeat == 0:
						dot_data = self.dot2x2_gpu_optimized(w, P * V, D, chunk_data)
						P -= dot_data * D
						P_target -= dot_data * D_target

						del dot_data

					# Se libera la memoria utilizada por la GPU, para evitar un sobreconsumo de
					# esta.
					
					cp.get_default_memory_pool().free_all_blocks()
					cp.get_default_pinned_memory_pool().free_all_blocks()

				# Limpieza de valores NaN e Inf
				P = cp.nan_to_num(P, nan=0.0, posinf=0.0, neginf=0.0)
				P_target = cp.nan_to_num(P_target, nan=0.0, posinf=0.0, neginf=0.0)

				# Actualización de V y cálculo de extrapolación
				V[k - j, j, :] = 0
				D = cp.array(P[k - j, j, :])
				D_target = cp.array(P_target[k - j, j, :])
				M = cp.sum(w * residual.flatten() * cp.conjugate(P[k - j, j, :]))
				final_data += M * P_target[k - j, j, :]
				residual -= M * P[k - j, j, :]
				err += cp.abs(P_target[k - j, j, :]) ** 2

		del M
		del V
		del D
		del D_target
		del w

		# Se libera la memoria utilizada por la GPU, para evitar un sobreconsumo de
		# esta (y se restringa el uso de Google Colab).
		mempool = cp.get_default_memory_pool()
		mempool.free_all_blocks()

		final_data[err > sigma2] = 0

		# Convertir las salidas de nuevo a NumPy para evitar errores fuera de esta función
		return cp.asnumpy(final_data), cp.asnumpy(residual), cp.asnumpy(err), cp.asnumpy(P_target), cp.asnumpy(P)
	
	
	@staticmethod
	def dot2x2_gpu_optimized(weights, matrix, pol, chunk_data):
		"""
		Versión optimizada de dot2x2_gpu para reducir el uso de memoria en GPU.
		"""
		N1, N2, n = matrix.shape
		final_dot = cp.zeros((N1, N2, 1), dtype=cp.complex128)

		for chunk1 in range(N1 // chunk_data + 1):
			for chunk2 in range(N2 // chunk_data + 1):
				start1 = chunk1 * chunk_data
				end1 = min((chunk1 + 1) * chunk_data, N1)
				start2 = chunk2 * chunk_data
				end2 = min((chunk2 + 1) * chunk_data, N2)

				sub_matrix = matrix[start1:end1, start2:end2, :]
				subsum = cp.einsum('ijk,k->ij', sub_matrix * weights, cp.conjugate(pol))
				final_dot[start1:end1, start2:end2, 0] += subsum

				# Liberar memoria intermedia
				del sub_matrix, subsum
				cp.get_default_memory_pool().free_all_blocks()

		return final_dot

	def recurrence2d(self, z_target, z, weights, data, size, s, division_sigma, chunk_data):
		z = np.array(z)
		z_target = np.array(z_target)
		w = np.array(weights)
		residual = np.array(data)

		sigma_weights = np.divide(1.0, w, where=w != 0, out=np.zeros_like(w))
		sigma2 = np.max(sigma_weights) / division_sigma
		print("Sigma:", sigma2)

		final_data = np.zeros(shape=(size), dtype=np.complex128)
		# P = np.zeros(shape=(s, s, z.size), dtype=np.complex128)
		# P_target = np.zeros(shape=(s, s, size), dtype=np.complex128)
		V = np.ones(shape=(s, s, 1), dtype=int)
		D = np.zeros(z.size, dtype=np.complex128)
		D_target = np.zeros(size, dtype=np.complex128)
		err = np.zeros(shape=(size), dtype=float)

		# Inicialización de matrices polinómicas P y P_target
		P, P_target = self.initialize_polynomials_cpu(z, z_target, w, s)

		print("Polinomios inicializados.")

		# Normalización inicial de P y P_target
		P, P_target = self.normalize_initial_polynomials_cpu(w, P, P_target, V, s, chunk_data)

		print("Polinomios normalizados.")

		# Procedimiento Gram-Schmidt en los polinomios
		final_data, residual, err, P_target, P = self.gram_schmidt_and_estimation_gpu(w, P, P_target, V, D, D_target,
																					  residual, final_data, err, s,
																					  sigma2,
																					  max_rep=2, chunk_data=chunk_data)
		# final_data, residual, err = gram_schmidt_and_estimation(w, P, P_target, V, D, D_target, residual, final_data, err, s, sigma2, max_rep=2, chunk_data=chunk_data)
		
		print("Hice G-S.")

		del w
		del D
		del D_target
		del z
		del z_target

		# Se libera la memoria utilizada por la GPU, para evitar un sobreconsumo de
		# esta.
		mempool = cp.get_default_memory_pool()
		mempool.free_all_blocks()

		return final_data, err, residual, P_target, P

