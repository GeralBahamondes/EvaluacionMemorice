# EvaluacionMemorice
Milhar Leiva, Rodrigo Garces, Julian Pino, Geral Bahamondes


# Agente Memorice

Proyecto de Inteligencia Artificial para el juego **Memorice** (tablero de 6x6 con 18 parejas de cartas).

El objetivo es que el agente memorice las cartas vistas y empareje todas las parejas en el menor número de movimientos posibles, mostrando además el tiempo total de resolución.



##  Requisitos cumplidos

- **Memorización:** el agente recuerda las cartas que se han volteado.  
- **Algoritmo de búsqueda:** se implementa un algoritmo de búsqueda (informada) para decidir los movimientos.  
- **Tiempo de resolución:** al finalizar el juego, se muestra el tiempo total de ejecución.  
- **Repositorio en GitHub:** incluye código documentado y este `README.md` con la explicación y ejecución. 

## Ejecución

Requisitos:  
- Python 3.8 o superior  

##Ejecutar en la terminal:  

bash
python agenteMemorice.py
El programa mostrará:

Número de movimientos realizados (cada movimiento = voltear 2 cartas).

Tiempo total de resolución del tablero.

##Algoritmo implementado
  El agente utiliza un enfoque informado basado en memoria:

  Cada vez que voltea una carta, almacena en memoria su valor y posición.

  Si encuentra una carta cuyo par ya estaba en memoria, las empareja inmediatamente.

  Si no conoce la pareja, voltea una nueva carta para seguir recolectando información.

  Repite hasta emparejar todas las cartas del tablero.

  Este comportamiento se considera búsqueda informada, porque el agente utiliza la información acumulada para reducir la cantidad de movimientos necesarios.

##Pruebas
  El agente fue probado en múltiples ejecuciones con tableros aleatorios.
  En cada corrida se registró


