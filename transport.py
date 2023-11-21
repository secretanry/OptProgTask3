# Get user input for supply
supply = list(map(int, input("Enter the supply values separated by spaces: ").split()))

# Get user input for demand
demand = list(map(int, input("Enter the demand values separated by spaces: ").split()))

# Get user input for the cost matrix
print("Input a matrix of coefficients of costs:")
grid = []
for i in range(len(supply)):
    row = list(map(int, input().split()))
    grid.append(row)


def print_input_table(supply, demand, grid):
    num_columns = len(grid[0])

    print("=" * (num_columns + 2) * 3, end="")
    print("INPUT TABLE".center((num_columns + 2) * 3), end="")
    print("=" * (num_columns + 2) * 3)

    output_row = ["*".center(8)]

    for index in range(num_columns):
        output_row.append(f"{index + 1:^8}")
    output_row.append("Supply".center(8))
    print_row(output_row)

    for index in range(len(grid)):
        output_row = [f"{index + 1:<8}"]
        for value in grid[index]:
            output_row.append(f"{value:^8}")
        output_row.append(f"{supply[index]:^8}")
        print_row(output_row)
    output_row = ["Demand".center(8)]
    for value in demand:
        output_row.append(f"{value:^8}")
    output_row.append("*".center(8))
    print_row(output_row)


def print_row(input_row):
    for value in input_row:
        print(value, end="|")
    print()
    print("-" * len(input_row) * 9)


####################################################### north_west_corner ##########################
def north_west_corner(supply, demand):
    # Initialize indices for the northwest corner of the cost matrix
    i, j = 0, 0

    # Initialize the allocation matrix with zeros
    allocation = [[0 for _ in demand] for _ in supply]

    # Loop until either supply or demand is exhausted
    while i < len(supply) and j < len(demand):
        # Determine the minimum value between the remaining supply and demand
        min_val = min(supply[i], demand[j])

        # Allocate the minimum value at the current position in the allocation matrix
        allocation[i][j] = min_val

        # Update the remaining supply and demand after allocation
        supply[i] -= min_val
        demand[j] -= min_val

        # Move to the next row if the current supply is exhausted
        if supply[i] == 0:
            i += 1
        # Move to the next column if the current demand is exhausted
        elif demand[j] == 0:
            j += 1

    total_cost = 0
    for i in range(len(allocation)):
        for j in range(len(allocation[0])):
            total_cost += allocation[i][j] * grid[i][j]

    return allocation, total_cost


print_input_table(supply, demand, grid)

# Copy the original supply and demand to avoid modifying the original data
allocation, total_cost = north_west_corner(supply.copy(), demand.copy())

# Display the result
print("North West Corner Method result:")
for row in allocation:
    print(row)

print(f"North West Corner Method | Initial Feasible Solution: {total_cost}")
print("_" * 30)


############################################ russells_approximation ################################
def russells_approximation(grid, supply, demand):
    def calculate_total_transportation_cost(solution, cost_matrix):
        total_cost = 0
        for i in range(len(solution)):
            for j in range(len(solution[0])):
                total_cost += solution[i][j] * cost_matrix[i][j]
        return total_cost

    def calculate_initial_feasible_solution(solution, cost_matrix):
        return calculate_total_transportation_cost(solution, cost_matrix)

    def print_solution(solution):
        print("Russell's Method result:")
        for row in solution:
            print(row)

    num_sources = len(supply)
    num_destinations = len(demand)

    initial_solution = [[0] * num_destinations for _ in range(num_sources)]
    while True:

        min_row_costs = [float('-inf')] * num_sources
        min_col_costs = [float('-inf')] * num_destinations
        for i in range(num_sources):
            min_cost = float('-inf')
            for j in range(num_destinations):
                if grid[i][j] > min_cost:
                    min_cost = grid[i][j]
            min_row_costs[i] = min_cost
        for j in range(num_destinations):
            min_cost = float('-inf')
            for i in range(num_sources):
                if grid[i][j] > min_cost:
                    min_cost = grid[i][j]
            min_col_costs[j] = min_cost

        max_cost = -1
        max_cost_row = -1
        max_cost_col = -1
        for i in range(num_sources):
            for j in range(num_destinations):
                cost = grid[i][j] - min_row_costs[i] - min_col_costs[j]
                if cost <= 0 and abs(cost) > max_cost and supply[i] > 0 and demand[j] > 0:
                    max_cost = abs(cost)
                    max_cost_col = j
                    max_cost_row = i

        if max_cost == -1:
            break

        allocation = min(supply[max_cost_row], demand[max_cost_col])

        supply[max_cost_row] -= allocation
        demand[max_cost_col] -= allocation

        initial_solution[max_cost_row][max_cost_col] = allocation

    print_solution(initial_solution)

    initial_feasible_solution = calculate_initial_feasible_solution(initial_solution, grid)
    print(f"Russell's Method | Initial Feasible Solution: {initial_feasible_solution}")
    print("_" * 30)


russells_approximation(grid.copy(), supply.copy(), demand.copy())

######################################## Vogel #####################################################

ans = 0
INF = 10 ** 3
n = len(grid)
m = len(grid[0])


# hepler function for finding the row difference and the column difference
def findDiff(grid):
    rowDiff = []
    colDiff = []
    for i in range(len(grid)):
        arr = grid[i][:]
        arr.sort()
        rowDiff.append(arr[1] - arr[0])
    col = 0
    while col < len(grid[0]):
        arr = []
        for i in range(len(grid)):
            arr.append(grid[i][col])
        arr.sort()
        col += 1
        colDiff.append(arr[1] - arr[0])
    return rowDiff, colDiff


def Vogel(grid, supply, demand):
    global ans
    result_vector = [[0] * len(demand) for _ in range(len(supply))]

    # loop runs until both the demand and the supply are exhausted
    while max(supply.copy()) != 0 or max(demand.copy()) != 0:
        # finding the row and col difference
        row, col = findDiff(grid.copy())
        # finding the maximum element in row difference array
        maxi1 = max(row)
        # finding the maximum element in col difference array
        maxi2 = max(col)

        try:
            # if the row diff max element is greater than or equal to col diff max element
            if maxi1 >= maxi2:
                for ind, val in enumerate(row):
                    if val == maxi1:
                        # finding the minimum element in grid index where the maximum was found in the row difference
                        mini1 = min(grid[ind])
                        for ind2, val2 in enumerate(grid[ind]):
                            if val2 == mini1:
                                # calculating the min of supply and demand in that row and col
                                mini2 = min(supply[ind], demand[ind2])
                                ans += mini2 * mini1

                                # Update the result_vector
                                result_vector[ind][ind2] = + mini2
                                # subtracting the min from the supply and demand
                                supply[ind] -= mini2
                                demand[ind2] -= mini2
                                # if demand is smaller, then the entire col is assigned max value so that the col is eliminated for the next iteration
                                if demand[ind2] == 0:
                                    for r in range(n):
                                        grid[r][ind2] = INF
                                # if supply is smaller, then the entire row is assigned max value so that the row is eliminated for the next iteration
                                else:
                                    grid[ind] = [INF for i in range(m)]
                                break
                        break
            # if the row diff max element is greater than col diff max element
            else:
                for ind, val in enumerate(col):
                    if val == maxi2:
                        # finding the minimum element in grid index where the maximum was found in the col difference
                        mini1 = INF
                        for j in range(n):
                            mini1 = min(mini1, grid[j][ind])

                        for ind2 in range(n):
                            val2 = grid[ind2][ind]
                            if val2 == mini1:
                                # calculating the min of supply and demand in that row and col
                                mini2 = min(supply[ind2], demand[ind])
                                ans += mini2 * mini1
                                result_vector[ind2][ind] = + mini2
                                # Update the result_vector

                                # subtracting the min from the supply and demand
                                supply[ind2] -= mini2
                                demand[ind] -= mini2
                                # if demand is smaller, then the entire col is assigned max value so that the col is eliminated for the next iteration
                                if demand[ind] == 0:
                                    for r in range(n):
                                        grid[r][ind] = INF
                                # if supply is smaller, then the entire row is assigned max value so that the row is eliminated for the next iteration
                                else:
                                    grid[ind2] = [INF for i in range(m)]
                                break
                        break

        except Exception as e:
            print(f"An exception occurred: {e}")
            print("The method is not applicable!")
            break

    # Print the basic feasible solution
    print("Vogel's Method result:")
    for row in result_vector:
        print(row)
    print(f"Vogel's Method | Initial Feasible Solution: {ans}")
    print("_" * 30)


Vogel(grid.copy(), supply.copy(), demand.copy())
