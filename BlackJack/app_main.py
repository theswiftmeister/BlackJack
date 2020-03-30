from tkinter import *
from PIL import Image, ImageTk
import random


class Create:
    @staticmethod
    def image(master, x, y, card):
        image = Image.open(f'images/{card}.jpg')
        image = image.resize((65, 93), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(image)

        img = Label(master, image=render)
        img.image = render
        img.place(relx=x, rely=y, anchor=CENTER)
        return img

    @staticmethod
    def deck(number_of_decks=1):
        cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        spades = [f'{i}S' for i in cards]
        diamonds = [f'{i}D' for i in cards]
        clubs = [f'{i}C' for i in cards]
        hearts = [f'{i}H' for i in cards]

        return (spades + diamonds + clubs + hearts) * number_of_decks


class BlackJack:
    def __init__(self, money=2):
        self.bets = money
        self.bet_amount = 0
        self.player_hand = []
        self.player_split_hand = []
        self.dealer_hand = []
        self.dealer_hidden_card = None
        self.player_doubled = False
        self.player_splits = False
        self.split_turn = 0
        self.reset = False
        self.table_cards_list = []
        self.label_list=[]
        self.deck = Create.deck(6)

        self.main_window = Tk()
        self.main_window.title('BlackJack')
        self.main_window.geometry('800x800+550+100')
        self.main_window.maxsize(800, 800)
        self.main_window.configure(background='#212121')

        table_image = Image.open(f'images/blakjak.png')
        render_table_image = ImageTk.PhotoImage(table_image)

        tbl_img = Label(self.main_window, image=render_table_image)
        tbl_img.image = render_table_image
        tbl_img['bg'] = tbl_img.master['bg']
        tbl_img.place(relx=0.5, rely=0.4, anchor=CENTER)

        # LABELS

        chip_image = Image.open(f'images/chip_image.png')
        chip_image = chip_image.resize((50, 55), Image.ANTIALIAS)
        render_chip_image = ImageTk.PhotoImage(chip_image)

        chip_img = Label(self.main_window, image=render_chip_image)
        chip_img.image = render_chip_image
        chip_img['bg'] = '#00763a'
        chip_img.place(relx=0.505, rely=0.38, anchor=CENTER)

        self.current_bets_label = Label(self.main_window, text=f'{self.bets}')
        self.current_bets_label.config(font=('Alata', 33), bg='#00763a', fg='#451b50')
        self.current_bets_label.place(relx=0.505, rely=0.445, anchor=CENTER)

        chip_img.tkraise(self.current_bets_label)

        self.dealer_points_label = Label(self.main_window, text=f'Points:')
        self.dealer_points_label.config(font=('Alata', 15), bg='#00763a', fg='#14ffec')
        self.dealer_points_label.place(relx=0.30, rely=0.13, anchor=CENTER)

        self.label_list.append(self.dealer_points_label)

        self.player_points_label = Label(self.main_window, text=f'Points:')
        self.player_points_label.config(font=('Alata', 15), bg='#212121', fg='#14ffec')
        self.player_points_label.place(relx=0.80, rely=0.7, anchor=CENTER)

        self.label_list.append(self.player_points_label)

        self.player_split_points_label = Label(self.main_window, text='')
        self.player_split_points_label.config(font=('Alata', 15), bg='#212121', fg='#14ffec')
        self.player_split_points_label.place(relx=0.20, rely=0.7, anchor=CENTER)

        self.label_list.append(self.player_split_points_label)

        self.info_label = Label(self.main_window, text='')
        self.info_label.config(font=('Alata', 20), bg='#212121', fg='#14ffec')
        self.info_label.place(relx=0.5, rely=0.05, anchor=CENTER)

        self.label_list.append(self.info_label)


        # BET BUTTONS

        self.decrease_bet_button = Button(self.main_window, text='-',
                                          command=lambda: self.set_bet_amount('-'))
        self.decrease_bet_button.config(font=("Alata", 15), width=4, bg='#212121', fg='#14ffec',
                                        borderwidth=2, activebackground='#323232', activeforeground='#0d7377')
        self.decrease_bet_button.place(relx=0.4, rely=0.8, anchor=CENTER)

        self.bet_amount_button = Button(self.main_window, text='Bet', command=lambda: self.set_bet_amount('bet'))
        self.bet_amount_button.config(font=("Alata", 15), width=8, bg='#212121', fg='#14ffec',
                                      borderwidth=2, activebackground='#323232', activeforeground='#0d7377')
        self.bet_amount_button.place(relx=0.5, rely=0.8, anchor=CENTER)

        self.increase_bet_button = Button(self.main_window, text='+',
                                          command=lambda: self.set_bet_amount('+'))
        self.increase_bet_button.config(font=("Alata", 15), width=4, bg='#212121', fg='#14ffec',
                                        borderwidth=2, activebackground='#323232', activeforeground='#0d7377')
        self.increase_bet_button.place(relx=0.6, rely=0.8, anchor=CENTER)

        # BUTTONS
        self.hit_button = Button(self.main_window, text='Hit', command=self.hit)
        self.hit_button.config(font=("Alata", 20), width=7, bg='#212121', fg='#14ffec',
                               borderwidth=2, activebackground='#323232', activeforeground='#0d7377')
        self.hit_button.place(relx=0.20, rely=0.9, anchor=CENTER)

        self.double_button = Button(self.main_window, text='Double', command=self.double)
        self.double_button.config(font=("Alata", 20), width=7, bg='#212121', fg='#14ffec',
                                  borderwidth=2, activebackground='#323232', activeforeground='#0d7377')
        self.double_button.place(relx=0.40, rely=0.9, anchor=CENTER)

        self.split_button = Button(self.main_window, text='Split', command=self.split)
        self.split_button.config(font=("Alata", 20), width=7, bg='#212121', fg='#14ffec',
                                 borderwidth=2, activebackground='#323232', activeforeground='#0d7377')
        self.split_button.place(relx=0.60, rely=0.9, anchor=CENTER)

        self.stand_button = Button(self.main_window, text='Stand', command=self.stand)
        self.stand_button.config(font=("Alata", 20), width=7, bg='#212121', fg='#14ffec',
                                 borderwidth=2, activebackground='#323232', activeforeground='#0d7377')
        self.stand_button.place(relx=0.80, rely=0.9, anchor=CENTER)

        self.buttons = [self.hit_button, self.double_button, self.split_button, self.stand_button]

        self.button_states(self.buttons, DISABLED)

        # SHUFFLE DECK
        random.shuffle(self.deck)
        self.main_window.mainloop()

    def give_cards(self, master, hand, x, y):
        hand.append(self.deck[0])
        if hand == self.dealer_hand:
            if len(self.dealer_hand) == 1:
                self.dealer_hidden_card = Create.image(master, x, y, 'X')
                self.table_cards_list.append(self.dealer_hidden_card)
            else:
                self.table_cards_list.append(Create.image(master, x, y, self.deck[0]))
        else:
            self.table_cards_list.append(Create.image(master, x, y, self.deck[0]))

        self.deck.remove(self.deck[0])
        if hand == self.player_hand:
            self.player_points_label['text'] = f'Points: {self.scoring_hand(self.player_hand)}'
        else:
            self.dealer_points_label['text'] = f'Points: {self.scoring_hand(hand[1:])}'

    def hit(self):
        if not self.player_splits:
            self.give_cards(self.main_window, self.player_hand, 0.505 + (len(self.player_hand) * 0.02),
                            0.58 - (len(self.player_hand) * 0.02))
            self.hit_lose_condition(self.player_hand, 'Player Busted, Dealer Wins')

        else:
            if self.split_turn == 1:
                self.give_cards(self.main_window, self.player_hand, 0.55 + (len(self.player_hand) * 0.02),
                                0.58 - (len(self.player_hand) * 0.02))
                self.hit_lose_condition(self.player_hand, 'Hand 1 Busted, Hand 2 turn')
            elif self.split_turn == 2:
                self.give_cards(self.main_window, self.player_split_hand, 0.45 - (len(self.player_split_hand) * 0.02),
                                0.58 - (len(self.player_split_hand) * 0.02))
                self.player_split_points_label['text'] = f'Points: {self.scoring_hand(self.player_split_hand)}'
                self.hit_lose_condition(self.player_split_hand, 'Hand 2 Busted')

        self.split_button['state'] = DISABLED
        self.double_button['state'] = DISABLED

    def double(self):
        self.give_cards(self.main_window, self.player_hand, 0.505 + (len(self.player_hand) * 0.02),
                        0.58 - (len(self.player_hand) * 0.02))
        if self.convert_score(self.player_hand) > 21:
            self.info_label['text'] = 'Player Busted, Dealer Wins'
            self.return_bets_amount(2, 'lose')
        else:
            self.player_doubled = True
            self.stand()

    def split(self):
        self.split_button['state'] = DISABLED
        self.double_button['state'] = DISABLED
        self.player_splits = True
        self.split_turn = 1
        self.table_cards_list[0].place(relx=0.55, rely=0.58, anchor=CENTER)
        self.table_cards_list[2].place(relx=0.45, rely=0.58, anchor=CENTER)
        self.player_split_hand.append(self.player_hand[1])
        self.player_hand.remove(self.player_hand[1])
        self.player_split_points_label['text'] = f'Points: {self.scoring_hand(self.player_split_hand)}'
        self.info_label['text'] = 'Hand 1 turn'

    def stand(self):
        if self.player_splits:
            if self.split_turn == 1:
                self.split_turn = 2
                self.info_label['text'] = 'Hand 2 turn'
            elif self.split_turn == 2:
                res = self.on_splitting_condition(self.player_hand, self.player_split_hand)
                if res.count(0) == 2:
                    self.return_bets_amount(1, 'lose')
                elif res.count(1) == 2:
                    self.return_bets_amount(0, 'tie')
                else:
                    self.return_bets_amount(res.count(2), 'win')

                self.split_turn = 0
                self.player_splits = False
                self.player_split_hand.clear()
        else:
            self.dealer_hidden_card.destroy()
            self.dealer_hidden_card = Create.image(self.main_window, 0.505, 0.17, self.dealer_hand[0])
            self.dealer_hidden_card.lower(self.table_cards_list[0])
            self.table_cards_list.append(self.dealer_hidden_card)

            self.dealer_points_label['text'] = f'Points: {self.scoring_hand(self.dealer_hand)}'
            while self.convert_score(self.dealer_hand) < 16 or self.convert_score(
                    self.dealer_hand) < self.convert_score(self.player_hand):
                self.give_cards(self.main_window, self.dealer_hand, 0.505 + (len(self.dealer_hand) * 0.02),
                                0.17 + (len(self.dealer_hand) * 0.02))
                self.dealer_points_label['text'] = f'Points: {self.scoring_hand(self.dealer_hand)}'

            if self.convert_score(self.dealer_hand) > self.convert_score(self.player_hand) and self.convert_score(
                    self.dealer_hand) <= 21:
                self.info_label['text'] = 'Dealer Wins'
                if self.player_doubled:
                    self.return_bets_amount(2, 'lose')
                else:
                    self.return_bets_amount(1, 'lose')
            elif self.convert_score(self.dealer_hand) == self.convert_score(self.player_hand):
                if len(self.player_hand) > 0:
                    self.info_label['text'] = 'Tie/Push'
                    self.return_bets_amount(0, 'tie')
            else:
                self.info_label['text'] = 'Player Wins'
                if self.player_doubled:
                    self.return_bets_amount(2, 'win')
                else:
                    self.return_bets_amount(1, 'win')

        self.player_doubled = False

    def set_bet_amount(self, action):

        if action == '+':
            if self.bet_amount < self.bets:
                self.bet_amount += 1
        elif action == '-':
            if self.bet_amount > 0:
                self.bet_amount -= 1
        elif action == 'bet':
            self.info_label['text'] = ''
            if self.reset:
                # RESET VALUES
                self.player_split_points_label['text'] = ''
                for cards in self.table_cards_list:
                    cards.destroy()
                self.table_cards_list.clear()
                self.dealer_hand.clear()
                self.player_hand.clear()
                self.split_turn = 0
                self.player_splits = False
                self.reset = False

            if self.bet_amount > 0:
                self.button_states([self.bet_amount_button, self.increase_bet_button, self.decrease_bet_button],
                                   DISABLED)
                # self.bets -= self.bet_amount
                self.current_bets_label['text'] = f'{self.bets}'

                # GIVE CARDS TO PLAYER AND DEALER
                for i in range(2):
                    self.give_cards(self.main_window, self.player_hand, 0.505 + (i * 0.02),
                                    0.58 - (len(self.player_hand) * 0.02))
                    self.give_cards(self.main_window, self.dealer_hand, 0.505 + (i * 0.02),
                                    0.17 + (len(self.dealer_hand) * 0.02))

                # CHECK IF PLAYER HAS BLACKJACK
                if self.blackjack_check(self.player_hand):
                    self.info_label['text'] = 'Winner Winner Chicken Dinner'
                    self.return_bets_amount(3, 'win')
                    self.button_states(self.buttons, DISABLED)
                else:
                    self.button_states(self.buttons, NORMAL)

                # CHECK IF PLAYER HAS ENOUGH BETS TO GO DOUBLE
                if self.bet_amount * 2 > self.bets:
                    self.double_button['state'] = DISABLED

                # CHECK IF SPLITTING IS POSSIBLE
                if self.player_hand[0][:-1] != self.player_hand[1][:-1]:
                    self.split_button['state'] = DISABLED

        self.bet_amount_button['text'] = f'{self.bet_amount}'

    def return_bets_amount(self, multiplier, res=''):
        if res == 'win':
            self.bets += self.bet_amount * multiplier
            self.current_bets_label['text'] = f'{self.bets}'

        else:
            self.bets -= self.bet_amount * multiplier
            self.current_bets_label['text'] = f'{self.bets}'
        self.button_states([self.bet_amount_button, self.increase_bet_button, self.decrease_bet_button], NORMAL)
        self.button_states(self.buttons, DISABLED)
        self.reset = True

        if self.bets == 0:
            self.info_label['text'] = 'You ran out of luck and money!!!'
            self.button_states([self.bet_amount_button, self.increase_bet_button, self.decrease_bet_button], DISABLED)
            self.button_states(self.buttons, DISABLED)
            # START NEW GAME PROMPT
            new_button = Button(self.main_window, text='New game', command=self.new_game)
            new_button.config(font=("Alata", 15), width=10, bg='#212121', fg='#14ffec',
                              borderwidth=2, activebackground='#323232', activeforeground='#0d7377')
            new_button.place(relx=0.95, rely=0.01, anchor=NE)

    def convert_score(self, hand):
        score_type = self.scoring_hand(hand)
        if type(score_type) == int:
            return score_type

        else:
            if max([int(score_type[:score_type.index(' o')]), int(score_type[-2:])]) > 21:
                valid_max_score = min([int(score_type[:score_type.index(' o')]), int(score_type[-2:])])
            else:
                valid_max_score = max([int(score_type[:score_type.index(' o')]), int(score_type[-2:])])
            return valid_max_score

    def hit_lose_condition(self, hand, txt):
        if self.convert_score(hand) == 21:
            self.stand()
        elif self.convert_score(hand) > 21:
            self.info_label['text'] = txt
            if not self.player_splits:
                self.return_bets_amount(1, 'lose')
            else:
                self.stand()

    def on_splitting_condition(self, turn1, turn2):
        self.dealer_hidden_card.destroy()
        self.dealer_hidden_card = Create.image(self.main_window, 0.505, 0.17, self.dealer_hand[0])
        self.dealer_hidden_card.lower(self.table_cards_list[0])
        self.table_cards_list.append(self.dealer_hidden_card)

        self.dealer_points_label['text'] = f'Points: {self.scoring_hand(self.dealer_hand)}'
        while self.convert_score(self.dealer_hand) < 16:
            self.give_cards(self.main_window, self.dealer_hand, 0.505 + (len(self.dealer_hand) * 0.02),
                            0.17 + (len(self.dealer_hand) * 0.02))
            self.dealer_points_label['text'] = f'Points: {self.scoring_hand(self.dealer_hand)}'

        temp = [turn1, turn2]
        wins = []

        for i in temp:
            if self.convert_score(self.dealer_hand) > self.convert_score(i) and self.convert_score(
                    self.dealer_hand) <= 21:
                wins.append(0)
            elif self.convert_score(self.dealer_hand) == self.convert_score(i):
                if len(self.player_hand) > 0:
                    wins.append(1)
            else:
                wins.append(2)

        self.info_label['text'] = f'Hands won: {len(wins)}'

        return wins

    def new_game(self):
        # RESET VALUES
        for labels in self.label_list:
            labels['text'] = ''
        self.button_states([self.bet_amount_button,self.increase_bet_button,self.decrease_bet_button],NORMAL)

        for cards in self.table_cards_list:
            cards.destroy()
        self.table_cards_list.clear()
        self.dealer_hand.clear()
        self.player_hand.clear()
        self.split_turn = 0
        self.player_splits = False
        self.reset = False
        self.deck = Create.deck(6)
        random.shuffle(self.deck)
        self.bets = 25
        self.current_bets_label['text'] = '25'

    @staticmethod
    def blackjack_check(hand):
        for card in range(len(hand)):
            if hand[card][:-1] in ['K', 'Q', 'J', '10']:
                return hand[1 - hand.index(hand[card])][:-1] == 'A'

    @staticmethod
    def scoring_hand(hand):
        temp_hand = [i[:-1] for i in hand]
        score = [0, 0]

        for i in temp_hand:
            if i in ['10', 'J', 'Q', 'K']:
                score[0] += 10
                score[1] += 10
            elif i in ['2', '3', '4', '5', '6', '7', '8', '9']:
                score[0] += int(i)
                score[1] += int(i)
            else:
                if temp_hand.count('A') > 1:
                    score[0] += 1
                    score[1] += 11
                    for j in range(len(score)):
                        if score[j] > 21:
                            score[j] -= 10
                else:
                    score[0] += 1
                    score[1] += 11

        if len(hand) > 1:
            if score[0] == score[1] and temp_hand[0] != 'A':
                return score[0]
            else:
                for i in range(len(score)):
                    if score[i] > 21:
                        return score[1 - i]

                return f'{score[0]} or {score[1]}'
        elif len(hand) == 1:
            if 'A' in temp_hand:
                return f'1 or 11'
            else:
                return score[0]
        else:
            return f'{score[0]} or {score[1]}'

    @staticmethod
    def button_states(buttons, state):
        for button in buttons:
            button['state'] = state


b = BlackJack()
