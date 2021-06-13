import webbrowser


class Reversi:
    def __init__(self, name, height=8, width=8, board_color="green", two_player=True):
        self.name = name
        self.filename = name + ".html"
        self.height = height
        self.width = width
        self.two_player = two_player

        if height % 2 == 0 and width % 2 == 0:
            self.white_center = [(width // 2, height // 2), (width // 2 + 1, height // 2 + 1)]
            self.black_center = [(width // 2 + 1, height // 2),  (width // 2, height // 2 + 1)]

        if height % 2 != 0 and width % 2 == 0:
            self.white_center = [(width // 2, height // 2), (width // 2 + 1, height // 2 + 1), (width // 2, height // 2 + 2)]
            self.black_center = [(width // 2 + 1, height // 2), (width // 2, height // 2 + 1), (width // 2 + 1, height // 2 + 2)]

        if height % 2 == 0 and width % 2 != 0:
            self.white_center = [(width // 2, height // 2), (width // 2 + 1, height // 2 + 1), (width // 2 + 2, height // 2)]
            self.black_center = [(width // 2 + 1, height // 2), (width // 2, height // 2 + 1), (width // 2 + 2, height // 2 + 1)]

        if height % 2 != 0 and width % 2 != 0:
            self.white_center = [(width // 2, height // 2), (width // 2 + 1, height // 2 + 1), (width // 2 + 2, height // 2), (width // 2, height // 2 + 2), (width // 2 + 2, height // 2 + 2)]
            self.black_center = [(width // 2 + 1, height // 2), (width // 2, height // 2 + 1), (width // 2 + 2, height // 2 + 1), (width // 2 + 1, height // 2 + 2)]

        colors = {
            "blue":   "#7393B3",
            "green":  "#00CC66",
            "orange": "#F4BB44",
            "pink":    "#e75480",
            "vinay": "style=\"background-image: url('Vinay.png');\""
        }

        self.board_color = colors[board_color.lower()]

    def create_head(self, file):
        with open("texts/head.txt", "r") as head:
            for line in head:
                if "Reversi" in line:
                    line = line.replace("Reversi", self.name)
                file.write(line)

    def create_table(self, file):
        with open("texts/table1.txt", "r") as table1:
            for line in table1:
                if "Reversi" in line:
                    line = line.replace("Reversi", self.name)
                if "#00CC66" in line:
                    if self.board_color == "style=\"background-image: url('Vinay.png');\"":
                        line = line.replace("bgcolor='#00CC66'", self.board_color)
                    else:
                        line = line.replace("#00CC66", self.board_color)
                file.write(line)
            for h in range(self.height):
                file.write("\t\t<tr>\n")
                for w in range(1, + self.width + 1):
                    file.write("\t\t\t<td id=\"mark(" + str(w) + "," + str(self.height - h) + ")" + "\" width=\"60\" height=\"60\" align=\"center\" valign=\"center\" onclick=\"modbutton(this)\" style=\"cursor: pointer;\">&nbsp;</td>\n")
                file.write("\t\t</tr>\n")

        with open("texts/table2.txt", "r") as table2:
            for line in table2:
                file.write(line)

    @staticmethod
    def create_single_player(file):
        with open("texts/single_player.txt") as single_player:
            for line in single_player:
                file.write(line)

    def create_lambda(self, file):
        file.write("<textarea id='lambda' type='text/hrf' style='display:none'>\n\n")
        for i in range(1, max(self.height, self.width) + 1):
            file.write("digit(" + str(i) + ")\n")
        file.write("control(black)\n")

        indices = [(i, j) for i in range(1, self.width + 1) for j in range(1, self.height + 1)]

        for index1 in indices:
            for index2 in indices:
                if index1[0] == index2[0] and index1[1] == index2[1] + 1:
                    file.write("north(cell" + str(index1) + ", cell" + str(index2) + ")\n")
                elif index1[0] == index2[0] + 1 and index1[1] == index2[1]:
                    file.write("east(cell" + str(index1) + ", cell" + str(index2) + ")\n")
                elif index1[0] == index2[0] + 1 and index1[1] == index2[1] + 1:
                    file.write("northeast(cell" + str(index1) + ", cell" + str(index2) + ")\n")
                elif index1[0] == index2[0] - 1 and index1[1] == index2[1] + 1:
                    file.write("northwest(cell" + str(index1) + ", cell" + str(index2) + ")\n")

        for index in indices:
            if index in self.black_center:
                file.write("is(cell" + str(index) + ", black)\n")
            elif index in self.white_center:
                file.write("is(cell" + str(index) + ", white)\n")
            else:
                file.write("is(cell" + str(index) + ", blank)\n")
        file.write("\n</textarea>\n\n")

    @staticmethod
    def create_library(file):
        with open("texts/library.txt", "r") as library:
            for line in library:
                file.write(line)

    @staticmethod
    def create_foot(file):
        with open("texts/foot.txt", "r") as foot:
            for line in foot:
                file.write(line)

    def create_game(self):
        with open(self.filename, "w") as file:
            self.create_head(file)
            self.create_table(file)
            if not self.two_player:
                self.create_single_player(file)
            self.create_lambda(file)
            self.create_library(file)
            self.create_foot(file)

        webbrowser.open(self.filename)


def main():
    original = input("Original? ")
    if original.lower() in "yes":
        reversi = Reversi("Reversi")
    else:
        filename = input("Game Name: ")
        height = int(input("Board Height: "))
        width = int(input("Board Width: "))
        board_color = input("Board Color: ")
        single_player = bool(int(input("Number of Players: ")) - 1)
        reversi = Reversi(filename, height, width, board_color, single_player)

    reversi.create_game()

    
if __name__ == '__main__':
    main()
