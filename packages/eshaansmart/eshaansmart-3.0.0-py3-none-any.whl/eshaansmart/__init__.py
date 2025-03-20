import random
from tkinter import *

def is_touching(x1, y1, w1, h1, x2, y2, w2, h2) -> bool:
    return not (x1 + w1 <= x2 or  # Object 1 is completely left of Object 2
                x1 >= x2 + w2 or  # Object 1 is completely right of Object 2
                y1 + h1 <= y2 or  # Object 1 is completely above Object 2
                y1 >= y2 + h2)  # Object 1 is completely below Object 2


class Task:
    def __init__(self, go_to, recieve):
        self.go_to = go_to
        self.recieve = recieve
        self.completed = False

    def complete(self):
        self.completed = True


class TaskGroup:
    def __init__(self):
        self.tasks = []

    def append_task(self, new_task):
        self.tasks.append(new_task)


class Tile:  # not much usage, ok to remove (safely)
    def __init__(self):
        self.occupied = False

    def occupy(self):
        self.occupied = True


class TileGroup:
    def __init__(self, columns, rows):
        self.tiles = {}

    def append_tile(self, tile, row, column):
        if row not in self.tiles:
            self.tiles[row] = {}
        if column not in self.tiles[row]:
            self.tiles[row][column] = tile

# Player class


class Player:
    def __init__(self, image, row, column, canvas, tile_group):
        self.inventory = []
        self.pos = (row, column)
        self.x, self.y = self.calculate_pos()
        self.PhotoImage = PhotoImage(file=image)
        self.id = canvas.create_image(self.x, self.y, anchor=NW, image=self.PhotoImage)
        self.canvas = canvas
        self.moving = (False, None)
        self.target_row, self.target_column = None, None
        self.tile_group = tile_group
        self.check_for_pick_up()
        self.update_inventory()

    def calculate_pos(self) -> tuple:
        row = self.pos[0]
        column = self.pos[1]
        squaresize = square[1][0]  # Assuming square is a global or class variable
        return squaresize * column, squaresize * row

    def update_inventory(self):
        self.glide(self.pos[0], self.pos[1])
        self.canvas.after(100, self.update_inventory)

    def move(self, x, y, plusminus=False):
        if plusminus:
            self.x += x
            self.y += y
        else:
            self.x = x
            self.y = y
        self.canvas.coords(self.id, self.x, self.y)

        counter = 1
        for item in self.inventory:  # for showing the inventory
            item.canvas.coords(item.id, self.x + (15 * counter), self.y)
            item.x = self.x + (15 * counter)
            item.y = self.y
            counter += 1

    def check_for_pick_up(self):  # to check for objects on the ground
        for item in groundfoods[::]:
            if is_touching(self.x, self.y, square[1][0], square[1][0],
                           item.x, item.y, item.height, item.height) and len(self.inventory) < 4:
                self.inventory.append(item)
                self.canvas.tag_raise(item.id)
                groundfoods.remove(item)
                print("I am picking up item")
        for item in self.inventory[:]:
            self.canvas.tag_raise(item.id)
        self.canvas.tag_raise(self.id)
        self.canvas.after(100, self.check_for_pick_up)

    def glide(self, row, column):
        if (row >= 0 and row < 8 and column >= 0 and column < 12) or isinstance(self, Worker):
            self.moving = (True, (row, column))
            self.target_row, self.target_column = self.moving[1]
            self._glide_step()

    def _glide_step(self):
        row = self.pos[0]
        column = self.pos[1]

        # Move towards the target position (row and column)
        if row < self.target_row:
            row += 1
        elif row > self.target_row:
            row -= 1

        if column < self.target_column:
            column += 1
        elif column > self.target_column:
            column -= 1

        # Correct position before moving
        self.pos = (row, column)  # Correctly update the position
        calculated = self.calculate_pos()
        self.move(calculated[0], calculated[1], plusminus=False)

        # Continue moving if the target position hasn't been reached
        if row != self.target_row or column != self.target_column:
            self.canvas.after(100, self._glide_step)
        else:
            self.moving = (False, None)
            # Ensure worker is exactly at target position without any offset
            self.pos = (self.target_row, self.target_column)
            self.move(self.calculate_pos()[0], self.calculate_pos()[1], plusminus=False)

    def bind(self, tk_window):
        tk_window.bind("<Up>", (lambda _: self.glide(self.pos[0] - 1, self.pos[1])))
        tk_window.bind("<Down>", (lambda _: self.glide(self.pos[0] + 1, self.pos[1])))
        tk_window.bind("<Left>", (lambda _: self.glide(self.pos[0], self.pos[1] - 1)))
        tk_window.bind("<Right>", (lambda _: self.glide(self.pos[0], self.pos[1] + 1)))
        tk_window.bind("w", (lambda _: self.glide(self.pos[0] - 1, self.pos[1])))
        tk_window.bind("s", (lambda _: self.glide(self.pos[0] + 1, self.pos[1])))
        tk_window.bind("a", (lambda _: self.glide(self.pos[0], self.pos[1] - 1)))
        tk_window.bind("d", (lambda _: self.glide(self.pos[0], self.pos[1] + 1)))
        # bind keys

class Customer:
    def __init__(self, row, column, image, canvas, reciever, speed):
        self.pos = (row, column)
        self.x, self.y = calc(row, column)
        self.PhotoImage = PhotoImage(file=image)
        self.canvas = canvas
        self.speed = speed
        self.id = canvas.create_image(self.x, self.y, anchor=NW, image=self.PhotoImage)
        self.reciever = reciever
        self.inventory = []
        self.stage = random.choice(["row", "column"])
        self.advance()

    def exit_advance(self):
        if self.pos != (0, 0):
            trow, tcolumn = (0, 0)
            row, column = self.pos
            if row < trow:
                row += 1
            if row > trow:
                row -= 1
            if column > tcolumn:
                column -= 1
            if column < tcolumn:
                column += 1

            self.pos = row, column
            self.coords(calc(row, column)[0], calc(row, column)[1])
            self.canvas.after(750, self.exit_advance)
        else:
            customers.remove(self)
            self.canvas.delete(self.id)
            del self

    def cash_register_advance(self) -> None:
        global money
        if self.pos != register.pos:
            trow, tcolumn = register.pos
            row, column = self.pos
            if row < trow:
                row += 1
            if row > trow:
                row -= 1
            if column > tcolumn:
                column -= 1
            if column < tcolumn:
                column += 1

            self.pos = row, column
            self.coords(calc(row, column)[0], calc(row, column)[1])
            self.canvas.after(750, self.cash_register_advance)
        else:
            print("money given")
            addition = 0
            for item in self.inventory:
                addition += 4.50
            money += addition
            register.cashout()
            self.canvas.after(0, self.exit_advance())

    def complete(self):
        global money
        removed = []
        counter = random.choice([1, 2, 2, 3, 4])
        number = counter + 0

        # Check if the receiver has the items to give
        if self.reciever.inventory:  # If there are items to give
            # Process taking items from the receiver's inventory

            # Move the items to the customer's inventory
            for i in range(number):
                try:
                    self.inventory.append(self.reciever.inventory.pop())
                except IndexError:
                    pass

            print("Customer has received the items!")
            self.stage = "done"  # Set the task to done
            self.cash_register_advance()

        else:
            # Wait for restocking, the customer will stay at the receiver and keep checking
            print("Waiting for restock...")
            self.canvas.after(1000, self.complete)  # Keep checking every 1 second

    def coords(self, x, y):
        self.canvas.coords(self.id, x, y)
        counter = 1
        for item in self.inventory:
            item.canvas.coords(item.id, x + 15 * counter, y)  # Position the food above the customer
            item.x = x + 15 * counter
            item.y = y
            counter += 1
        self.canvas.tag_raise(self.id)

    def advance(self, finishing=False, target_row=100, target_column=100):
        global money
        if target_row == 100:
            target_row = self.reciever.pos[0]
        if target_column == 100:
            target_column = self.reciever.pos[1]
        current_row, current_column = self.pos

        if self.stage == "row":
            if current_row < target_row:
                current_row += 1
            elif current_row > target_row:
                current_row -= 1
            else:
                if is_touching(self.x, self.y, 76, 76, calc(target_row, target_column)[0],
                               calc(target_row, target_column)[1], 76, 76):
                    self.stage = "done"
                else:
                    self.stage = "column"

        if self.stage == "column":
            if current_column < target_column:
                current_column += 1
            elif current_column > target_column:
                current_column -= 1
            else:
                if is_touching(self.x, self.y, 76, 76, calc(target_row, target_column)[0],
                               calc(target_row, target_column)[1], 76, 76):
                    self.stage = "done"
                else:
                    self.stage = "row"

        # lostness
        if random.choice([True, True, False, False, False, False, False]):
            movement = random.choice(
                ["current_row += 1", "current_column += 1", "current_row -= 1", "current_column -= 1"])

            # Reverse movement if out of bounds
            if movement == "current_row += 1":
                current_row += 1
                if current_row > 12:
                    current_row -= 2  # Reverse the movement if out of bounds
            elif movement == "current_row -= 1":
                current_row -= 1
                if current_row < 0:
                    current_row += 2  # Reverse the movement if out of bounds
            elif movement == "current_column += 1":
                current_column += 1
                if current_column > 7:
                    current_column -= 2  # Reverse the movement if out of bounds
            elif movement == "current_column -= 1":
                current_column -= 1
                if current_column < 0:
                    current_column += 2  # Reverse the movement if out of bounds

        self.pos = (current_row, current_column)

        if self.stage != "done":
            if not finishing:
                self.pos = (current_row, current_column)
                self.x, self.y = calc(current_row, current_column)
                self.coords(self.x, self.y)
            self.canvas.after(self.speed, self.advance)
        else:
            self.complete()

class FoodItem:
    def __init__(self, icon, canvas, x, y, height):
        self.x = x
        self.y = y
        self.height = height
        self.image_file = icon
        self.PhotoImage = PhotoImage(file=icon)
        self.canvas = canvas
        self.id = canvas.create_image(self.x, self.y, anchor=NW, image=self.PhotoImage)
        self.pickup_able = True

    def move(self, x, y, plusminus=False):
        if plusminus:
            self.x += x
            self.y += y
        else:
            self.x = x
            self.y = y
        self.canvas.coords(self.id, self.x, self.y)


def calc(row, column) -> tuple:
    return (row * square[1][0], column * square[1][1])


class CashRegister:
    def __init__(self, imagefile, row, column, canvas, cashierfile):
        self.imagefile = imagefile
        self.pos = (row, column)
        self.canvas = canvas
        self.PhotoImage = PhotoImage(file=imagefile)
        self.id = canvas.create_image(calc(row, column)[0], calc(row, column)[1], anchor=NW, image=self.PhotoImage)
        self.cashier_imagefile = cashierfile
        self.cashier_PhotoImage = PhotoImage(file=self.cashier_imagefile)
        self.cashier_id = canvas.create_image(calc(row + 1, column)[0], calc(row + 1, column)[1], anchor=NW,
                                              image=self.cashier_PhotoImage)
        self.money_fade_level = 10
        self.money_PhotoImage = PhotoImage(file="assets/money.png")
        self.money_id = None

    def cashout(self, restart=True):
        if self.money_fade_level == 10 or restart:
            self.money_id = self.canvas.create_image(calc(self.pos[0], self.pos[1])[0] + 15,
                                                     calc(self.pos[0], self.pos[1])[1], anchor=NW,
                                                     image=self.money_PhotoImage)
            self.money_fade_level = 9
            self.canvas.after(250, (lambda: self.cashout(False)))
        else:
            self.canvas.move(self.money_id, 0, -self.money_fade_level)
            self.money_fade_level -= 1
            if self.money_fade_level != -1:
                self.canvas.after(250, (lambda: self.cashout(False)))
            else:
                self.canvas.delete(self.money_id)
                self.money_id = None

class PlayerReceiver:
    def __init__(self, row, column, image_file, canvas, image_to_get):
        self.pos = (row, column)
        self.image = image_file
        self.PhotoImage = PhotoImage(file=image_file)
        print("Exists photoimage")
        self.canvas = canvas
        self.image_to_get = image_to_get
        self.inventory = []
        self.id = canvas.create_image(calc(row, column)[0], calc(row, column)[1], anchor=NW, image=self.PhotoImage)
        print("player reciever exists")
        self.canvas.coords(self.id, calc(row, column)[0], calc(row, column)[1])
        self.canvas.update()
        self.check_for_players()
        self.canvas.tag_raise(self.id)

    def check_for_players(self):
        for player in players[:]:
            for item in player.inventory[:]:
                if item.image_file == self.image_to_get and len(self.inventory) < 12 and is_touching(player.x, player.y,
                                                                                                     75, 75,
                                                                                                     calc(self.pos[0],
                                                                                                          self.pos[1])[
                                                                                                         0],
                                                                                                     calc(self.pos[0],
                                                                                                          self.pos[1])[
                                                                                                         1], 75, 75):
                    player.inventory.remove(item)
                    self.inventory.append(item)
                    print("added to inventory of reciever")
                    print(self.inventory)

        for index, item in enumerate(self.inventory):
            row_offset = index // 4
            col_offset = index % 4
            item_x = self.pos[0] * square[1][0] + (15 * col_offset)
            item_y = self.pos[1] * square[1][1] + (15 * row_offset)
            item.canvas.coords(item.id, item_x, item_y)
            item.x = item_x
            item.y = item_y

        self.canvas.after(100, self.check_for_players)


class TrashCan:
    def __init__(self, image, row, column, canvas):
        self.pos = (row, column)
        self.imagefile = image
        self.PhotoImage = PhotoImage(file=image)
        self.canvas = canvas
        self.id = canvas.create_image(calc(row, column)[0], calc(row, column)[1], anchor=NW, image=self.PhotoImage)
        self.check_for_players()

    def check_for_players(self):
        for player in players:
            if is_touching(player.x, player.y, 75, 75, calc(self.pos[0], self.pos[1])[0],
                           calc(self.pos[0], self.pos[1])[1], 75, 75):
                for item in player.inventory:
                    item.canvas.delete(item.id)
                player.inventory.clear()
        self.canvas.after(100, self.check_for_players)


class PlayerGiver:
    def __init__(self, image, row, column, canvas, imagefile_togive, producing_time):
        self.pos = (row, column)
        self.image_file = image
        self.PhotoImage = PhotoImage(file=image)
        self.canvas = canvas
        self.imagefile_togive = imagefile_togive
        self.id = canvas.create_image(calc(row, column)[0], calc(row, column)[1], anchor=NW, image=self.PhotoImage)
        self.canvas.update()
        self.producing_time = producing_time
        self.counter = 0
        self.give()

    def give(self):
        current_food = [food for food in groundfoods if food.image_file == self.imagefile_togive]
        if len(current_food) < 3:
            item = FoodItem(self.imagefile_togive, self.canvas, calc(self.pos[0], self.pos[1])[0] + (15 * self.counter),
                            calc(self.pos[0], self.pos[1])[1], 40)
            groundfoods.append(item)
            self.counter += 1
            if self.counter == 3:
                self.counter = 0
        self.canvas.after(self.producing_time, self.give)


class Worker(Player):
    def __init__(self, image, row, column, canvas, tile_group, tree, stand, home):
        super().__init__(image, row, column, canvas, tile_group)
        self.tree = tree
        self.stand = stand
        self.go()
        self.check_for_foods()
        self.home = home

    def go(self) -> None:
        if True:
            self.pathfind(self.tree.pos[1], self.tree.pos[0])
            print("Gliding to tree at", self.tree.pos[0], self.tree.pos[1])
            self.canvas.after(
                1000 * self.calculate_distance(self.pos[0], self.pos[1], self.tree.pos[0], self.tree.pos[1]),
                self.wait_at_tree)
            print(self.pos)

    def wait_at_tree(self):
        print("Waited at tree, going to stand at", self.stand.pos[0], self.stand.pos[1])
        self.pathfind(self.stand.pos[1], self.stand.pos[0])
        self.canvas.after(
            1000 * self.calculate_distance(self.pos[0], self.pos[1], self.stand.pos[0], self.stand.pos[1]),
            self.wait_at_stand)
        print(self.pos)

    def wait_at_stand(self):
        print("Waited at stand, going home to 0,0")
        self.pathfind(self.home[0], self.home[1])
        self.canvas.after(1000 * self.calculate_distance(self.pos[0], self.pos[1], 0, 0), self.go)
        print(self.pos)

    def calculate_distance(self, start_row, start_column, end_row, end_column) -> int:
        return abs(end_row - start_row) + abs(end_column - start_column)

    def pathfind(self, target_row, target_column):
        path = self.find_path(self.pos[0], self.pos[1], target_row, target_column)
        if path:
            self.follow_path(path)

    def find_path(self, start_row, start_column, target_row, target_column):
        queue = [(start_row, start_column, [])]
        visited = set()

        while queue:
            current_row, current_column, path = queue.pop(0)

            if (current_row, current_column) == (target_row, target_column):
                return path

            visited.add((current_row, current_column))

            neighbors = self.get_neighbors(current_row, current_column)
            for neighbor_row, neighbor_column in neighbors:
                if (neighbor_row, neighbor_column) not in visited:
                    queue.append((neighbor_row, neighbor_column, path + [(neighbor_row, neighbor_column)]))

        return None

    def get_neighbors(self, row, column):
        neighbors = []
        possible_moves = [(row - 1, column), (row + 1, column), (row, column - 1), (row, column + 1)]

        for r, c in possible_moves:
            if 0 <= r < grid_squares[1][0] and 0 <= c < grid_squares[1][1]:
                neighbors.append((r, c))

        return neighbors

    def check_for_foods(self):
        for item in self.inventory[:]:
            if item.image_file != self.tree.imagefile_togive:
                groundfoods.append(item)
                self.inventory.remove(item)
        self.canvas.after(100, self.check_for_foods)

    def follow_path(self, path):
        if path:
            self.move_along_path(path, 1)

    def move_along_path(self, path, step):
        if step < len(path):
            next_row, next_column = path[step]
            self.glide(next_row, next_column)
            self.canvas.after(500, lambda: self.move_along_path(path, step + 1))


class Obj:
    pass


# Grid settings
grid = ("607x910", (607, 910))
original_width, original_height = grid[1]
grid_squares = ("8x12", (8, 12))
square = ("75.875x75.875", (75.875, 75.875))

group = TileGroup(grid_squares[1][0], grid_squares[1][1])
for i in range(0, grid_squares[1][0]):
    for j in range(0, grid_squares[1][1]):
        group.append_tile(Tile(), i, j)

# Setup the game
gameboard = Tk()
gameboard.title("Eshaan's Mart")
gridimage = PhotoImage(file="assets/grid.png")

gamecanvas = Canvas(gameboard, height=607, width=910)
gamecanvas.pack(fill=BOTH, expand=True)
gamecanvas.create_image(0, 0, anchor=NW, image=gridimage)

iconimg = PhotoImage(file="assets/app-icon.png")
gameboard.iconphoto(False, iconimg)

# gameboard.resizable(False, False)

groundfoods = []
players = []
stands = []
plants = []
customers = []

money = 10

money_text = gamecanvas.create_text(900, 10, text=f"${money:.2f}", fill="black", font=("Avenir", 22), anchor=NE)

def update_money():
    gamecanvas.itemconfigure(money_text, text=f"${money:.2f}")
    gamecanvas.after(500, update_money)

update_money()
apple_stand = None
apple_tree = None
worker1 = None

def random_customer():
    if len(customers) < 5:
        customer = Customer(0, 0, "assets/customer.png", gamecanvas, random.choice(stands), 500)
        customers.append(customer)
    gamecanvas.after(12000, random_customer)


register = CashRegister("assets/cash-register.png", 8, 3, gamecanvas, "assets/worker.png")

bob = True

orange_tree = None
orange_stand = None
watermelon_tree = None
watermelon_stand = None

if __name__=='__main__':
    banana_stand = PlayerReceiver(5, 1, "assets/banana-stand.png", gamecanvas, "assets/banana.png")
    stands.append(banana_stand)

    banana_tree = PlayerGiver("assets/banana-tree.png", 5, 5, gamecanvas, "assets/banana.png", 5000)
    plants.append(banana_tree)

    def sixth_checking():
        global watermelon_tree, watermelon_stand
        if money >= 95:
            thing = Obj()
            thing.pos = (10, 1)
            thing2 = Obj()
            thing2.pos = (7, 0)
            thing2.imagefile_togive = "assets/orange.png"
            worker3 = Worker("assets/worker.png", 5, 5, gamecanvas, group, thing2, thing, (7, 7))
            players.append(worker3)
        else:
            gameboard.after(100, sixth_checking)

    def fifth_checking():
        global watermelon_tree, watermelon_stand
        if money >= 80:
            watermelon_tree = PlayerGiver("assets/watermelon-tree.png", 2, 2, gamecanvas, "assets/watermelon.png", 5000)
            watermelon_stand = PlayerReceiver(4, 2, "assets/watermelon-stand.png", gamecanvas, "assets/watermelon.png")
            stands.append(watermelon_stand)
            plants.append(watermelon_tree)
            sixth_checking()
        else:
            gameboard.after(100, fifth_checking)

    def fourth_checking():
        if money >= 65:
            thing = Obj()
            thing.pos = (11, 5)
            worker2 = Worker("assets/worker.png", 7, 7, gamecanvas, group, apple_tree, thing, (4, 4))
            players.append(worker2)
            fifth_checking()
        else:
            gameboard.after(100, fourth_checking)


    def third_checking():
        global orange_tree, orange_stand
        if money >= 50:
            orange_tree = PlayerGiver("assets/orange-tree.png", 7, 1, gamecanvas, "assets/orange.png", 5000)
            orange_stand = PlayerReceiver(9, 1, "assets/orange-stand.png", gamecanvas, "assets/orange.png")
            stands.append(orange_stand)
            plants.append(orange_tree)
            fourth_checking()
        else:
            gameboard.after(100, third_checking)


    def second_checking():
        global worker1
        if money >= 35:
            thing = Obj()
            thing.pos = (5, 0)
            worker1 = Worker("assets/worker.png", 0, 0, gamecanvas, group, banana_tree, thing, (3, 3))
            players.append(worker1)
            third_checking()
        else:
            gamecanvas.after(100, second_checking)


    def checking():
        global apple_stand, apple_tree
        if money >= 20:
            apple_stand = PlayerReceiver(10, 5, "assets/apple-stand.png", gamecanvas, "assets/apple.png")
            stands.append(apple_stand)

            apple_tree = PlayerGiver("assets/apple-tree.png", 3, 5, gamecanvas, "assets/apple.png", 5000)
            plants.append(apple_tree)
            second_checking()
        else:
            gamecanvas.after(100, checking)


    checking()

    trash = TrashCan("assets/trash.png", 1, 5, gamecanvas)

    gameboard.after(15000, random_customer)

    myguy = Player("assets/monkey.png", 0, 0, gamecanvas, group)
    myguy.bind(gameboard)
    players.append(myguy)

    gamecanvas.update()

    gameboard.update()
    gameboard.update_idletasks()
    gameboard.mainloop()

def play():
    global trash
    banana_stand = PlayerReceiver(5, 1, "assets/banana-stand.png", gamecanvas, "assets/banana.png")
    stands.append(banana_stand)

    banana_tree = PlayerGiver("assets/banana-tree.png", 5, 5, gamecanvas, "assets/banana.png", 5000)
    plants.append(banana_tree)

    def sixth_checking():
        global watermelon_tree, watermelon_stand
        if money >= 95:
            thing = Obj()
            thing.pos = (10, 1)
            thing2 = Obj()
            thing2.pos = (7, 0)
            thing2.imagefile_togive = "assets/orange.png"
            worker3 = Worker("assets/worker.png", 5, 5, gamecanvas, group, thing2, thing, (7, 7))
            players.append(worker3)
        else:
            gameboard.after(100, sixth_checking)

    def fifth_checking():
        global watermelon_tree, watermelon_stand
        if money >= 80:
            watermelon_tree = PlayerGiver("assets/watermelon-tree.png", 2, 2, gamecanvas, "assets/watermelon.png", 5000)
            watermelon_stand = PlayerReceiver(4, 2, "assets/watermelon-stand.png", gamecanvas, "assets/watermelon.png")
            stands.append(watermelon_stand)
            plants.append(watermelon_tree)
            sixth_checking()
        else:
            gameboard.after(100, fifth_checking)

    def fourth_checking():
        if money >= 65:
            thing = Obj()
            thing.pos = (11, 5)
            worker2 = Worker("assets/worker.png", 7, 7, gamecanvas, group, apple_tree, thing, (4, 4))
            players.append(worker2)
            fifth_checking()
        else:
            gameboard.after(100, fourth_checking)


    def third_checking():
        global orange_tree, orange_stand
        if money >= 50:
            orange_tree = PlayerGiver("assets/orange-tree.png", 7, 1, gamecanvas, "assets/orange.png", 5000)
            orange_stand = PlayerReceiver(9, 1, "assets/orange-stand.png", gamecanvas, "assets/orange.png")
            stands.append(orange_stand)
            plants.append(orange_tree)
            fourth_checking()
        else:
            gameboard.after(100, third_checking)


    def second_checking():
        global worker1
        if money >= 35:
            thing = Obj()
            thing.pos = (5, 0)
            worker1 = Worker("assets/worker.png", 0, 0, gamecanvas, group, banana_tree, thing, (3, 3))
            players.append(worker1)
            third_checking()
        else:
            gamecanvas.after(100, second_checking)


    def checking():
        global apple_stand, apple_tree
        if money >= 20:
            apple_stand = PlayerReceiver(10, 5, "assets/apple-stand.png", gamecanvas, "assets/apple.png")
            stands.append(apple_stand)

            apple_tree = PlayerGiver("assets/apple-tree.png", 3, 5, gamecanvas, "assets/apple.png", 5000)
            plants.append(apple_tree)
            second_checking()
        else:
            gamecanvas.after(100, checking)


    checking()

    trash = TrashCan("assets/trash.png", 1, 5, gamecanvas)

    gameboard.after(15000, random_customer)

    myguy = Player("assets/monkey.png", 0, 0, gamecanvas, group)
    myguy.bind(gameboard)
    players.append(myguy)

    gamecanvas.update()

    gameboard.update()
    gameboard.update_idletasks()
    gameboard.mainloop()
