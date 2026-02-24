# Smart Drone — Proyecto de Inteligencia Artificial (2025-1)

Implementación de algoritmos de búsqueda aplicados a planificación de rutas para drones, desarrollada como solución al Proyecto 1 del curso de Inteligencia Artificial.

Repositorio alojado en :contentReference[oaicite:0]{index=0}.

El objetivo principal es comparar **técnicas de búsqueda informadas y no informadas** para encontrar caminos eficientes dentro de mapas con obstáculos, incluyendo visualización del proceso de exploración.

---

## 🎯 Objetivos del proyecto

- Modelar el problema de navegación de un drone como espacio de estados
- Implementar algoritmos clásicos de búsqueda
- Comparar eficiencia y calidad de soluciones
- Visualizar el comportamiento de cada algoritmo
- Comprender heurísticas y costos acumulados

---

## 🧠 Algoritmos implementados

### 🔹 Búsqueda no informada
- BFS (Breadth-First Search)
- DFS (Depth-First Search)
- Uniform Cost Search (UCS)

Exploran el espacio sin conocimiento adicional del objetivo.

### 🔹 Búsqueda informada
- Greedy Search
- A* Search

Utilizan funciones heurísticas para guiar la exploración y mejorar el rendimiento.

---

## 🏗️ Estructura del proyecto

```text
smart-drone/
│
├── BúsquedaInformada/        # Algoritmos heurísticos (A*, Greedy)
├── BúsquedaNoInformada/      # BFS, DFS, UCS
├── maps/                    # Mapas de prueba
├── assets/                  # Recursos gráficos
├── Nodo.py                  # Modelo de nodo/estado
├── gui.py                   # Interfaz gráfica de visualización
├── main.py                  # Punto de entrada
└── README.md
```

---

## ⚙️ Tecnologías

- Python 3
- Algoritmos de búsqueda clásicos de IA
- Interfaz gráfica (Tkinter o similar)
- Programación orientada a objetos

---

## ▶️ Cómo ejecutar

### 1. Clonar repositorio
```bash
git clone https://github.com/Jfonsecai/smart-drone.git
cd smart-drone
```

### 2. Ejecutar
```bash
python main.py
```

---

## 🖥️ Qué hace el programa

- Carga un mapa con obstáculos
- Ejecuta un algoritmo de búsqueda
- Expande nodos paso a paso
- Visualiza el recorrido
- Muestra la ruta encontrada y el costo

Permite comparar visualmente eficiencia y comportamiento entre estrategias.

---

## 📚 Aprendizajes clave

Este proyecto refuerza conceptos fundamentales de IA:

- Representación de estados
- Grafos y árboles de búsqueda
- Heurísticas
- Complejidad temporal y espacial
- Diferencias entre búsqueda óptima y rápida
- Visualización de algoritmos

---

## 🎓 Contexto académico

Desarrollado como trabajo práctico para el curso:

**Inteligencia Artificial — Semestre 2025-1**

Enfocado en aplicar teoría de búsqueda a un problema práctico de navegación autónoma.

---

## 👨‍💻 Autores

- Juan Fonseca  
- Michael Ramirez Suriel  
- Jose Adrian Marin  
- David Pinto  

---

## 📄 Licencia

Uso académico y educativo.
