def calculate_sum(n):
    """Calculates the sum of numbers from 0 to n."""
    total = 0
    for i in range(n + 1):
        total += i
    return total


def main():
    """Main function to run the script logic."""
    x = 10
    if x > 5:
        result = calculate_sum(x)
        # This is the final output line the test will look for
        print(f"The final result is: {result}")
    else:
        print("x was not greater than 5.")

    print("Script execution completed.")


# Execute the main function
main()
