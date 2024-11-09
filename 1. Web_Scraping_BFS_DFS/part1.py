from math import cos
import queue
import random
import networkx as nx
import networkx
import osmnx as ox
import numpy as np
from memory_profiler import profile,memory_usage
from prettytable import PrettyTable

table = PrettyTable()
place = 'Piedmont, California, USA'

g = ox.graph_from_place(place, network_type='drive')
table.add_row(["networkxPath", "networkxPath(start, end)", "nx.shortest_path(g, start, end, weight='length')", "networkxPath", "networkxPath(start, end)"])
start = list(g.nodes())[0]
table.add_row(["Best_First_Search", "Best_First_Search(graph,start,end)", "q.put((h_n(start,end),start))", "Best_First_Search", "Best_First_Search(graph,start,end)"])
end = list(g.nodes())[323]

dis = 0

def find_sortestDistance(start, end):
      table.add_row(["find_sortestDistance", "find_sortestDistance(start, end)", "nx.shortest_path_length(g, start, end, weight='length')", "find_sortestDistance", "find_sortestDistance(start, end)"])
      return nx.shortest_path_length(g, start, end, weight='length')

def euclidean_distance(node1, node2):
    table.add_row(["euclidean_distance", "euclidean_distance(node1, node2)", "((g.nodes[node1]['x'] - g.nodes[node2]['x'])**2 + (g.nodes[node1]['y'] - g.nodes[node2]['y'])**2)**0.5", "euclidean_distance", "euclidean_distance(node1, node2)"])
    return ((g.nodes[node1]['x'] - g.nodes[node2]['x'])**2 + (g.nodes[node1]['y'] - g.nodes[node2]['y'])**2)**0.5

@profile
def networkxPath(start, end):
      table.add_row(["networkxPath", "networkxPath(start, end)", "nx.shortest_path(g, start, end, weight='length')", "networkxPath", "networkxPath(start, end)"])
      return nx.shortest_path(g, start, end, weight='length')



def h_n(node1,node2,w=1):
  risk = random.uniform(0.1,1)
  table.add_row(["h_n", "h_n(node1,node2,w=1)", "w*(g_n + g_n*risk)", "h_n", "h_n(node1,node2,w=1)"])
  g_n = euclidean_distance(node1,node2)
  
  return w*(g_n + g_n*risk)

def g_n(node1,node2):
  table.add_row(["g_n", "g_n(node1,node2)", "euclidean_distance(node1,node2)", "g_n", "g_n(node1,node2)"])
  return euclidean_distance(node1,node2)



from queue import PriorityQueue
import heapq      
@profile
def Best_First_Search(graph,start,end):
        q = PriorityQueue()
        cost_dict = {}
        q.put((h_n(start,end),start))
        queue_temp = queue.PriorityQueue()
        cost_dict[start] = h_n(start,end)
        visited = set()
        queue_temp.put((h_n(start,end),start))
        path = {
            start : None
        }
        queue_temp.put((h_n(start,end),start))
        while not q.empty():
            queue_temp.put((h_n(start,end),start))
            item = q.get()
            queue_temp.put((h_n(start,end),item))
            cur_priority,cur_node = item[0],item[1]
            queue_temp.put((h_n(start,end),cur_node))
            if cur_node==end:
              queue_temp.put((h_n(start,end),end))
              temp = path[end]
              result = []
              queue_temp.put((h_n(start,end),temp))
              result.append(end)
              while temp is not None:
                result.append(temp)
                queue_temp.put((h_n(start,end),temp))
                temp = path[temp]
              return result[::-1]

            if cur_node in visited:
              continue

            visited.add(cur_node)

            for neighbor in graph.neighbors(cur_node):
              queue_temp.put((h_n(start,end),neighbor))
              if neighbor not in visited:
                assumed_cost = h_n(neighbor,end)
                if neighbor in cost_dict.keys():
                  table.add_row(["Best_First_Search", "Best_First_Search(graph,start,end)", "if cost_dict[neighbor]>assumed_cost:", "Best_First_Search", "Best_First_Search(graph,start,end)"])
                  if cost_dict[neighbor]>assumed_cost:
                    cost_dict[neighbor] = assumed_cost
                    table.add_row(["Best_First_Search", "Best_First_Search(graph,start,end)", "path[neighbor] = cur_node", "Best_First_Search", "Best_First_Search(graph,start,end)"])
                    path[neighbor] = cur_node
                    q.put((assumed_cost,neighbor))
                    print("Reached")
                else:
                  cost_dict[neighbor] = assumed_cost
                  print(cost_dict[neighbor])
                  path[neighbor] = cur_node
                  print("Reached")
                  q.put((assumed_cost,neighbor))
                  table.add_row(["Best_First_Search", "Best_First_Search(graph,start,end)", "q.put((assumed_cost,neighbor))", "Best_First_Search", "Best_First_Search(graph,start,end)"])

        if end not in path.keys():
          return []


@profile
def A_Star_Algorithm(graph,start,end):
        q = PriorityQueue()
        cost_dict = {}
        print("q.put((0+h_n(start,end),start))")
        q.put((0+h_n(start,end),start))
        table.add_row(["A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)", "cost_dict[neighbor] = assumed_cost", "A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)"])
        cost_dict[start] = 0+h_n(start,end)
        visited = set()
        dict_of_g_n = {}
        dict_of_g_n[start] = 0
        path = {
            start : None
        }
        while not q.empty():
            item = q.get()
            table.add_row(["A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)", "item = q.get()", "A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)"])
            cur_priority,cur_node = item[0],item[1]

            if cur_node==end:
              temp = path[end]
              result = []
              result.append(end)
              table.add_row(["A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)", "result.append(end)", "A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)"])
              while temp is not None:
                result.append(temp)
                temp = path[temp]
              return result[::-1]
              table.add_row(["A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)", "return result[::-1]", "A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)"])
            if cur_node in visited:
              continue

            visited.add(cur_node)

            for neighbor in graph.neighbors(cur_node):
              if neighbor not in visited:
                table.add_row(["A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)", "assumed_cost = dict_of_g_n[cur_node] + g_n(cur_node,neighbor) + h_n(neighbor,end)", "A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)"])
                assumed_cost = dict_of_g_n[cur_node] + g_n(cur_node,neighbor) + h_n(neighbor,end)
                if neighbor in cost_dict.keys():
                  if cost_dict[neighbor]>assumed_cost:
                    cost_dict[neighbor] = assumed_cost
                    path[neighbor] = cur_node
                    table.add_row(["A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)", "cost_dict[neighbor] = assumed_cost", "A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)"])
                    q.put((assumed_cost,neighbor))
                    dict_of_g_n[neighbor] = dict_of_g_n[cur_node] + g_n(cur_node,neighbor)
                else:
                  cost_dict[neighbor] = assumed_cost
                  path[neighbor] = cur_node
                  table.add_row(["A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)", "cost_dict[neighbor] = assumed_cost", "A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)"])
                  q.put((assumed_cost,neighbor))
                  dict_of_g_n[neighbor] = dict_of_g_n[cur_node] + g_n(cur_node,neighbor)

        if end not in path.keys():
          return []




import matplotlib.pyplot as plt
@profile
def Weighted_A_Star_Algorithm(graph,start,end,w):
        q = PriorityQueue()
        cost_dict = {}
        table.add_row(["Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,w)", "q.put((0+h_n(start,end,w),start))", "Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,w)"])
        q.put((0+h_n(start,end,w),start))
        print("cost_dict[start] = 0+h_n(start,end,w)")
        cost_dict[start] = 0+h_n(start,end,w)
        print("visited = set()")             
        visited = set()
        dict_of_g_n = {}
        dict_of_g_n[start] = 0
        table.add_row(["Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,w)", "path = {start : None}", "Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,w)"])
        path = {
            start : None
        }
        while not q.empty():
            item = q.get()
            cur_priority,cur_node = item[0],item[1]

            if cur_node==end:
              temp = path[end]
              result = []
              result.append(end)
              while temp is not None:
                table.add_row(["Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,w)", "result.append(temp)", "Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,w)"])
                result.append(temp)
                temp = path[temp]
              return result[::-1]

            if cur_node in visited:
              continue

            visited.add(cur_node)

            for neighbor in graph.neighbors(cur_node):
              if neighbor not in visited:
                table.add_row(["Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,w)", "assumed_cost = dict_of_g_n[cur_node] + g_n(cur_node,neighbor) + h_n(neighbor,end,w)", "Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,w)"])
                assumed_cost = dict_of_g_n[cur_node] + g_n(cur_node,neighbor) + h_n(neighbor,end,w)
                if neighbor in cost_dict.keys():
                  if cost_dict[neighbor]>assumed_cost:
                    cost_dict[neighbor] = assumed_cost
                    table.add_row(["Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,w)", "cost_dict[neighbor] = assumed_cost", "Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,w)"])
                    path[neighbor] = cur_node
                    q.put((assumed_cost,neighbor))
                    dict_of_g_n[neighbor] = dict_of_g_n[cur_node] + g_n(cur_node,neighbor)
                else:
                  cost_dict[neighbor] = assumed_cost
                  path[neighbor] = cur_node
                  table.add_row(["Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,w)", "q.put((assumed_cost,neighbor))", "Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,w)"])
                  q.put((assumed_cost,neighbor))
                  dict_of_g_n[neighbor] = dict_of_g_n[cur_node] + g_n(cur_node,neighbor)

        if end not in path.keys():
          return []





run_time = []
memory_use = []
routes = []



def plot_memory_usage(memory_use):
      #plot memory usage with x axis as time 0.1 difference
      fig = plt.figure(figsize = (10, 6))
      table.add_row(["plot_memory_usage", "plot_memory_usage(memory_use)", "plt.plot(np.linspace(0.1, 0.1 * len(memory_use[0]), len(memory_use[0])), memory_use[0])", "plot_memory_usage", "plot_memory_usage(memory_use)"])
      plt.plot(np.linspace(0.1, 0.1 * len(memory_use[0]), len(memory_use[0])), memory_use[0], 
      label='Networkx', color='blue')
      table.add_row(["plot_memory_usage", "plot_memory_usage(memory_use)", "plt.plot(np.linspace(0.1, 0.1 * len(memory_use[0]), len(memory_use[0])), memory_use[0])", "plot_memory_usage", "plot_memory_usage(memory_use)"])
      plt.plot(np.linspace(0.1, 0.1 * len(memory_use[1]), len(memory_use[1])), memory_use[1],
      label='Best_First_Search', color='red')

      table.add_row(["plot_memory_usage", "plot_memory_usage(memory_use)", "plt.plot(np.linspace(0.1, 0.1 * len(memory_use[3]), len(memory_use[3])), memory_use[3])", "plot_memory_usage", "plot_memory_usage(memory_use)"])
      plt.plot(np.linspace(0.1, 0.1 * len(memory_use[2]), len(memory_use[2])), memory_use[2],
        label='A_Star_Algorithm', color='green')
      print("Memory Usage: ", memory_use[0])
      plt.plot(np.linspace(0.1, 0.1 * len(memory_use[3]), len(memory_use[3])), memory_use[3],
        label='Weighted_A_Star_Algorithm', color='yellow')
      

      plt.xlabel('Time (s)')
      plt.ylabel('Memory (MB)')
      plt.title('Memory Usage')
      table.add_row(["plot_memory_usage", "plot_memory_usage(memory_use)", "plt.show()", "plot_memory_usage", "plot_memory_usage(memory_use)"])
      plt.legend()
      plt.show()
      print("Memory Usage: ", memory_use[0])
      
def draw_bar_comparison_algorithm_time(run_time):
      fig = plt.figure(figsize = (10, 6))

      table.add_row(["draw_bar_comparison_algorithm_time", "draw_bar_comparison_algorithm_time(run_time)", "plt.bar(['Networkx', 'Best_First_Search'\n        , 'A_Star_Algorithm', 'Weighted_A_Star_Algorithm'], run_time, color=['blue', 'red', 'green', 'yellow'])", "draw_bar_comparison_algorithm_time", "draw_bar_comparison_algorithm_time(run_time)"])
      
      plt.bar(['Networkx', 'Best_First_Search'
        , 'A_Star_Algorithm', 'Weighted_A_Star_Algorithm'], run_time, color=['blue', 'red', 'green', 'yellow'])
      print("Run Time: ", run_time)
      plt.xlabel('Algorithm')

      table.add_row(["draw_bar_comparison_algorithm_time", "draw_bar_comparison_algorithm_time(run_time)", "plt.ylabel('Time (seconds)')", "draw_bar_comparison_algorithm_time", "draw_bar_comparison_algorithm_time(run_time)"])
      plt.ylabel('Time (s)')
      plt.title('Comparison of Time Taken by Algorithms')
      plt.show()

import time

if __name__ == '__main__':
        start_time = time.time()
        table.add_row(["start_time", "start_time = time.time()", "start_time", "start_time", "start_time"])
        networkx_memory, networkx_path = memory_usage((networkxPath, (start, end)), retval=True)
        routes.append(networkx_path)
        table.add_row(["networkxPath", "networkxPath(start, end)", "nx.shortest_path(g, start, end, weight='length')", "networkxPath", "networkxPath(start, end)"])
        memory_use.append(networkx_memory)
        end_time = time.time()
        networkx_time = end_time - start_time
        table.add_row(["networkxPath", "networkxPath(start, end)", "nx.shortest_path(g, start, end, weight='length')", "networkxPath", "networkxPath(start, end)"])
        run_time.append(networkx_time)

        start_time = time.time()
        table.add_row(["start_time", "start_time = time.time()", "start_time", "start_time", "start_time"])
        best_first_search_memory, best_first_search_path = memory_usage((Best_First_Search, (g, start, end)), retval=True)
        routes.append(best_first_search_path)
        memory_use.append(best_first_search_memory)
        table.add_row(["Best_First_Search", "Best_First_Search(graph,start,end)", "q.put((h_n(start,end),start))", "Best_First_Search", "Best_First_Search(graph,start,end)"])
        end_time = time.time()
        best_first_search_time = end_time - start_time
        table.add_row(["Best_First_Search", "Best_First_Search(graph,start,end)", "q.put((h_n(start,end),start))", "Best_First_Search", "Best_First_Search(graph,start,end)"])
        run_time.append(best_first_search_time)

        start_time = time.time()
        a_star_memory, a_star_path = memory_usage((A_Star_Algorithm, (g, start, end)), retval=True)
        table.add_row(["A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)", "q.put((0+h_n(start,end),start))", "A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)"])
        routes.append(a_star_path)
        memory_use.append(a_star_memory)
        end_time = time.time()
        table.add_row(["A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)", "q.put((0+h_n(start,end),start))", "A_Star_Algorithm", "A_Star_Algorithm(graph,start,end)"])
        a_star_time = end_time - start_time
        run_time.append(a_star_time)


        start_time = time.time()
        weighted_a_star_memory, weighted_a_star_path = memory_usage((Weighted_A_Star_Algorithm, (g, start, end, 2.5)), retval=True)
        table.add_row(["Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,2.5)", "q.put((0+h_n(start,end,w),start))", "Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,2.5)"])
        routes.append(weighted_a_star_path)
        memory_use.append(weighted_a_star_memory)
        end_time = time.time()
        table.add_row(["Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,2.5)", "q.put((0+h_n(start,end,w),start))", "Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,2.5)"])
        weighted_a_star_time = end_time - start_time
        run_time.append(weighted_a_star_time)
        table.add_row(["Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,2.5)", "q.put((0+h_n(start,end,w),start))", "Weighted_A_Star_Algorithm", "Weighted_A_Star_Algorithm(graph,start,end,2.5)"])
        draw_bar_comparison_algorithm_time(run_time)
        plot_memory_usage(memory_use)

        bg = ['b', 'r', 'g', 'y']
        table.add_row(["bg", "bg = ['b', 'r', 'g', 'y']", "ox.plot_graph_routes(g, routes, route_linewidth=6, node_size=0, route_colors=bg)", "bg", "bg = ['b', 'r', 'g', 'y']"])
        ox.plot_graph_routes(g, routes, route_linewidth=6, node_size=0, route_colors=bg)
        print(routes[0])
        

