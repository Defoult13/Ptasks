import multiprocessing
import argparse

def calculate_column_sum(matrix, column, result_queue):
    column_sum = sum(matrix[i][column] for i in range(len(matrix)))
    result_queue.put(column_sum)

def main(args):
    num_rows = args.rows
    num_columns = args.columns
    values = args.values

    if num_rows * num_columns != len(values):
        print("The number of element values does not correspond to the size of the matrix.")
        return

    matrix = [[values[i * num_columns + j] for j in range(num_columns)] for i in range(num_rows)]

    with multiprocessing.Manager() as manager:
        result_queue = manager.Queue()
        processes = []

        for column in range(num_columns):
            process = multiprocessing.Process(target=calculate_column_sum, args=(matrix, column, result_queue))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()

        column_sums = [result_queue.get() for _ in range(num_columns)]
        total_sum = sum(column_sums)

    print(f"Matrix:")
    for row in matrix:
        print(row)
    
    print(f"Sum by columns: {column_sums}")
    print(f"Total sum: {total_sum}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculation of the sum of matrix elements with parallel processing by columns.")
    parser.add_argument("rows", type=int, help="Number of rows in the matrix")
    parser.add_argument("columns", type=int, help="Number of columns in the matrix")
    parser.add_argument("values", type=int, nargs="*", help="Values of matrix elements")
    args = parser.parse_args()
    main(args)
