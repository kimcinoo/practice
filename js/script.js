const graph = {
   A: ["B", "C"],
   B: ["A", "D"],
   C: ["A", "G", "H", "I"],
   D: ["B", "E", "F"],
   E: ["D"],
   F: ["D"],
   G: ["C"],
   H: ["C"],
   I: ["C", "J"],
   J: ["I"]
};

const BFS = (graph, startNode) => {
   const visited = [];
   let needVisit = [];
   needVisit.push(startNode);
   while (needVisit.length !== 0 ) {
      const node = needVisit.shift();
      if (!visited.includes(node)) {
         visited.push(node);
         needVisit = [...needVisit, ...graph[node]];
      }
   }
   return visited;
};

const DFS = (graph, startNode) => {
   const visited = [];
   let needVisit = [];
   needVisit.push(startNode);
   while (needVisit.length !== 0 ) {
      const node = needVisit.shift();
      if (!visited.includes(node)) {
         visited.push(node);
         needVisit = [...graph[node], ...needVisit];
      }
   }
   return visited;
};


let result = document.getElementById("bfs-result");
result.innerText = BFS(graph, "A");

result = document.getElementById("dfs-result");
result.innerText = DFS(graph, "A");
