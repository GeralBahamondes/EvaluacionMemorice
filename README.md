# Juego de Memoria - Comparación de Algoritmos de Búsqueda

# Integrantes :
Milhar Leiva
Geral Bahamondes
Rodrigo Garcés
Julian Pino

## Descripción del Proyecto

Este proyecto implementa y compara dos algoritmos diferentes para resolver un juego de memoria (6x6 cartas, 18 pares únicos):

1. **Algoritmo Voraz (Greedy)** - Búsqueda informada con memoria local
2. **Algoritmo A*** - Búsqueda informada con función heurística global

El objetivo es analizar el rendimiento, eficiencia y optimalidad de ambos enfoques en la resolución automática del juego de memoria.

---

## Algoritmos Implementados

**Ambos algoritmos son búsquedas informadas, pero difieren en el tipo y alcance de la información utilizada:**

- **Voraz:** Usa información **local** (memoria de cartas vistas) para decisiones greedy inmediatas
- **A*:** Usa información **global** (memoria + heurística) para decisiones óptimas sistemáticas

### 1. Algoritmo Voraz (Original)

**Tipo:** Búsqueda informada - Estrategia Greedy con memoria local

**Funcionamiento:**
- Utiliza **memoria local** para recordar todas las cartas vistas anteriormente
- **Información disponible:** Mantiene un registro completo de posiciones y valores descubiertos
- **Estrategia de emparejamiento:** Si conoce una pareja en memoria, la empareja inmediatamente
- **Estrategia de exploración:** Explora 2 cartas nuevas por turno, agregando información a su memoria
- **Toma de decisiones informada:** Cada decisión se basa en el conocimiento acumulado
- **Sin backtracking:** Una vez tomada una decisión, no retrocede (característica greedy)

**Información Utilizada:**
- **Memoria de cartas:** Registro completo de todas las cartas vistas
- **Parejas identificadas:** Conocimiento de qué cartas pueden emparejarse
- **Posiciones conocidas:** Ubicación exacta de cada carta descubierta
- **Estado de emparejamiento:** Qué parejas ya fueron resueltas

**Ventajas:**
- Extremadamente rápido (milisegundos)
- Uso eficiente de memoria local
- Implementación directa y clara
- Complejidad lineal
- **Utiliza información:** Toma decisiones basadas en conocimiento previo

**Desventajas:**
- No garantiza solución globalmente óptima
- No considera múltiples estrategias simultáneamente
- **Información limitada:** Solo usa memoria local, no evaluación global
- Resultado puede depender del orden de exploración inicial

### 2. Algoritmo A*

**Tipo:** Búsqueda informada con heurística global y exploración sistemática

**Funcionamiento:**
- Utiliza función de evaluación global para comparar múltiples estrategias
- **Información disponible:** Memoria local + evaluación heurística de estados futuros
- **g(n):** Costo real desde el estado inicial (número de movimientos)
- **h(n):** Heurística admisible que estima movimientos restantes
- **f(n) = g(n) + h(n):** Función de evaluación total
- **Estrategia:** Explora estados más prometedores primero según f(n)
- **Backtracking:** Puede retroceder si encuentra mejor camino
- **Exploración sistemática:** Considera múltiples secuencias de acciones

**Información Utilizada:**
-  **Memoria de cartas:** Igual que el voraz, registro de cartas vistas
-  **Evaluación heurística:** Estimación del costo futuro para cada estado
-  **Múltiples caminos:** Comparación entre diferentes secuencias de acciones
-  **Estados globales:** Evaluación completa del espacio de búsqueda
-  **Optimalidad:** Garantía de encontrar la mejor solución

**Función Heurística:**
La heurística estima el número mínimo de movimientos restantes basándose en parejas conocidas más parejas desconocidas más una estimación de descubrimiento. Considera las cartas que ya están en memoria y pueden emparejarse inmediatamente, estima las parejas restantes que aún no han sido descubiertas, y calcula los movimientos necesarios para revelar cartas nuevas.

- **Parejas conocidas:** Cartas en memoria que pueden emparejarse inmediatamente
- **Parejas desconocidas:** Estimación de parejas restantes por descubrir
- **Estimación de descubrimiento:** Movimientos necesarios para revelar cartas

**Características de la Heurística:**
-  **Admisible:** Nunca sobreestima el costo real
-  **Consistente:** Cumple la desigualdad triangular
-  **Informativa:** Proporciona buena guía para la búsqueda

**Ventajas:**
-  Garantiza solución óptima (con heurística admisible)
-  **Información completa:** Usa memoria + evaluación heurística global
-  Búsqueda sistemática y completa
-  Mejor calidad de solución
-  Considera múltiples estrategias simultáneamente

**Desventajas:**
-  Significativamente más lento
-  Mayor consumo de memoria para estados múltiples
-  Complejidad exponencial en el peor caso
-  Implementación más compleja

---

## Métodos de Prueba

### 1. Tablero de Prueba Estándar
Se utiliza un tablero fijo de 36 posiciones con 18 pares únicos distribuidos de manera específica para garantizar consistencia en las pruebas y permitir comparaciones reproducibles entre ambos algoritmos.

### 2. Métricas Evaluadas

| Métrica | Descripción | Unidad |
|---------|-------------|---------|
| **Movimientos** | Número total de turnos para completar | Entero |
| **Tiempo** | Duración de ejecución | Segundos |
| **Memoria** | Cartas almacenadas en memoria | Entero |
| **Nodos explorados** | Estados evaluados (solo A*) | Entero |
| **Nodos expandidos** | Estados desarrollados (solo A*) | Entero |

### 3. Casos de Prueba

#### Caso 1: Rendimiento Básico
- **Objetivo:** Comparar eficiencia en tablero estándar
- **Métricas:** Tiempo, movimientos, memoria

#### Caso 2: Calidad de Solución  
- **Objetivo:** Evaluar optimalidad de las soluciones
- **Métricas:** Movimientos totales, eficiencia

#### Caso 3: Escalabilidad
- **Objetivo:** Analizar comportamiento con diferentes complejidades
- **Métricas:** Tiempo vs tamaño del problema

### 4. Análisis Comparativo
- **Trade-off velocidad vs optimalidad**
- **Factor de mejora en movimientos**
- **Costo computacional relativo**
- **Recomendaciones de uso**


### Componentes Principales

#### 1. AgenteMemorice (Algoritmo Voraz)
Esta clase implementa el algoritmo voraz original que toma decisiones inmediatas sin planificación futura. Incluye métodos para buscar parejas conocidas en la memoria, resolver el juego paso a paso explorando cartas y emparejando cuando es posible, y mostrar estadísticas del resultado final.

#### 2. EstadoJuego (Representación de Estado)
Clase que representa un estado específico del juego de memoria, manteniendo información sobre qué cartas están en memoria, cuáles ya fueron emparejadas y cuántos movimientos se han realizado. Incluye funciones para verificar si el juego está completo, crear copias del estado, y métodos de comparación necesarios para A*.

#### 3. AgentememoriceAstar (Algoritmo A*)
Implementa el algoritmo A* con búsqueda informada. Incluye la función heurística que estima movimientos restantes, generación de estados sucesores, búsqueda de parejas disponibles, y el algoritmo principal A* que usa una cola de prioridad para explorar los estados más prometedores primero.

#### 4. ComparadorAlgoritmos (Sistema de Análisis)
Sistema que ejecuta ambos algoritmos de forma separada y organizada, muestra los resultados de cada uno por separado con pausas interactivas, genera una comparación final detallada, y proporciona recomendaciones basadas en el análisis de trade-offs entre velocidad y optimalidad.

---

## Cómo Ejecutar el Código

### Prerrequisitos
- **Python 3.7+**
- Bibliotecas estándar: `time`, `heapq`, `copy`

### Instalación
```bash
# Clonar o descargar el archivo
git clone <repository-url>
cd memorice-algorithms

# O simplemente descargar agenteMemorice.py
```

### Ejecución Básica
Ejecutar el programa principal desde la línea de comandos usando Python. El programa automáticamente iniciará la comparación entre ambos algoritmos, mostrando primero los resultados del algoritmo voraz, luego los de A*, y finalmente una comparación detallada.

### Ejecución Personalizada

#### 1. Usar Tablero Personalizado
Es posible crear tableros personalizados modificando la lista de valores en el programa principal. El tablero debe contener exactamente 36 elementos representando 18 pares únicos para mantener la estructura del juego 6x6.

#### 2. Ejecutar Solo Un Algoritmo
Se pueden ejecutar los algoritmos de forma independiente creando instancias específicas de las clases correspondientes y llamando a sus métodos de resolución, lo que es útil para análisis enfocados en un solo enfoque.

#### 3. Acceder a Resultados Programáticamente
Los resultados de la comparación se devuelven en una estructura que permite acceso programático a todas las métricas calculadas, incluyendo movimientos, tiempo, memoria utilizada y nodos explorados para análisis posterior.

---

## Interpretación de Resultados

### Ejemplo de Salida
El programa muestra primero la ejecución del algoritmo voraz con mensajes detallados sobre cada acción tomada, incluyendo exploración de posiciones y emparejamiento de cartas. Luego ejecuta A* con salida similar pero mostrando la búsqueda más sistemática. Finalmente presenta una comparación completa con métricas detalladas, análisis de trade-offs y recomendaciones.

### Análisis de Resultados

#### Factores de Éxito:
- **Movimientos:** Menor es mejor (eficiencia)
- **Tiempo:** Menor es mejor (velocidad)
- **Nodos explorados:** Indicador de complejidad computacional

#### Interpretación:
- **Voraz gana en velocidad:** Típicamente 100-1000x más rápido
- **A* gana en calidad:** Generalmente 10-20% menos movimientos
- **Trade-off:** Velocidad vs Optimalidad

---

## Configuración y Personalización

### Ajustar Heurística de A*
La función heurística puede modificarse para experimentar con diferentes estimaciones de costo. Se pueden implementar heurísticas más o menos optimistas, agregar factores de peso diferentes, o considerar patrones específicos del tablero.

### Cambiar Estrategia de Exploración
Los algoritmos permiten ajustar la estrategia de exploración modificando cuántas cartas se exploran por turno, el orden de exploración, o los límites de ramificación para controlar la complejidad computacional.

### Personalizar Salida
El nivel de detalle en la salida puede ajustarse modificando los mensajes mostrados durante la ejecución, desde salida mínima hasta trazas detalladas de cada decisión tomada por los algoritmos.

---

## Referencias y Fundamentos Teóricos

### Algoritmo A*
- Russell, S. & Norvig, P. "Artificial Intelligence: A Modern Approach"
- Fundamentos de heurísticas admisibles y consistentes
- Complejidad temporal: O(b^d) donde b=factor de ramificación, d=profundidad

### Algoritmos Greedy
- Cormen, T. et al. "Introduction to Algorithms"  
- Estrategias de optimización local
- Complejidad temporal: O(n) típicamente lineal

### Juegos de Memoria
- Análisis de estrategias óptimas en juegos de información perfecta
- Teoría de juegos y búsqueda en espacios de estados

---

## Limitaciones y Consideraciones

### Limitaciones del Algoritmo A*
- **Memoria:** Puede agotar memoria en tableros muy grandes
- **Tiempo:** Exponencial en el peor caso
- **Heurística:** La calidad depende de la heurística utilizada

### Limitaciones del Algoritmo Voraz
- **Optimalidad:** No garantiza la mejor solución
- **Determinismo:** Resultado puede variar según implementación
- **Adaptabilidad:** No se adapta a patrones específicos

### Consideraciones de Implementación
- **Detección de ciclos:** A* incluye manejo de estados repetidos
- **Límite de profundidad:** Evitar búsquedas infinitas
- **Eficiencia de memoria:** Gestión cuidadosa de estados almacenados

---

## Contribuciones y Extensiones

### Posibles Mejoras
1. **Heurísticas adicionales:** Implementar diferentes funciones h(n)
2. **Algoritmos alternativos:** BFS, DFS, Hill Climbing
3. **Optimizaciones:** Poda alfa-beta, memoización
4. **Análisis estadístico:** Múltiples ejecuciones, promedios
5. **Visualización:** Interfaz gráfica del proceso de búsqueda

### Casos de Uso Extendidos
- **Tableros variables:** 4x4, 8x8, tamaños personalizados
- **Dificultad adaptativa:** Diferentes distribuciones de cartas
- **Métricas adicionales:** Análisis de patrones, predicción

---

## Soporte y Contacto

Para preguntas, sugerencias o reportar bugs:
- Revisar el código fuente comentado
- Analizar la salida detallada de los algoritmos
- Experimentar con diferentes tableros y configuraciones

---


