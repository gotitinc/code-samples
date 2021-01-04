import sys


def cron_do_something():
    print('doing something')


tasks = {
    'do_something': cron_do_something()
}

if __name__ == '__main__':
    number_of_arguments = len(sys.argv)

    if number_of_arguments < 2:
        print('Please choose a valid task to run:')
        print(', '.join(sorted(tasks.keys())))
    elif sys.argv[1] not in tasks:
        print('{} is not a valid task'.format(sys.argv[1]))
    else:
        task = sys.argv[1]
        tasks[task]()
        print('ran {} successfully!'.format(task))
