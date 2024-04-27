import itertools
import time

# Brute force algorithm


def brute_force_average_subsets(n):
    count = 0
    # Generate all possible subsets of the set {1, 2, ..., n}
    for i in range(2, n+1):  # Start from 2 to ensure at least two members
        for subset in itertools.combinations(range(1, n+1), i):
            if sum(subset) % len(subset) == 0:  # Check if the average is an integer
                count += 1
    return count

# More efficient algorithm


def efficient_average_subsets(n):
    # It calculates the number of subsets with an integer average with at least 2 members.
    # It uses dynamic programming to build up a table `dp` where `dp[i][j]`
    # represents the number of subsets of size `i` with sum `j`.
    # The final result is calculated by summing over all possible subset sizes and sums that have an integer average.
    # The time complexity of this code is O(n^3), which is efficient for calculating the number of subsets with an integer average.
    dp = [[0] * (n * (n + 1) // 2 + 1) for _ in range(n + 1)]
    dp[0][0] = 1

    for num in range(1, n + 1):
        for i in range(n, 0, -1):
            for j in range(n * (n + 1) // 2, num - 1, -1):
                dp[i][j] += dp[i - 1][j - num]

    total = sum(dp[i][j] for i in range(2, n + 1)
                for j in range(i, n * (n + 1) // 2 + 1) if j % i == 0)
    return total


# Compare the two algorithms on some samples up to n=30
brute_result = efficient_result = 0  # scope of these variable
for n in (3, 4, 10, 20, 30):
    start_time = time.time()
    brute_result = brute_force_average_subsets(n)
    brute_time = time.time() - start_time

    start_time = time.time()
    efficient_result = efficient_average_subsets(n)
    efficient_time = time.time() - start_time

    print(f'n={n}, Brute Force: {brute_result}, Time: {brute_time:.4f}s, '
          f'Efficient: {efficient_result}, Time: {efficient_time:.4f}s')
    if brute_result != efficient_result:
        break
# If the results are the same, calculate the result for n=100 using the most effective algorithm
if brute_result == efficient_result:
    start_time = time.time()
    final_result = efficient_average_subsets(100)
    total_time = time.time() - start_time
    print(f'Result for n=100: {final_result}, Time: {total_time:.4f}s')
