import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np

# Configurações
LEFT_EYE_THRESHOLD = 0.004   # Ajuste conforme necessário
RIGHT_EYE_THRESHOLD = 0.004  # Ajuste conforme necessário
SMOOTHING_FACTOR = 0.5       # Valores entre 0-1, menor = mais suave

# Inicializa o MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,             # Limite para 1 rosto para economia de recursos
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Inicializa a webcam
cam = cv2.VideoCapture(0)

# Obtém dimensões da tela
screen_w, screen_h = pyautogui.size()

# Variáveis para suavização
prev_x, prev_y = 0, 0
last_left_click_time = 0
last_right_click_time = 0

try:
    while True:
        # Mede o tempo para calcular FPS
        start_time = time.time()
        
        # Captura frame da webcam
        success, frame = cam.read()
        if not success:
            print("Falha ao capturar frame da webcam")
            continue
            
        # Inverte horizontalmente (espelho)
        frame = cv2.flip(frame, 1)
        
        # Converte para RGB sem criar cópia desnecessária
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Para melhorar o desempenho, defina a imagem como não gravável
        rgb_frame.flags.writeable = False
        output = face_mesh.process(rgb_frame)
        rgb_frame.flags.writeable = True
        
        frame_h, frame_w, _ = frame.shape
        
        # Verifica se detectou algum rosto
        if output.multi_face_landmarks:
            landmarks = output.multi_face_landmarks[0].landmark
            
            # Ponta do nariz (landmark 4)
            nose_tip = landmarks[4]
            
            # Converte coordenadas para pixels
            x = int(nose_tip.x * frame_w)
            y = int(nose_tip.y * frame_h)
            
            # Aplica suavização para movimento mais natural
            screen_x = screen_w * nose_tip.x
            screen_y = screen_h * nose_tip.y
            
            smoothed_x = prev_x + (screen_x - prev_x) * SMOOTHING_FACTOR
            smoothed_y = prev_y + (screen_y - prev_y) * SMOOTHING_FACTOR
            
            # Atualiza posições anteriores
            prev_x, prev_y = smoothed_x, smoothed_y
            
            # Move o mouse com posição suavizada
            pyautogui.moveTo(smoothed_x, smoothed_y)
            
            # Desenha na visualização
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            
            # Landmarks para o olho esquerdo
            left_eye_top = landmarks[159]
            left_eye_bottom = landmarks[145]
            
            # Landmarks para o olho direito
            right_eye_top = landmarks[386]     # Parte superior do olho direito
            right_eye_bottom = landmarks[374]  # Parte inferior do olho direito
            
            # Visualização dos pontos do olho esquerdo
            left_top_x, left_top_y = int(left_eye_top.x * frame_w), int(left_eye_top.y * frame_h)
            left_bottom_x, left_bottom_y = int(left_eye_bottom.x * frame_w), int(left_eye_bottom.y * frame_h)
            
            # Visualização dos pontos do olho direito
            right_top_x, right_top_y = int(right_eye_top.x * frame_w), int(right_eye_top.y * frame_h)
            right_bottom_x, right_bottom_y = int(right_eye_bottom.x * frame_w), int(right_eye_bottom.y * frame_h)
            
            # Desenha círculos nos pontos dos olhos
            cv2.circle(frame, (left_top_x, left_top_y), 3, (0, 255, 255), -1)
            cv2.circle(frame, (left_bottom_x, left_bottom_y), 3, (0, 255, 255), -1)
            cv2.circle(frame, (right_top_x, right_top_y), 3, (255, 0, 255), -1)
            cv2.circle(frame, (right_bottom_x, right_bottom_y), 3, (255, 0, 255), -1)
            
            # Calcula distância vertical dos olhos
            left_eye_distance = abs(left_eye_top.y - left_eye_bottom.y)
            right_eye_distance = abs(right_eye_top.y - right_eye_bottom.y)
            
            current_time = time.time()
            
            # Lógica de clique esquerdo
            if left_eye_distance < LEFT_EYE_THRESHOLD and (current_time - last_left_click_time) > 1.0:
                pyautogui.click(button='left')
                last_left_click_time = current_time
                # Feedback visual para o clique esquerdo
                cv2.putText(frame, "Left Click!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Lógica de clique direito
            if right_eye_distance < RIGHT_EYE_THRESHOLD and (current_time - last_right_click_time) > 1.0:
                pyautogui.click(button='right')
                last_right_click_time = current_time
                # Feedback visual para o clique direito
                cv2.putText(frame, "Right Click!", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        # Calcula e mostra FPS
        fps = 1.0 / (time.time() - start_time)
        cv2.putText(frame, f"FPS: {fps:.1f}", (frame_w - 120, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Mostra o frame
        cv2.imshow('Nose Controlled Mouse', frame)
        
        # Verifica tecla ESC para sair
        if cv2.waitKey(1) == 27:  # ESC
            break

except Exception as e:
    print(f"Erro: {e}")

finally:
    # Libera recursos
    cam.release()
    cv2.destroyAllWindows()
    face_mesh.close()