import testing_strategy
def main():
    
    print('Pick an option:')
    print('1 - Test hard coded strategy:')
    print('2 - Test multyple variables strategy:')
    
    option = input()

    if option == '1':
        testing_strategy.test_strategy()
    elif option == '2':
        testing_strategy.test_strategy_with_multiples_variables()
    
main()