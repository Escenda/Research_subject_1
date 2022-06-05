import random

masks = {"なし": [100, 100],
         "不織布": [20, 30],
         "布マスク": [26, 60],
         "ウレタン": [50, 65],
         "フェイスシールド": [80, 0],
         "マウスシールド": [90, 0]}

vaccines = {"なし": 0,
            "ファイザー": 95,
            "モデルナ": 94,
            "アストラゼネカ": 70,
            "ノババックス": 90}


class Human:
    # tはHuman
    def __init__(self, t, x, y, min_width, max_width, min_height, max_height):
        self.t = t
        self.x = x
        self.y = y
        self.max_x, self.min_x = x, x
        self.max_y, self.min_y = y, y
        self.min_width, self.max_width = min_width, max_width
        self.min_height, self.max_height = min_height, max_height
        self.step_after_infected = 0
        self.mask, trash = random.choice(list(masks.items()))
        self.vaccine, trash = random.choice(list(vaccines.items()))

    def move_around(self, x, y):
        # この条件で見ている値の範囲は移動後の範囲で、self.xに+1しているのは仮に移動するとしたら、値が+1されるため。
        x_c_1 = (self.min_width <= self.x + 1 <= self.max_width and x >= 0)
        x_c_2 = (self.min_width <= self.x - 1 <= self.max_width and x <= 0)
        x_c_3 = (self.min_width + 1 <= self.x <= self.max_width - 1)
        x_conditions = (x_c_1 or x_c_2) or x_c_3
        y_c_1 = (self.min_height <= self.y + 1 <= self.max_height and y >= 0)
        y_c_2 = (self.min_height <= self.y - 1 <= self.max_height and y <= 0)
        y_c_3 = (self.min_height + 1 <= self.y <= self.max_height - 1)
        y_conditions = (y_c_1 or y_c_2) or y_c_3
        if x_conditions:
            self.x += x
            if self.max_x < self.x:
                self.max_x = self.x
            if self.min_x > self.x:
                self.min_x = self.x
        if y_conditions:
            self.y += y
            if self.max_y < self.y:
                self.max_y = self.y
            if self.min_y > self.y:
                self.min_y = self.y

    def print_max_min(self):
        print(f"X {self.max_x, self.min_x} (max, min), Y {self.max_y, self.min_y} (max, min)")

    def heal(self, heal_after_steps):
        is_threshold = 0 < heal_after_steps <= self.step_after_infected
        if is_threshold:
            self.t = "innocent"
            self.step_after_infected = 0

    def dead(self, dead_after_steps):
        is_threshold = 0 < dead_after_steps <= self.step_after_infected
        if is_threshold:
            self.t = "corpse"
            self.step_after_infected = 0

    def get_percentage_of_droplet(self):
        mask_percentage = masks.get(self.mask)[0]
        return mask_percentage

    def get_percentage_of_droplet_infection(self):
        mask_percentage = masks.get(self.mask)[1]
        return mask_percentage

    def get_percentage_of_infection(self):
        vaccine_percentage = vaccines.get(self.vaccine)
        return vaccine_percentage
