import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

# Posição (linha, coluna) de cada peça no estado objetivo
_GOAL_POS = {tile: divmod(index, 3) for index, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):
    """Busca A* com f(n) = g(n) + h(n)."""

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan (soma das distâncias de cada peça à sua posição final).

        Admissível: cada movimento desloca uma peça em apenas uma casa,
        então a heurística nunca superestima o custo real. Também é consistente.
        O espaço vazio (0) não entra na soma.
        """
        total = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            row, col = divmod(index, 3)
            goal_row, goal_col = _GOAL_POS[tile]
            total += abs(row - goal_row) + abs(col - goal_col)
        return total

    def search(self, initial: State) -> SearchResult:
        generated = 1
        expanded = 0

        tie = count()  # desempate estável no heap
        frontier = [(self.heuristic(initial), next(tie), initial)]
        max_frontier = 1
        best_g = {initial.tiles: initial.cost}
        closed = set()

        while frontier:
            _, _, current = heapq.heappop(frontier)

            if current.tiles in closed:
                continue  # entrada obsoleta (já existe caminho melhor expandido)

            if current.is_goal:
                return SearchResult(current, expanded, generated, max_frontier, current.cost)

            closed.add(current.tiles)
            expanded += 1

            for child in current.neighbors():
                if child.tiles in closed:
                    continue
                known = best_g.get(child.tiles)
                if known is not None and known <= child.cost:
                    continue
                best_g[child.tiles] = child.cost
                f = child.cost + self.heuristic(child)
                heapq.heappush(frontier, (f, next(tie), child))
                generated += 1

            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, expanded, generated, max_frontier, 0)