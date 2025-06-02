

╔════════════════════════════════════════════════════════╗
║////////////////////////////////////////////////////////║
║#######     ALUMNO: Ortiz García Pablo Adrián    #######║
║////////////////////////////////////////////////////////║
╚════════════════════════════════════════════════════════╝



# /////// Ensamblador IA-32 (x86 de 32 bits) en Python /////// #

Este proyecto es un **ensamblador básico para la arquitectura IA-32 (x86 de 32 bits)**, desarrollado en Python. Su objetivo es traducir instrucciones en lenguaje ensamblador (archivo '.asm') a código máquina en formato hexadecimal, y generar archivos auxiliares como la **tabla de símbolos** y la **tabla de referencias**.

---

##  Estructura del Proyecto ##

ensamblador/
├── ensamblador.py # Código principal del ensamblador (clase EnsambladorIA32)
├── programa.asm # Archivo de entrada con el código ensamblador
├── programa.hex # Salida con el código máquina en hexadecimal
├── simbolos.txt # Tabla de símbolos con etiquetas y direcciones
├── referencias.txt # Tabla de referencias a etiquetas (saltos, llamadas)
└── README.md # Documentación del proyecto

---

## Ejecución ##

### Requisitos ###

- Python (3.6 o superior)

### Instrucciones ###

1. Escribe tu código ensamblador en 'programa.asm' utilizando instrucciones compatibles.
2. Ejecuta el ensamblador desde la terminal:
    ```bash
    python ensamblador.py
3. Se generarán automáticamente los siguientes archivos:
    programa.hex
    simbolos.txt
    referencias.txt


### Instrucciones Soportadas ###

**Transferencia y operaciones**

Instrucción	      Descripción
mov	              Mueve datos entre registros o hacia/desde memoria
add	              Suma valores de registros o memoria
cmp	              Compara dos operandos
test	            Realiza una operación lógica AND (sin guardar resultado)
imul	            Multiplicación de enteros con signo
inc	              Incrementa el valor de un registro
dec	              Decrementa el valor de un registro

**Saltos condicionales e incondicionales**

Instrucción	      Descripción
jmp	              Salto incondicional
je, jne	          Saltos condicionales según resultado previo
jg, jge	          Salta si mayor / mayor o igual
jl, jle	          Salta si menor / menor o igual
loop	            Disminuye ecx y salta si no es 0

**Subrutinas y pila**

Instrucción	      Descripción
call	            Llama a subrutina
ret	              Retorna de subrutina
push	            Apila un valor/registros
pop	              Saca un valor de la pila
leave	            Limpia el stack frame (equivale a mov esp, ebp + pop ebp)

**Interrupciones**

Instrucción	      Descripción
int	              Ejecuta interrupción del sistema (ej: int 0x80)

**Registros Soportados**

Registro	        Función
eax	              Acumulador general
ebx	              Base
ecx	              Contador
edx	              Datos
esi	              Fuente para cadenas
edi	              Destino para cadenas
esp	              Puntero de pila
ebp	              Base del stack frame



### Funcionamiento Interno ###
El ensamblador procesa el archivo .asm en dos fases:

    Análisis de etiquetas: se registra la dirección de cada etiqueta para poder resolver referencias.
    Traducción a código máquina: se convierte cada instrucción en su forma hexadecimal y se genera el archivo programa.hex.

**Componentes clave**
    1.- procesar_linea(linea): interpreta y traduce una línea individual.
    2.- resolver_referencias(): resuelve las direcciones relativas o absolutas de etiquetas utilizadas en saltos y llamadas.
    3.- ensamblar(lineas): orquesta todo el proceso de ensamblado.
    4.- guardar_archivos(): genera los archivos de salida.

**Consideraciones**
No soporta macros, directivas como .data, ni estructuras avanzadas del lenguaje ensamblador.

Las etiquetas deben ser únicas y estar bien posicionadas.

El conjunto de instrucciones se ajusta para ejecutar ejemplos como:
    -Factorial
    -Serie de Fibonacci
    -Bubble Sort
    -Torres de Hanoi


╔════════════════════════════════════════════════════════╗
║////////////////////////////////////////////////////////║
║#######     ALUMNO: Ortiz García Pablo Adrián    #######║
║////////////////////////////////////////////////////////║
╚════════════════════════════════════════════════════════╝






