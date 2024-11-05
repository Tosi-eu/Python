import pulp
import random

# Definindo o navio com restrições de peso e dimensões
class Ship:
    def __init__(self, length, width, height, max_weight):
        self.length = length
        self.width = width
        self.height = height
        self.max_weight = max_weight 
        self.volume = length * width * height 
        self.container_volume_limit = 0.35 * self.volume  

# Definindo os tipos de contêineres (dimensões e peso variáveis)
class ContainerType:
    def __init__(self, name, length, width, height, weight):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight

    # Retorna todas as orientações possíveis do contêiner
    def orientations(self):
        return [
            (self.length, self.width, self.height),
            (self.length, self.height, self.width),
            (self.width, self.length, self.height),
            (self.width, self.height, self.length),
            (self.height, self.length, self.width),
            (self.height, self.width, self.length),
        ]

# Função para otimizar a alocação de contêineres em múltiplos navios considerando orientações
def optimize_container_allocation(ships, container_types):
    # Cria o problema de otimização
    problem = pulp.LpProblem("ContainerAllocation", pulp.LpMaximize)

    # Variáveis de decisão: quantidade de cada tipo de contêiner em cada orientação e em cada navio
    container_vars = {}
    for ship in ships:
        for ctype in container_types:
            for i, (l, w, h) in enumerate(ctype.orientations()):
                var_name = f"{ctype.name}_orient_{i}_ship_{ships.index(ship)}"
                container_vars[var_name] = pulp.LpVariable(var_name, lowBound=0, cat="Integer")

    # Função objetivo: maximizar o número total de contêineres alocados em todos os navios
    problem += pulp.lpSum(container_vars[var_name] for var_name in container_vars)

    # Restrições de volume e peso para cada navio
    for ship in ships:
        ship_idx = ships.index(ship)
        
        # Restrição de volume: apenas 35% do volume do navio pode ser utilizado para containers
        problem += pulp.lpSum(
            container_vars[f"{ctype.name}_orient_{i}_ship_{ship_idx}"] * l * w * h
            for ctype in container_types
            for i, (l, w, h) in enumerate(ctype.orientations())
        ) <= ship.container_volume_limit, f"VolumeConstraint_Ship_{ship_idx}"
        
        # Restrição de peso: a soma dos pesos dos contêineres não pode exceder o peso máximo do navio
        problem += pulp.lpSum(
            container_vars[f"{ctype.name}_orient_{i}_ship_{ship_idx}"] * ctype.weight
            for ctype in container_types
            for i in range(len(ctype.orientations()))
        ) <= ship.max_weight, f"WeightConstraint_Ship_{ship_idx}"

        # Restrição para garantir que nenhum tipo de contêiner seja dominante (máx. 50% dos contêineres em cada navio)
        total_containers_ship = pulp.lpSum(
            container_vars[f"{ctype.name}_orient_{i}_ship_{ship_idx}"]
            for ctype in container_types
            for i in range(len(ctype.orientations()))
        )

        for ctype in container_types:
            problem += pulp.lpSum(
                container_vars[f"{ctype.name}_orient_{i}_ship_{ship_idx}"]
                for i in range(len(ctype.orientations()))
            ) <= 0.5 * total_containers_ship, f"Max50Percent_{ctype.name}_Ship_{ship_idx}"

    # Restrições para garantir que pelo menos 1 contêiner de cada tipo seja alocado
    for ctype in container_types:
        for ship in ships:
            ship_idx = ships.index(ship)
            problem += pulp.lpSum(container_vars[f"{ctype.name}_orient_{i}_ship_{ship_idx}"]
                                  for i in range(len(ctype.orientations()))) >= 1, f"MinContainer_{ctype.name}_Ship_{ship_idx}"

    # Resolve o problema
    problem.solve()

    # Verifica o status da solução
    if pulp.LpStatus[problem.status] == "Optimal":
        print("Solução Ótima Encontrada:")
        for ship in ships:
            ship_idx = ships.index(ship)
            print(f"\nAlocação para o Navio {ship_idx + 1}:")
            for ctype in container_types:
                for i, (l, w, h) in enumerate(ctype.orientations()):
                    var_name = f"{ctype.name}_orient_{i}_ship_{ship_idx}"
                    count = int(container_vars[var_name].value())
                    if count > 0:
                        print(f"{ctype.name} na orientação ({l}x{w}x{h}): {count} contêineres")
    else:
        print("Não foi possível encontrar uma solução ótima.")

# Main
if __name__ == "__main__":
    # Gerando dados de navios (484 navios com capacidades e tamanhos variados)
    ships = []
    for _ in range(484):
        ship_length = random.randint(80, 120)  # Comprimento
        ship_width = random.randint(40, 60)    # Largura
        ship_height = random.randint(25, 35)   # Altura
        ship_max_weight = random.randint(800000, 1500000)  # Peso máximo
        ships.append(Ship(ship_length, ship_width, ship_height, ship_max_weight))

    # Definindo tipos de contêineres (com dimensões variáveis e peso)
    container_types = [
        ContainerType("Tipo A", length=2, width=1, height=1, weight=10),
        ContainerType("Tipo B", length=5, width=3, height=5, weight=5),
        ContainerType("Tipo C", length=3, width=2, height=2, weight=20)
    ]

    # Otimizando a alocação de contêineres nos navios considerando orientações
    optimize_container_allocation(ships, container_types)
