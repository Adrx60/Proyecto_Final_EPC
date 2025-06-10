import re

REGISTROS = {
    'eax': 0, 'ecx': 1, 'edx': 2, 'ebx': 3,
    'esp': 4, 'ebp': 5, 'esi': 6, 'edi': 7
}

INSTRUCCIONES_REG_REG = {
    'mov': 0x89, 'add': 0x01, 'cmp': 0x39, 'test': 0x85,
    'sub': 0x29, 'xor': 0x31
}

INSTRUCCIONES_SALTOS = {
    'jmp': 0xEB, 'je': 0x74, 'jne': 0x75,
    'jge': 0x7D, 'jg': 0x7F, 'jl': 0x7C, 'jle': 0x7E,
    'jz': 0x74, 'jnz': 0x75, 'ja': 0x77, 'jae': 0x73,
    'jb': 0x72, 'jbe': 0x76, 'jg': 0x7F, 'jge': 0x7D
}

INSTRUCCIONES_UNARIAS = {
    'inc': 0x40, 'dec': 0x48
}

class EnsambladorIA32:
    def __init__(self):
        self.codigo = []
        self.pos_codigo = 0
        self.tabla_simbolos = {}
        self.tabla_referencias = []
        self.datos = {}
        self.seccion = None
        self.direccion_datos = 0x1000

    def agregar_direccion(self, direccion):
        self.codigo += [direccion & 0xFF, (direccion >> 8) & 0xFF,
                        (direccion >> 16) & 0xFF, (direccion >> 24) & 0xFF]

    def es_memoria(self, op):
        return op.startswith('[') and op.endswith(']')

    def procesar_linea(self, linea):
        linea = linea.split(';')[0].strip()
        if not linea:
            return

        if linea.startswith('section'):
            self.seccion = linea.split()[1]
            return

        if self.seccion == '.data':
            if 'dd' in linea:
                partes = linea.split()
                nombre = partes[0]
                valores = [int(v.strip().strip(',')) for v in ' '.join(partes[2:]).split()]
                self.tabla_simbolos[nombre] = self.direccion_datos
                for val in valores:
                    self.datos[self.direccion_datos] = val
                    self.direccion_datos += 4
            return

        if ':' in linea:
            etiqueta = linea.replace(':', '')
            self.tabla_simbolos[etiqueta] = self.pos_codigo
            return

        partes = linea.replace(',', ' ').split()
        if not partes:
            return
        mnemonico = partes[0].lower()
        operandos = partes[1:]

        if mnemonico in INSTRUCCIONES_REG_REG and len(operandos) == 2:
            dest, src = operandos
            opcode = INSTRUCCIONES_REG_REG[mnemonico]
            if dest in REGISTROS and src in REGISTROS:
                modrm = (0b11 << 6) | (REGISTROS[src] << 3) | REGISTROS[dest]
                self.codigo += [opcode, modrm]
                self.pos_codigo += 2
            elif dest in REGISTROS and self.es_memoria(src):
                base = src[1:-1]
                modrm = (0b00 << 6) | (REGISTROS[dest] << 3) | 0b101
                self.codigo.append(opcode + 2)
                self.codigo.append(modrm)
                self.codigo += [0x00] * 4
                self.tabla_referencias.append((len(self.codigo) - 4, base, False))
                self.pos_codigo += 6
            elif self.es_memoria(dest) and src in REGISTROS:
                base = dest[1:-1]
                modrm = (0b00 << 6) | (REGISTROS[src] << 3) | 0b101
                self.codigo.append(opcode)
                self.codigo.append(modrm)
                self.codigo += [0x00] * 4
                self.tabla_referencias.append((len(self.codigo) - 4, base, False))
                self.pos_codigo += 6

        elif mnemonico == 'mov' and len(operandos) == 2:
            dest, src = operandos
            if dest in REGISTROS and (src.startswith('0x') or src.isdigit()):
                valor = int(src, 0)
                self.codigo.append(0xB8 + REGISTROS[dest])
                self.agregar_direccion(valor)
                self.pos_codigo += 5
            elif dest in REGISTROS and self.es_memoria(src):
                base = src[1:-1]
                modrm = (0b00 << 6) | (REGISTROS[dest] << 3) | 0b101
                self.codigo.append(0x8B)
                self.codigo.append(modrm)
                self.codigo += [0x00] * 4
                self.tabla_referencias.append((len(self.codigo) - 4, base, False))
                self.pos_codigo += 6
            elif self.es_memoria(dest) and src in REGISTROS:
                base = dest[1:-1]
                modrm = (0b00 << 6) | (REGISTROS[src] << 3) | 0b101
                self.codigo.append(0x89)
                self.codigo.append(modrm)
                self.codigo += [0x00] * 4
                self.tabla_referencias.append((len(self.codigo) - 4, base, False))
                self.pos_codigo += 6

        elif mnemonico == 'imul' and len(operandos) == 2:
            dest, src = operandos
            self.codigo += [0x0F, 0xAF]
            modrm = (0b11 << 6) | (REGISTROS[src] << 3) | REGISTROS[dest]
            self.codigo.append(modrm)
            self.pos_codigo += 3

        elif mnemonico in INSTRUCCIONES_UNARIAS and len(operandos) == 1:
            reg = operandos[0]
            self.codigo.append(INSTRUCCIONES_UNARIAS[mnemonico] + REGISTROS[reg])
            self.pos_codigo += 1

        elif mnemonico in INSTRUCCIONES_SALTOS and len(operandos) == 1:
            etiqueta = operandos[0]
            self.codigo.append(INSTRUCCIONES_SALTOS[mnemonico])
            self.codigo.append(0x00)
            self.tabla_referencias.append((len(self.codigo) - 1, etiqueta, True))
            self.pos_codigo += 2

        elif mnemonico == 'int' and len(operandos) == 1:
            self.codigo += [0xCD, int(operandos[0], 0)]
            self.pos_codigo += 2

        elif mnemonico == 'loop' and len(operandos) == 1:
            etiqueta = operandos[0]
            self.codigo.append(0xE2)
            self.codigo.append(0x00)
            self.tabla_referencias.append((len(self.codigo) - 1, etiqueta, True))
            self.pos_codigo += 2

        elif mnemonico == 'push' and len(operandos) == 1:
            op = operandos[0]
            if op in REGISTROS:
                self.codigo.append(0x50 + REGISTROS[op])
                self.pos_codigo += 1
            elif op.startswith("'") and op.endswith("'"):
                valor = ord(op[1])
                self.codigo.append(0x68)
                self.agregar_direccion(valor)
                self.pos_codigo += 5
            elif op.isdigit() or (op.startswith('0x') and len(op) > 2):
                valor = int(op, 0)
                self.codigo.append(0x68)
                self.agregar_direccion(valor)
                self.pos_codigo += 5

        elif mnemonico == 'pop' and len(operandos) == 1:
            reg = operandos[0]
            self.codigo.append(0x58 + REGISTROS[reg])
            self.pos_codigo += 1

        elif mnemonico == 'call' and len(operandos) == 1:
            etiqueta = operandos[0]
            self.codigo.append(0xE8)
            self.codigo += [0x00] * 4
            self.tabla_referencias.append((len(self.codigo) - 4, etiqueta, False))
            self.pos_codigo += 5

        elif mnemonico == 'ret':
            self.codigo.append(0xC3)
            self.pos_codigo += 1

        elif mnemonico == 'leave':
            self.codigo.append(0xC9)
            self.pos_codigo += 1

    def resolver_referencias(self):
        for ref in self.tabla_referencias:
            pos, etiqueta, relativo = ref
            if etiqueta not in self.tabla_simbolos:
                print(f"Error: etiqueta no definida -> {etiqueta}")
                continue
            destino = self.tabla_simbolos[etiqueta]
            if relativo:
                offset = destino - (pos + 1)
                self.codigo[pos] = offset & 0xFF
            else:
                offset = destino - (pos + 4)
                for i in range(4):
                    self.codigo[pos + i] = (offset >> (8 * i)) & 0xFF

    def ensamblar(self, lineas):
        for linea in lineas:
            self.procesar_linea(linea.strip())
        self.resolver_referencias()
        return self.codigo

    def guardar_archivos(self):
        with open("programa.hex", 'w') as f:
            for byte in self.codigo:
                f.write(f"{byte:02X} ")

        with open("simbolos.txt", 'w') as f:
            for simb, dir in self.tabla_simbolos.items():
                f.write(f"{simb}: {dir:04X}\n")

        with open("referencias.txt", 'w') as f:
            for ref in self.tabla_referencias:
                pos, etiqueta = ref[0], ref[1]
                f.write(f"{etiqueta}: {hex(pos)}\n")

if __name__ == "__main__":
    ensamblador = EnsambladorIA32()
    with open("programa.asm", "r") as archivo:
        lineas = archivo.readlines()
    ensamblador.ensamblar(lineas)
    ensamblador.guardar_archivos()
