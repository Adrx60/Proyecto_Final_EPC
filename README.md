# Ensamblador IA‑32 (x86 de 32 bits) en Python

## 1. Introducción  
**Descripción del problema**  
El propósito de este proyecto es desarrollar un ensamblador para la arquitectura IA‑32 que traduzca código en lenguaje ensamblador a código máquina (hexadecimal). El desafío principal es implementar las fases de análisis léxico de instrucciones, resolución de etiquetas y generación del formato binario, soportando múltiples modos de direccionamiento y diferentes tipos de instrucciones (registros, memoria, saltos, pila, interrupciones, llamadas, unarias). La herramienta debe ser precisa, modular y escalable para agregar más funcionalidades en el futuro.

---

## 2. Desarrollo (Análisis y diseño de la solución)

### 2.1 Análisis  
- **Entrada**: archivo `programa.asm` con instrucciones y etiquetas en sintaxis x86‑32.  
- **Salida**:  
  - `programa.hex` → código máquina en formato hexadecimal.  
  - `simbolos.txt` → tabla de símbolos con direcciones.  
  - `referencias.txt` → posiciones de referencias a etiquetas.  
- **Requisitos**:  
  - Dos fases:  
    1. Procesamiento de cada línea (identificar secciones, etiquetas, instrucciones).  
    2. Resolución de referencias (saltos, llamadas, memoria) con cálculos relativos o absolutos.  
  - Soportar modos de direccionamiento: registro–registro, registro–memoria, inmediato a registro.  
  - Soporte para varios tipos de instrucciones: aritméticas, de salto, llamadas, interrupciones, pila, unarias.

### 2.2 Diseño  
- Clase `EnsambladorIA32`: encapsula funcionalidad de ensamblado.  
  - Atributos:  
    - `codigo`: lista de bytes generados.  
    - `pos_codigo`: posición actual en código.  
    - `tabla_simbolos`, `tabla_referencias`: para etiquetas y referencias.  
    - `datos`: diccionario para datos en `.data`.  
    - `seccion`, `direccion_datos`: para control de secciones.  
  - Métodos principales:  
    - `procesar_linea()`: analiza y traduce cada instrucción.  
    - `resolver_referencias()`: calcula offsets y rellena bytes pendientes.  
    - `ensamblar(lineas)`: ejecuta procesamiento y resolución en orden.  
    - `guardar_archivos()`: exporta salidas necesarias.  
- Diccionarios de códigos de operación (`opcode`): definidos de forma estática para cada instrucción.

---

## 3. Implementación  
El proyecto está estructurado de la siguiente forma:

```
ensamblador/
├── ensamblador.py      # clase EnsambladorIA32 con todo el ensamblador
├── programa.asm        # entrada con código en ensamblador
├── programa.hex        # salida: código máquina hexadecimal
├── simbolos.txt        # salida: tabla de símbolos
├── referencias.txt     # salida: referencias a etiquetas
└── README.md           # documentación (esta actualización)
```

- Se apoya en diccionarios `REGISTROS`, `INSTRUCCIONES_*` para generar opcodes.  
- En `procesar_linea()`, se manejan secciones (`.data`, `.text`), etiquetas (almacenadas en `tabla_simbolos`), instrucciones con operandos variados, y se generan entradas en `tabla_referencias` según necesite relleno.  
- `resolver_referencias()` rellena, tras el parseo inicial, los desplazamientos relativos o absolutos desde las posiciones originales.

---

## 4. Pruebas  
Para verificar el ensamblador:

1. **Casos básicos**:  
   - `mov eax, ebx` → 0x89 / modrm 0xD8.  
   - `add eax, [var]`, `mov [var], eax`, con relleno de direcciones.  
   - Saltos: `jmp etiqueta`, `je etiqueta`.  
   - `call`, `ret`, `push` y `pop` con registros, inmediatos, caracteres.  
   - Interrupciones: `int 0x80`.

2. **Etiquetas y referencias**:  
   - Crear mini-programas con múltiples saltos, llamadas, loops, con comprobación de que `programa.hex`, `simbolos.txt` y `referencias.txt` reflejan correctamente las direcciones.

3. **.data**:  
   - Verificar que variables definidas con `dd` se ubiquen correctamente en la sección de datos y las referencias a memoria se resuelvan.

4. **Tests unitarios (opcional)**:  
   - Usar `unittest` o `pytest` para verificar bytes resultantes de cada instrucción desde cadenas de entrada.

---

## 5. Manual de usuario  
Instrucciones para usar el ensamblador:

1. Instalar Python 3.6 o superior.  
2. Escribir el ensamblador en `programa.asm`.  
3. Ejecutar:
   ```
   python ensamblador.py
   ```
4. Archivos generados:  
   - `programa.hex`: salida de bytes.  
   - `simbolos.txt`: direcciones de variables y etiquetas.  
   - `referencias.txt`: posiciones de saltos y llamadas.

**Sintaxis soportada**:  
- Secciones: `section .data`, `section .text`.  
- Definición de datos: `var dd 1, 2, 3`.  
- Instrucciones comunes: `mov`, `add`, `sub`, `cmp`, `test`, `xor`, `imul`, `inc`, `dec`, saltos (`jmp`, `je`, `jne`, etc.), `push`, `pop`, `call`, `ret`, `leave`, `int`, `loop`.

---

## 6. Manual técnico  
Detalla los componentes:

- **Clases/Diccionarios**:  
  - `REGISTROS`: asignación del registro a un código.  
  - `INSTRUCCIONES_REG_REG`: opcodes base.  
  - Otras estructuras `INSTRUCCIONES_SALTOS`, etc.

- **Procesamiento de operandos**:  
  - Registro directo.  
  - Memoria: detección con `es_memoria()`, mod‑rm, relleno de 4 bytes y referencias.  
  - Inmediatos: códigos especiales para `mov registro, inmediato` y `push inmediato`.

- **Resolución de referencias**:  
  - Relativa: saltos (`jmp`, `je`, `call`, `loop`) calculados desde posición actual.  
  - Absoluta: direcciones de memoria, se almacena directo en 4 bytes en little‑endian.

- **Salida de archivos**:  
  - `programa.hex`: bytes formateados en hexadecimal.  
  - `simbolos.txt`, `referencias.txt`: para debugging y enlace.

---

## 7. Conclusiones  

### Personales (Ortiz García Pablo Adrián)  
- He logrado implementar un ensamblador funcional, con soporte para una amplia gama de instrucciones del conjunto básico x86‑32.  
- La estructura modular de la clase facilita comprender el flujo de alto nivel y mantener el código.  
- Identifiqué y solucioné retos al manejar distintos modos de direccionamiento, cálculos de offsets relativos y absoluto, y el soporte para definiciones de datos.

### Como equipo  
- Desarrollar esta mini‑herramienta fortaleció nuestras competencias en compiladores/ensamblador, análisis de lenguaje y manejo de binarios.  
- El involucramiento en las fases de diseño, implementación y pruebas permitió afianzar buenas prácticas de desarrollo: separación de fases, modularidad, manejo de errores (etiquetas no definidas).  
- Como resultado, contamos con una base sólida que puede extenderse a más instrucciones, optimización y posible generación de secciones ELF o integración con enlazadores.