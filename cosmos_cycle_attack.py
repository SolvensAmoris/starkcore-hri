#!/usr/bin/env python3

print("=== CA-008 CAUSAL CYCLE ATTACK ===")


class CycleError(Exception):
    pass



class CosmosGraph:


    def __init__(self):

        self.parents = {}



    def add_node(self, node):

        if node not in self.parents:
            self.parents[node] = []



    def add_edge(self, child, parent):

        print(
            f"Intentando conectar {child} -> {parent}"
        )


        if self.detect_cycle(
            child,
            parent
        ):
            raise CycleError(
                f"Ciclo detectado: {child} depende de {parent}"
            )


        self.parents[child].append(parent)



    def detect_cycle(self, child, parent):

        """
        Pregunta:
        si agrego child -> parent,
        ¿puedo regresar a child?
        """

        visited = set()


        def walk(node):

            if node == child:
                return True


            if node in visited:
                return False


            visited.add(node)


            for p in self.parents.get(node, []):

                if walk(p):
                    return True


            return False


        return walk(parent)



cosmos = CosmosGraph()


for n in ["A","B","C"]:

    cosmos.add_node(n)



print("\n=== CREANDO CADENA NORMAL ===")


cosmos.add_edge("B","A")
cosmos.add_edge("C","B")


print("✅ Cadena A ← B ← C creada")


print("\n=== ATAQUE ===")


try:

    cosmos.add_edge(
        "A",
        "C"
    )


    print(
        "🚨 FALLA: ciclo aceptado"
    )


except CycleError as e:

    print(
        "✅ ATAQUE DETENIDO"
    )

    print(e)



print("\nGrafo final:")

print(cosmos.parents)

