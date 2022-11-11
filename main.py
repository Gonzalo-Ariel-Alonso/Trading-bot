import testing_strategy
import real_time_data
def main():
    
    print('Pick an option:')
    print('1 - Test hard coded strategy:')
    print('2 - Test multyple variables strategy:')
    print('3 - Get real time data')
    print('4 - Run script')
    
    option = input()

    if option == '1':
        testing_strategy.test_strategy()
    elif option == '2':
        testing_strategy.test_strategy_with_multiples_variables()
    elif option == '3':
        print(real_time_data.get_last_5m_candle())
    elif option == '4':
        real_time_data.fill_data_base_real_time()

main()