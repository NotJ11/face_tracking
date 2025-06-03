# Controle do Mouse por Rastreamento Facial

Este projeto implementa um sistema de controle do mouse utilizando **rastreamento facial em tempo real**, com foco em acessibilidade digital para pessoas com mobilidade reduzida nos membros superiores. O sistema usa o **nariz como ponto de referência para mover o cursor** e **piscadas dos olhos para simular cliques**, tudo com **hardware convencional e bibliotecas de código aberto**.

---

# Tecnologias Utilizadas

- **Python 3**
- **OpenCV** – Processamento de imagens
- **MediaPipe** – Detecção de pontos de referência facial (Face Mesh)
- **PyAutoGUI** – Controle do mouse
- **Interpolação Linear Ponderada** – Suavização do movimento do cursor

---

#  Funcionalidades

-  Rastreamento facial em tempo real com webcam
-  Movimento do cursor controlado pela posição do nariz
-  Clique com o olho esquerdo e direito
-  Algoritmo de suavização de movimento para maior estabilidade
-  Detecção de piscadas com thresholds calibrados
-  Funciona com webcam padrão e sem hardware especializado
