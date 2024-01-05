import cv2
from collections import deque

INF = 10000
MAP_HEIGHT, MAP_WIDTH = 131, 131


class Position2D:
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class MapPoint:
    def __init__(self):
        self.occupancy = INF
        self.cost = 0.0
        self.exitCost = 0.0
        self.isVisited = False
        self.costComputed = False
        self.exitChecked = False
        self.isTracked = False
        self.visitedNum = 0
        self.next_point_position = Position2D(INF, INF)
        self.prev_point_position = Position2D(INF, INF)


prob_map = {}  # position-point
candidate_positions = deque()
optimal_path = deque()
shortcut_candidate_positions = deque()
sub_path = deque()
isExitFound = False
isPlanningFinished = False


def get_neighbors(root_position):
    neighbor_positions = [
        Position2D(root_position.x - 1, root_position.y - 1),
        Position2D(root_position.x, root_position.y - 1),
        Position2D(root_position.x + 1, root_position.y - 1),
        Position2D(root_position.x - 1, root_position.y),
        Position2D(root_position.x + 1, root_position.y),
        Position2D(root_position.x - 1, root_position.y + 1),
        Position2D(root_position.x, root_position.y + 1),
        Position2D(root_position.x + 1, root_position.y + 1)
    ]
    return neighbor_positions


def update_neighbors(root_position):
    neighbor_positions = get_neighbors(root_position)

    for neighbor_position in neighbor_positions:
        if not (0 <= neighbor_position.x <= (MAP_HEIGHT - 1) and 0 <= neighbor_position.y <= (MAP_WIDTH - 1)):
            continue
        elif prob_map[neighbor_position].occupancy != INF:
            if not prob_map[neighbor_position].costComputed:
                prob_map[neighbor_position].cost = prob_map[root_position].cost + 1
                prob_map[neighbor_position].costComputed = True
                candidate_positions.append(neighbor_position)


def wave_front_spread(start_position):
    prob_map[start_position].costComputed = True
    curr_position = start_position
    update_neighbors(curr_position)

    while candidate_positions:
        curr_position = candidate_positions.popleft()
        update_neighbors(curr_position)


def reset_exit_cost():
    for i in range(MAP_WIDTH):
        for j in range(MAP_HEIGHT):
            prob_map[Position2D(i, j)].exitChecked = False
            prob_map[Position2D(i, j)].exitCost = 0.0
            prob_map[Position2D(i, j)].isTracked = False
    shortcut_candidate_positions.clear()
    sub_path.clear()


def find_exit(stuck_position):
    neighbor_positions = get_neighbors(stuck_position)
    exit_point = Position2D(INF, INF)

    for neighbor_position in neighbor_positions:
        if not (0 <= neighbor_position.x <= (MAP_HEIGHT - 1) and 0 <= neighbor_position.y <= (MAP_WIDTH - 1)):
            continue
        elif prob_map[neighbor_position].occupancy != INF and not prob_map[neighbor_position].isVisited:
            global isExitFound
            isExitFound = True
            prob_map[neighbor_position].prev_point_position = stuck_position
            exit_point = neighbor_position
            break
        elif prob_map[neighbor_position].occupancy != INF and not prob_map[neighbor_position].exitChecked:
            prob_map[neighbor_position].exitChecked = True
            prob_map[neighbor_position].exitCost = prob_map[stuck_position].exitCost + 1
            prob_map[neighbor_position].prev_point_position = stuck_position
            shortcut_candidate_positions.append(neighbor_position)

    return exit_point

def corner_escape(stuck_position):
    prob_map[stuck_position].exitChecked = True
    prob_map[stuck_position].isTracked = True
    curr_position = stuck_position
    found_point = find_exit(curr_position)

    current_position = None

    while shortcut_candidate_positions:
        curr_position = shortcut_candidate_positions.popleft()
        found_point = find_exit(curr_position)

        if found_point.x != INF and found_point.y != INF:
            current_position = found_point
            while prob_map[current_position].prev_point_position.x != INF and prob_map[current_position].prev_point_position.y != INF and not prob_map[current_position].isTracked:
                prob_map[current_position].isVisited = True
                prob_map[current_position].visitedNum += 1
                prob_map[current_position].isTracked = True
                sub_path.appendleft(current_position)
                current_position = prob_map[current_position].prev_point_position

            global isExitFound
            isExitFound = False
            reset_exit_cost()
            return

    global isPlanningFinished
    isPlanningFinished = True
    print("path planning finished.")



def find_next_step(position):
    is_stuck = True
    min_cost = INF
    next_position = position
    neighbor_positions = get_neighbors(position)

    for neighbor_position in neighbor_positions:
        if not (0 <= neighbor_position.x <= (MAP_HEIGHT - 1) and 0 <= neighbor_position.y <= (MAP_WIDTH - 1)):
            continue
        elif prob_map[neighbor_position].occupancy != INF and not prob_map[neighbor_position].isVisited:
            if prob_map[neighbor_position].cost < min_cost:
                min_cost = prob_map[neighbor_position].cost
                next_position = neighbor_position
                is_stuck = False

    if is_stuck:
        corner_escape(position)
    else:
        prob_map[next_position].isVisited = True
        prob_map[next_position].visitedNum += 1
        optimal_path.append(next_position)


def complete_coverage_path_planning(start_position):
    wave_front_spread(start_position)
    prob_map[start_position].isVisited = True
    prob_map[start_position].visitedNum += 1
    optimal_path.append(start_position)
    curr_position = start_position

    while not isPlanningFinished:
        find_next_step(curr_position)
        curr_position = optimal_path[-1]


def main():
    global prob_map, candidate_positions, optimal_path, shortcut_candidate_positions, sub_path, isExitFound, isPlanningFinished
    prob_map = {Position2D(i, j): MapPoint() for i in range(MAP_WIDTH) for j in range(MAP_HEIGHT)}

    # Build a simple map
    for i in range(MAP_WIDTH):
        for j in range(MAP_HEIGHT):
            if i != 0 and i != (MAP_WIDTH - 1) and j != 0 and j != (MAP_HEIGHT - 1):
                prob_map[Position2D(i, j)].occupancy = 1.0
            else:
                prob_map[Position2D(i, j)].occupancy = INF
                prob_map[Position2D(i, j)].cost = INF

    for i in range(40, 90):
        for j in range(40, 90):
            if i == 40 or i == 89 or j == 89:
                prob_map[Position2D(i, j)].occupancy = INF
                prob_map[Position2D(i, j)].cost = INF

    start = Position2D(41, 88)
    complete_coverage_path_planning(start)

    print("\n\n")

    cost_map = [[prob_map[Position2D(i, j)].cost * 1.2 if i != 0 and i != (MAP_HEIGHT - 1) and j != 0 and j != (MAP_WIDTH - 1) else 255.0 for i in range(MAP_WIDTH)] for j in range(MAP_HEIGHT)]
    for i in range(40, 90):
        for j in range(40, 90):
            if i == 40 or i == 89 or j == 89:
                cost_map[j][i] = 255.0

    cost_map = cv2.applyColorMap(cv2.convertScaleAbs(cost_map), cv2.COLORMAP_RAINBOW)
    cv2.imshow("cost map", cost_map)
    cv2.waitKey(0)

    map_image = [[(255.0, 255.0, 255.0) if i != 0 and i != (MAP_HEIGHT - 1) and j != 0 and j != (MAP_WIDTH - 1) else (0.0, 0.0, 0.0) for i in range(MAP_WIDTH)] for j in range(MAP_HEIGHT)]
    for i in range(40, 90):
        for j in range(40, 90):
            if i == 40 or i == 89 or j == 89:
                map_image[j][i] = (0.0, 0.0, 0.0)
    for position in optimal_path:
        map_image[position.y][position.x] = (0.0, 0.0, 255.0)

    cv2.imshow("trajectory", cv2.convertScaleAbs(map_image))
    cv2.waitKey(0)

    hotmap = [[51.0 * prob_map[Position2D(i, j)].visitedNum if i != 0 and i != (MAP_HEIGHT - 1) and j != 0 and j != (MAP_WIDTH - 1) else 0.0 for i in range(MAP_WIDTH)] for j in range(MAP_HEIGHT)]
    hotmap = cv2.applyColorMap(cv2.convertScaleAbs(hotmap), cv2.COLORMAP_HOT)
    cv2.imshow("hotmap", hotmap)
    cv2.waitKey(0)

