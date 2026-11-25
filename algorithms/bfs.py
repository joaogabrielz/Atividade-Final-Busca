from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):
    """Busca em Largura (fila FIFO + conjunto de visitados).

    Completa e ótima para custo uniforme (cada movimento custa 1).
    """

    def search(self, initial: State) -> SearchResult:
        generated = 1
        expanded = 0
        max_frontier = 1

        if initial.is_goal:
            return SearchResult(initial, expanded, generated, max_frontier, initial.cost)

        frontier = deque([initial])
        visited = {initial.tiles}

        while frontier:
            current = frontier.popleft()
            expanded += 1

            for child in current.neighbors():
                if child.tiles in visited:
                    continue
                visited.add(child.tiles)
                generated += 1

                # Teste de objetivo na geração: garante o menor número de expansões
                if child.is_goal:
                    return SearchResult(child, expanded, generated, max(max_frontier, len(frontier) + 1), child.cost)

                frontier.append(child)

            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, expanded, generated, max_frontier, 0)