#
#
# Jogo da Velha utilizando Visao Computacional e Realidade aumentada.
#
#


import numpy as np
import cv2
import play
from random import randint
from time import sleep, time


# Marca o inicio do programa. Utilizado para o temporizador.
inicial = time()


# Captura pelo a webcam
cap = cv2.VideoCapture(0)
tamanho = (500, 500) # tamanho da imagem de output
pts2 = np.float32([[0,0], [tamanho[1], 0], [0, tamanho[0]], [tamanho[1], tamanho[0]]])


# Tabuleiros vazios. -1 representa um espaco vazio.
tabuleiro = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
tabuleiro2 = [False, False, False, False, False, False, False, False, False]
escolhas = []



# Loop de captura da webcam, o loop termina com o fim do jogo.
while(cap.isOpened() and play.won(tabuleiro) == 0):
	ret, img = cap.read()

	if ret==True:
		imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)	# tranforma a imagem para niveis de cinza.
		ret2,thresh = cv2.threshold(imgray,170,255,0)	# faz o threshold da imagem em niveis de cinza.
		image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)	# Procura o contornos


		for i in range(len(contours)):
			area = cv2.contourArea(contours[i]) # Area de contorno
			aprox = cv2.approxPolyDP(contours[i], 0.02 * cv2.arcLength(contours[i], True), True)

			# Verifica se e um rentangulo
			if area > 10000 and len(aprox) == 4:
				aprox = play.ordena(aprox, img.shape[:2])
				pts1 = np.float32([\
					[aprox[0][0][0], aprox[0][0][1]],\
					[aprox[1][0][0], aprox[1][0][1]],\
					[aprox[2][0][0], aprox[2][0][1]],\
					[aprox[3][0][0], aprox[3][0][1]] ])
				M = cv2.getPerspectiveTransform(pts1,pts2)	# Transformacao de perspectiva

				dst = cv2.warpPerspective(img, M, (tamanho[1], tamanho[0]))
				template = cv2.imread('x.png', 0)	# le o a imagem usada como template para o match.
				# redimensiona o modelo para 25% do tamanho da imagem do tabuleiro.
				template = cv2.resize(template, dsize=(img.shape[0] // 4, img.shape[1] // 4))
				w, h = template.shape[::-1]
				im_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
				res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)
				threshold = 0.4 	# limiar
				loc = np.where(res >= threshold)

				# Temporizador
				# Caso o jogador humano não inicie a jogada em 10 segundos o computador iniciara.
				if int(time() - inicial) == 10 and 1 not in tabuleiro:
					aux = randint(0, 8)
					escolhas.append(aux)
					inicial = 0

				for pt in zip(*loc[::-1]):
					# desenha um retangulo vermelha nas regioes que dao match com o template.
					cv2.rectangle(dst, (pt[0]+20,pt[1]+20), (pt[0] + w-20, pt[1] + h-20), (0, 0, 255), 0)

					#
					#	Dependendo da regiao identificada marca-se na sua respectiva posicao na matriz que representa o tabuleiro.
					#
					if img.shape[0]//6 - 50 < pt[0] +w/2 < img.shape[0]//6 + 50 and img.shape[1]//8 - 50 < pt[1]+h/2 < img.shape[1]//8 + 50 and tabuleiro2[0] == False:
						play.move(tabuleiro, 0, 1)
						tabuleiro2[0] = True
						if play.won(tabuleiro) == 0:
							aux = randint(0,8)
							while(tabuleiro2[aux] != False):
								aux = randint(0, 8)
							escolhas.append(aux)
					elif img.shape[0]//6 -50 < pt[0]+w/2 < img.shape[0]//6 + 50 and 3*img.shape[1]//8 - 50 < pt[1]+h/2< 3*img.shape[1]//8 +50 and tabuleiro2[3] == False:
						play.move(tabuleiro, 3, 1)
						tabuleiro2[3] = True
						if play.won(tabuleiro) == 0:
							aux = randint(0,8)
							while(tabuleiro2[aux] != False):
								aux = randint(0, 8)
							escolhas.append(aux)
					elif img.shape[0]//6 - 50 < pt[0] +w/2< img.shape[0]//6 + 50 and 5*img.shape[1]//8 - 50 < pt[1]+h/2< 5*img.shape[1]//8 +50 and tabuleiro2[6] == False:
						play.move(tabuleiro, 6, 1)
						tabuleiro2[6] = True
						if play.won(tabuleiro) == 0:
							aux = randint(0,8)
							while(tabuleiro2[aux] != False):
								aux = randint(0, 8)
							escolhas.append(aux)
					elif 3*img.shape[0]//6 - 50 < pt[0] +w/2< 3*img.shape[0]//6 + 50 and img.shape[1]//8 - 50< pt[1] +h/2<img.shape[1]//8 +50 and tabuleiro2[1] == False:
						play.move(tabuleiro, 1, 1)
						tabuleiro2[1] = True
						if play.won(tabuleiro) == 0:
							aux = randint(0,8)
							while(tabuleiro2[aux] != False):
								aux = randint(0, 8)
							escolhas.append(aux)
					elif 3*img.shape[0]//6 - 50 < pt[0] +w/2< 3 * img.shape[0]// 6 +50 and 3*img.shape[1]//8 - 50 < pt[1] +h/2< 3* img.shape[1]//8 +50 and tabuleiro2[4] == False:
						play.move(tabuleiro, 4, 1)
						tabuleiro2[4] = True
						if play.won(tabuleiro) == 0:
							aux = randint(0,8)
							while(tabuleiro2[aux] != False):
								aux = randint(0, 8)
							escolhas.append(aux)
					elif 3*img.shape[0]//6 - 50 < pt[0] +w/2<3*img.shape[0]//6  +50 and 5*img.shape[1]// 8 - 50 < pt[1] +h/2< 5*img.shape[1]//8 +50 and tabuleiro2[7] == False:
						play.move(tabuleiro, 7, 1)
						tabuleiro2[7] = True
						if play.won(tabuleiro) == 0:
							aux = randint(0,8)
							while(tabuleiro2[aux] != False):
								aux = randint(0, 8)
							escolhas.append(aux)
					elif 5*img.shape[0]//6 - 50 < pt[0] +w/2< 5*img.shape[0]//6 +50 and img.shape[1]//8 - 50 < pt[1] +h/2< img.shape[1]//8 +50 and tabuleiro2[2] == False:
						play.move(tabuleiro, 2, 1)
						tabuleiro2[2] = True
						if play.won(tabuleiro) == 0:
							aux = randint(0,8)
							while(tabuleiro2[aux] != False):
								aux = randint(0, 8)
							escolhas.append(aux)
					elif 5*img.shape[0]//6 - 50 < pt[0] +w/2< 5*img.shape[0]//6 +50 and 3*img.shape[1]//8 - 50 < pt[1] +h/2< 3*img.shape[1]//8 + 50 and tabuleiro2[5] == False:
						play.move(tabuleiro, 5, 1)
						tabuleiro2[5] = True
						if play.won(tabuleiro) == 0:
							aux = randint(0,8)
							while(tabuleiro2[aux] != False):
								aux = randint(0, 8)
							escolhas.append(aux)
					elif 5*img.shape[0]//6 - 50 < pt[0] +w/2< 5*img.shape[0]//6 +50 and 5* img.shape[1]//8 - 50 < pt[1] +h/2< 5*img.shape[1]//8 +50 and tabuleiro2[8] == False:
						play.move(tabuleiro, 8, 1)
						tabuleiro2[8] = True
						if play.won(tabuleiro) == 0:
							aux = randint(0,8)
							while(tabuleiro2[aux] != False):
								aux = randint(0, 8)
							escolhas.append(aux)



				#
				# Para cada escolha do computador e desenhado circulo nas suas repectivas regioes a cada frame.
				#
				for escolha in escolhas:
					if escolha == 0:
						cv2.circle(dst, (img.shape[0] // 6, img.shape[1] // 8), 50, (255, 0, 0), 4)
						play.move(tabuleiro, escolha, 0)
						tabuleiro2[0] = True
					elif escolha == 3:
						cv2.circle(dst, (img.shape[0] // 6, 3 * img.shape[1] // 8), 50, (255, 0, 0), 4)
						play.move(tabuleiro, escolha, 0)
						tabuleiro2[3] = True
					elif escolha == 6:
						cv2.circle(dst, (img.shape[0] // 6, 5 * img.shape[1] // 8), 50, (255, 0, 0), 4)
						play.move(tabuleiro, escolha, 0)
						tabuleiro2[6] = True
					elif escolha == 1:
						cv2.circle(dst, (3 * img.shape[0] // 6, img.shape[1] // 8), 50, (255, 0, 0), 4)
						play.move(tabuleiro, escolha, 0)
						tabuleiro2[1] = True
					elif escolha == 4:
						cv2.circle(dst, (3 * img.shape[0] // 6, 3 * img.shape[1] // 8), 50, (255, 0, 0), 4)
						play.move(tabuleiro, escolha, 0)
						tabuleiro2[4] = True
					elif escolha == 7:
						cv2.circle(dst, (3 * img.shape[0] // 6, 5 * img.shape[1] // 8), 50, (255, 0, 0), 4)
						play.move(tabuleiro, escolha, 0)
						tabuleiro2[7] = True
					elif escolha == 2:
						cv2.circle(dst, (5 * img.shape[0] // 6, img.shape[1] // 8), 50, (255, 0, 0), 4)
						play.move(tabuleiro, escolha, 0)
						tabuleiro2[2] = True
					elif escolha == 5:
						cv2.circle(dst, (5 * img.shape[0] // 6, 3 * img.shape[1] // 8), 50, (255, 0, 0), 4)
						play.move(tabuleiro, escolha, 0)
						tabuleiro2[5] = True
					elif escolha == 8:
						cv2.circle(dst, (5 * img.shape[0] // 6, 5 * img.shape[1] // 8), 50, (255, 0, 0), 4)
						play.move(tabuleiro, escolha, 0)
						tabuleiro2[8] = True

				# Escrita do resultado sobre a imagem do tabuleiro.
				fonte = cv2.FONT_HERSHEY_SIMPLEX
				if play.won(tabuleiro) == 1:
					cv2.putText(dst, 'Voce perdeu!!!', (125, 250), fonte, 1, (0, 0, 0), 2, cv2.LINE_AA)
				elif play.won(tabuleiro) == 2:
					cv2.putText(dst, 'Voce ganhou!!!', (125, 250), fonte, 1, (0, 0, 0), 2, cv2.LINE_AA)
				elif play.won(tabuleiro) == 3:
					cv2.putText(dst, 'Deu Velha!!!', (125, 250), fonte, 1, (0, 0, 0), 2, cv2.LINE_AA)
				cv2.imshow("output", dst)


		cv2.imshow("th",thresh)
		cv2.imshow('frame', img)
	if cv2.waitKey(1) == 32:
		break

# Com o fim do jogo espera-se 3 segundos para fechar a janela.
sleep(3)
cv2.imshow('frame', img)
