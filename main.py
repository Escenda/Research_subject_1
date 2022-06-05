import random
import numpy
from Human import Human

humans = []
results = []

min_human = 5
max_infected_human = 1
min_width, max_width = 0, 10
min_height, max_height = 0, 10

infected_human_wont_move = True
innocent_human_wont_move = False
heal_after_steps = 0
dead_after_steps = 0

repetition = 10000


def count_infected_humans():
    result = 0
    for human in humans:
        if human.t != "infected":
            continue
        result += 1
    return result


def prepare():
    humans.clear()
    infected_count = 0
    for _i in range(min_human):
        infect_percentage = random.uniform(0, 100)
        which_type = "infected" if infect_percentage < 50 and infected_count < max_infected_human else "innocent"
        human = Human(which_type, random.randint(min_width, max_width), random.randint(min_height, max_height),
                      min_width, max_width, min_height, max_height)
        humans.append(human)
        if which_type == "infected":
            infected_count += 1


def search_around():
    for human in humans:
        for around_human in humans:
            if around_human is human or around_human.t != "infected":
                continue
            is_x_near = (human.x + 1 == around_human.x or human.x - 1 == around_human.x)
            is_y_near = (human.y + 1 == around_human.y or human.y - 1 == around_human.y)
            if is_x_near and is_y_near:
                percentage_of_droplet = human.get_percentage_of_droplet()
                percentage_of_droplet_infection = human.get_percentage_of_droplet_infection()
                percentage_of_infection = human.get_percentage_of_infection()
                if random.uniform(0, 100) < percentage_of_droplet \
                        and random.uniform(0, 100) < percentage_of_droplet_infection \
                        and random.uniform(0, 100) < percentage_of_infection:
                    continue
                human.t = "infected"


def run():
    _ = 0
    innocent_count, infected_count = 0, 0
    is_threshold = False
    while not is_threshold:
        _ += 1
        for human in humans:
            if human.t == "infected":
                infected_count += 1
                human.step_after_infected += 1
                human.heal(heal_after_steps)
                human.dead(dead_after_steps)
            if human.t == "innocent":
                innocent_count += 1
            if human.t == "corpse":
                humans.remove(human)
            search_around()
            if (infected_human_wont_move and human.t == "infected") \
                    or (innocent_human_wont_move and human.t == "innocent"):
                continue
            x = random.randint(-1, 1)
            y = random.randint(-1, 1)
            human.move_around(x, y)
        is_threshold = (not min_human > innocent_count > 0) or (not min_human > infected_count > 0)
        innocent_count, infected_count = 0, 0
    results.append(_)
    print(f"最終到達: {_}")


if __name__ == '__main__':
    print(f"プログラムが開始されました。")
    for i in range(repetition):
        while not min_human > count_infected_humans() > 0:
            prepare()
        run()
    results.sort()
    print(f"\n試行回数: {len(results)}, 平均値: {numpy.average(results)}\n最大値: {results[-1]}, 最低値: {results[0]}")
