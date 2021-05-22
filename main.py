import random

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.behaviors import FocusBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.snackbar import Snackbar

from screen_nav import screen_helper  # import our own code from screen_nav

Window.size = (360, 600)  # only for testing, remove before building!!


# global englishvocab
# global turkishvocab


class MenuScreen(Screen):
    pass


class DictionaryScreen(Screen):
    # add dictionary  --> realtime search for words with example sentences
    pass


class VocabularyScreen(Screen):
    pass


class AddVocabularyScreen(Screen):

    def add_vocabulary(self):

        if self.ids.adding_english_vocab.text and self.ids.adding_turkish_vocab.text != '':  # is None does not work properly
            print('there is data')
            with open("vocab_english.txt", "a+", encoding='utf8') as e:
                e.write(self.ids.adding_english_vocab.text + "\n")

            with open("vocab_turkish.txt", "a+", encoding='utf8')as t:
                t.write(self.ids.adding_turkish_vocab.text + "\n")

            self.ids.adding_english_vocab.text = ''
            self.ids.adding_turkish_vocab.text = ''

        else:
            print('it is not filled out')
            self.snackbar_add_vocabulary = Snackbar(text='you have to fill out both fields!',
                                                    size_hint_x='7',
                                                    size_hint_y='7'
                                                    )
            self.snackbar_add_vocabulary.show()


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, GridLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    cols = 3


    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        #self.label1_text = str(index)
        self.ids['id_label1'].text = str(index)
        self.ids['id_label2'].text = data['label2']['text']
        #self.label2_text = data['label2']['text']
        #self.label3_text = data['label3']['text']
        self.ids['id_label3'].text = data['label3']['text']
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)



    def on_touch_down(self, touch):
        ''' Add selection on touch down '''

        yes_delete_word_button = MDFlatButton(text='Yes', on_release=self.delete_word)
        no_dont_delete_word_button = MDFlatButton(text='No', on_release=self.dont_delete_word)
        warning_received_button = MDFlatButton(text='Okay', on_release=self.warning_received)

        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:


            #todo check this --> why no turkish list?
            with open("vocab_english.txt", "r+") as r:

                englishvocab = r.readlines()
                englishvocab_readable = []

                for english_element in englishvocab:
                    englishvocab_readable.append(english_element.strip())


            if len(englishvocab_readable) < 2:
                self.dialog_prevent_zero_vocabs = MDDialog(title='Warning!',
                                                           text='You cannot delete the last vocab in a file',
                                                           size_hint=(0.7, 1),
                                                           buttons=[warning_received_button]
                                                           )

                self.dialog_prevent_zero_vocabs.open()

            else:

                self.dialog_delete_vocab = MDDialog(title='Delete Vocab?',
                                                    text= 'Delete'
                                                          ' ' + self.ids['id_label2'].text + ' ?',
                                                    size_hint=(0.7, 1),
                                                    buttons=[yes_delete_word_button, no_dont_delete_word_button]
                                                    )

                self.dialog_delete_vocab.open()



                #MDDialog to check if you want to delet the word?
                #Move to JSON instead of textfiles?
                #copy just the rv code to new project to look at it more in depth
                return self.parent.select_with_touch(self.index, touch)  # highlits itself


    def delete_word(self, obj):
        self.parent.parent.data.pop(self.index)  # deletes the entry but does not save it

        # MDDialog to check if you want to delete the entry

        with open("vocab_english.txt", "r+") as r:

            englishvocab = r.readlines()
            englishvocab_readable = []

            for english_element in englishvocab:
                englishvocab_readable.append(english_element.strip())

            actualindex = self.index
            englishvocab_readable.pop(actualindex)

        with open("vocab_english.txt", "w") as w:  # fills the file with the new array
            for word in englishvocab_readable:
                w.write(word + "\n")

        with open("vocab_turkish.txt", "r+") as r:
            turkishvocab = r.readlines()
            turkishvocab_readable = []

            for turkish_element in turkishvocab:
                turkishvocab_readable.append(turkish_element.strip())

            # turkishvocab_readable.remove(turkishvocab_readable[english_vocab_delete])
            turkishvocab_readable.pop(actualindex)

            with open("vocab_turkish.txt", "w") as w:
                for word in turkishvocab_readable:
                    w.write(word + "\n")

        self.dialog_delete_vocab.dismiss()


    def dont_delete_word(self, obj):
        self.dialog_delete_vocab.dismiss()


    def warning_received(self, obj):
        self.dialog_prevent_zero_vocabs.dismiss()


    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

        global english_vocab_delete  # if no word is selected app crashes
        global turkish_vocab_delete
        if is_selected:
            '''print("selection changed to {0}".format(rv.data[index]))
            # DeleteVocabularyScreen.delete_vocabulary(self)
            print(int(self.ids['id_label1'].text) + 1)  # actual id in the list
            print(self.ids['id_label2'].text)
            print(self.ids['id_label3'].text)'''
            # global english_vocab_delete
            english_vocab_delete = self.ids['id_label2'].text
            # global turkish_vocab_delete
            turkish_vocab_delete = self.ids['id_label3'].text


        else:
            #print("selection removed for {0}".format(rv.data[index]))
            pass


    def add_word(self):

        test = 'test'
        test2 ='test2'

        # insert_vocab_into_rv ={'label2': {'text': test}, 'label3': {'text': test2}}
        # self.parent.parent.data.append(insert_vocab_into_rv)

        ###

        # self.ids['id_label1'].text = str(index)

        #print(len(self.parent.parent.data))  # length of the index list #1000

        #open english list
        with open("vocab_english.txt", "r+") as r:

            englishvocab = r.readlines()
            englishvocab_readable = []

            for english_element in englishvocab:
                englishvocab_readable.append(english_element.strip())

        #open turkish list
        with open("vocab_turkish.txt", "r+") as r:
            turkishvocab = r.readlines()
            turkishvocab_readable = []

            for turkish_element in turkishvocab:
                turkishvocab_readable.append(turkish_element.strip())

        #print(len(englishvocab_readable))

        if len(self.parent.parent.data) != len(englishvocab_readable):
            numberone = len(englishvocab_readable)
            numbertwo = len(self.parent.parent.data)

            solution = numberone - numbertwo
            countbackwardsnumber = (len(englishvocab_readable) -1)
            entryfrommiddle = countbackwardsnumber - solution

            for x in range(solution):
                #count = countbackwardsnumber - x
                entryfrommiddle += 1
                #print(englishvocab_readable[count])  # prints the entries from last to solution
                insert_vocab_into_rv = {'label2': {'text': englishvocab_readable[entryfrommiddle]}, 'label3': {'text': turkishvocab_readable[entryfrommiddle]}}
                self.parent.parent.data.append(insert_vocab_into_rv)
                #entryfrommiddle += 1

        # insert_vocab_into_rv ={'label2': {'text': test}, 'label3': {'text': test2}}
        # self.parent.parent.data.append(insert_vocab_into_rv)


class RV(RecycleView):

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

        self.showdata()

        # self.checkclockbool()

        # if self.showdata() != self.what():
        #   Clock.schedule_interval(self.reloading, .1)
        # Clock.schedule_interval(self.reloading, .1) #reloads every milisecond
        # self.data = [{'text': str(x)} for x in range(10000)]

    def checkclockbool(self):
        global testtest
        testtest = False
        Clock.schedule_interval(self.refresh_the_screen, 1)

    def refresh_the_screen(self, time):

        global testtest

        while testtest is True:
            Clock.schedule_interval(self.reloading, .1)
            testtest = False

        else:
            testtest = False

    def reloading(self, time):
        with open("vocab_english.txt", "r+", encoding='utf8') as r:
            englishvocab = r.readlines()
            englishvocab_readable = []
            for english_element in englishvocab:
                englishvocab_readable.append(english_element.strip())

        with open("vocab_turkish.txt", "r+", encoding='utf8') as r:
            turkishvocab = r.readlines()
            turkishvocab_readable = []
            for turkish_element in turkishvocab:
                turkishvocab_readable.append(turkish_element.strip())

        filtered = zip(englishvocab_readable, turkishvocab_readable)
        self.data = []
        for display_english, display_turkish in filtered:
            d = {'label2': {'text': display_english}, 'label3': {'text': display_turkish}}
            self.data.append(d)

        print('Reloading')
        global testtest
        testtest = False

    def showdata(self):

        with open("vocab_english.txt", "r+", encoding='utf8') as r:
            englishvocab = r.readlines()
            englishvocab_readable = []
            for english_element in englishvocab:
                englishvocab_readable.append(english_element.strip())

        with open("vocab_turkish.txt", "r+", encoding='utf8') as r:
            turkishvocab = r.readlines()
            turkishvocab_readable = []
            for turkish_element in turkishvocab:
                turkishvocab_readable.append(turkish_element.strip())

        filtered = zip(englishvocab_readable, turkishvocab_readable)
        self.data = []
        for display_english, display_turkish in filtered:
            d = {'label2': {'text': display_english}, 'label3': {'text': display_turkish}}
            self.data.append(d)


class DeleteVocabularyScreen(Screen):
    # DemoApp.get_running_app().get_screen('deletevocabulary').ids.rv_test.showdata(self)

    '''def on_enter(self):
        print('Hello there to you')
        #self.ids.rv_test.scroll_y = 0
        global testtest
        testtest = True
        #call clock_schedule from RV
        #rv = DemoApp.get_running_app().root.ids.rv_test.refresh_the_screen()
        #rv.reloading()

    def on_leave(self):
        print('Goodbye then')
        #end clock_schedule from RV
        global testtest

        if testtest is True:
            testtest = False
        else:
            testtest = False
'''

    '''def on_enter(self):
        self.Data()



    def Data(self):
        with open("vocab_english.txt", "r+") as r:
            # global englishvocab
            englishvocab = r.readlines()
            englishvocab_readable = []

            for english_element in englishvocab:
                englishvocab_readable.append(english_element.strip())
            print(englishvocab_readable)  # shows content of file as a list #rn just console'''

    def delete_vocabulary(self):
        pass
        '''if english_vocab_delete == '' or turkish_vocab_delete == '':
            print('No word selected')
            #MD Popup : please select a row
            # implement --> when no row is higlighted as well
        else:

            with open("vocab_english.txt", "r+") as r:
                # global englishvocab
                englishvocab = r.readlines()
                englishvocab_readable = []

                for english_element in englishvocab:
                    englishvocab_readable.append(english_element.strip())

                # print(english_vocab_delete)
                # print(len(english_vocab_delete))

                # print(turkish_vocab_delete)

                letters_for_word_delete = englishvocab_readable.index(english_vocab_delete)
                number_for_word_delete = int(englishvocab_readable.index(english_vocab_delete))
                print(letters_for_word_delete)
                print('###########################')
                print()
                print('###########################')
                englishvocab_readable.pop(number_for_word_delete)

            with open("vocab_english.txt", "w") as w:  # fills the file with the new array
                for word in englishvocab_readable:
                    w.write(word + "\n")

            with open("vocab_turkish.txt", "r+") as r:
                turkishvocab = r.readlines()
                turkishvocab_readable = []

                for turkish_element in turkishvocab:
                    turkishvocab_readable.append(turkish_element.strip())

                # turkishvocab_readable.remove(turkishvocab_readable[english_vocab_delete])
                turkishvocab_readable.pop(number_for_word_delete)

                with open("vocab_turkish.txt", "w") as w:
                    for word in turkishvocab_readable:
                        w.write(word + "\n")
            print('Here needs to be a new instance loaded')
'''
        # DemoApp.get_running_app().get_screen('deletevocabulary').ids.rv_test.showdata(self)

    pass


class ExercisesScreen(Screen):
    # Example sentences with gaps
    # 4 different words displayed(english) -> compare with one turkish word (quick exercise)
    # time trial  --> every exercise mixed with limited time
    # Yes/No questions --> word given -> right or wrong
    pass


class ComparisonScreen(Screen):
    pass


class OneWordScreen(Screen):
    # label_Text = StringProperty(englishvocab_readable[random_number])

    with open("vocab_english.txt", "r+", encoding='utf8') as ve:
        # global englishvocab
        englishvocab = ve.readlines()

    with open("vocab_turkish.txt", "r+", encoding='utf8') as vt:
        # print("The new turkish list: " + "\n" + e.read())
        # global turkishvocab
        turkishvocab = vt.readlines()

        turkishvocab_readable = []

        for turkish_element in turkishvocab:
            turkishvocab_readable.append(turkish_element.strip())

        englishvocab_readable = []

        for english_element in englishvocab:
            englishvocab_readable.append(english_element.strip())

    random_number = random.randint(0, len(englishvocab_readable) - 1)
    # label_Text = (englishvocab_readable[random_number])

    label_Text = StringProperty(englishvocab_readable[random_number])

    def compare_data(self):  # the method is the on_press: attribute in screen_nav.py

        close_button_one_word = MDFlatButton(text='Close', on_release=self.close_dialog)
        move_to_next_vocab_button = MDFlatButton(text='Next', on_release=self.move_forward)
        retry_current_vocab_button = MDFlatButton(text='Retry', on_release=self.close_dialog)

        word = self.ids.turkish_input.text  # reference the id from your textfield
        if word == self.turkishvocab_readable[self.random_number]:  # compare the textfield with the vocab

            self.dialog_one_word = MDDialog(title='Check Vocab',
                                            text='that was right!',
                                            size_hint=(0.7, 1),
                                            buttons=[close_button_one_word, move_to_next_vocab_button]
                                            )
            self.dialog_one_word.open()
        else:
            self.dialog_one_word = MDDialog(title='Check Vocab',
                                            text=self.turkishvocab_readable[
                                                     self.random_number] + ' would have been right',
                                            size_hint=(0.7, 1),
                                            buttons=[move_to_next_vocab_button]
                                            )
            self.dialog_one_word.open()

    def close_dialog(self, obj):
        self.dialog_one_word.dismiss()

    def move_forward(self, *args):
        self.update()
        # self.manager.current = 'oneword' #works, but does nothing try 'settings' for example
        self.dialog_one_word.dismiss(self)  # closes dialog upon clicking next #self after dismiss(self) is not needed?

    def update(self):
        # self.label_Text = self.englishvocab_readable[random.randint(0, len(self.englishvocab_readable) - 1)]
        # self.label_Text = self.englishvocab_readable[random.randint(0, len(self.englishvocab_readable) - 1)]

        self.random_number = random.randint(0, len(self.englishvocab_readable) - 1)
        self.label_Text = self.englishvocab_readable[
            self.random_number]  # works for updating the label, only the label!!!

        self.ids.turkish_input.text = ''
        # self.random_number = random.randint(0, len(self.englishvocab_readable) - 1)
        # self.englishvocab_readable[self.random_number] = self.label_Text
        # print('something happened')


class FourWordsScreen(Screen):

    global random_numbers_answers_fourword
    with open("vocab_english.txt", "r+", encoding='utf8') as ve:
        englishvocab = ve.readlines()

        englishvocab_readable = []

        for english_element in englishvocab:
            englishvocab_readable.append(english_element.strip())

    with open("vocab_turkish.txt", "r+", encoding='utf8') as vt:
        turkishvocab = vt.readlines()

        turkishvocab_readable = []

        for turkish_element in turkishvocab:
            turkishvocab_readable.append(turkish_element.strip())

    random_number_solution_fourword = random.randint(0, len(englishvocab_readable) - 1)

    random_numbers_answers_fourword = random.sample(range(0, len(turkishvocab_readable) - 1), 4)  # get index #works on its own


    word1 = englishvocab_readable[random_numbers_answers_fourword[0]] #get word
    word2 = englishvocab_readable[random_numbers_answers_fourword[1]]
    word3 = englishvocab_readable[random_numbers_answers_fourword[2]]
    word4 = englishvocab_readable[random_numbers_answers_fourword[3]]

    wordlistenglish = [word1, word2, word3, word4]
    # receiving only the index 0-3
    eng_compare1 = wordlistenglish.index(word1)
    eng_compare2 = wordlistenglish.index(word2)
    eng_compare3 = wordlistenglish.index(word3)
    eng_compare4 = wordlistenglish.index(word4)

    eng_list = [eng_compare1, eng_compare2, eng_compare3, eng_compare4]

    word1index = englishvocab_readable.index(word1)#gets index of the value from the long array index
    word2index = englishvocab_readable.index(word2)
    word3index = englishvocab_readable.index(word3)
    word4index = englishvocab_readable.index(word4)

    wordlistenglishindex = [word1index, word2index, word3index, word4index]



    word1turkish = turkishvocab_readable[word1index] #word
    word2turkish = turkishvocab_readable[word2index]  # word
    word3turkish = turkishvocab_readable[word3index]  # word
    word4turkish = turkishvocab_readable[word4index]  # word

    wordlistturkish = [word1turkish, word2turkish, word3turkish, word4turkish]
    # receiving only the index 0-3
    trk_compare1 = wordlistturkish.index(word1turkish)
    trk_compare2 = wordlistturkish.index(word2turkish)
    trk_compare3 = wordlistturkish.index(word3turkish)
    trk_compare4 = wordlistturkish.index(word4turkish)

    trk_list = [trk_compare1, trk_compare2, trk_compare3, trk_compare4]

    word1turkishindex = turkishvocab_readable.index(word1turkish) #index of word from long array with english index value
    word2turkishindex = turkishvocab_readable.index(word2turkish)
    word3turkishindex = turkishvocab_readable.index(word3turkish)
    word4turkishindex = turkishvocab_readable.index(word4turkish)

    wordlistturkishindex = [word1turkishindex, word2turkishindex, word3turkishindex, word4turkishindex]

    #todo give each random_number a different index each time  --> they are str
    #todo get the index behind the str
    #done boxlayout for the four buttons --> arrange like 2 | 2


    #todo randmoize


    inbetween1 = word1turkish
    inbetween2 = word2turkish
    inbetween3 = word3turkish
    inbetween4 = word4turkish

    inbetweenarray = [inbetween1, inbetween2, inbetween3, inbetween4]


    #todo #done randomize the index of the array with an array in between
    haa = [0, 1, 2, 3]

    random.shuffle(haa)

    fourwordbutton1_Text =StringProperty(inbetweenarray[haa[0]])
    fourwordbutton2_Text =StringProperty(inbetweenarray[haa[1]])
    fourwordbutton3_Text =StringProperty(inbetweenarray[haa[2]])
    fourwordbutton4_Text =StringProperty(inbetweenarray[haa[3]])




    fourwordslabel_Text = StringProperty(wordlistenglish[0]) #wordlistenglishindex[0]



    def compare_fourword_data(self, index):

        fourwordscreen = self.manager.get_screen('fourword')
        setattr(fourwordscreen, 'index', index)

        close_button_fourword = MDFlatButton(text='Close', on_release=self.close_dialog_four)
        move_to_next_four_button = MDFlatButton(text='Next', on_release=self.move_forward_four)

        if self.index-1 == self.haa.index(0):
            self.dialog_four_word = MDDialog(title='Check Vocab',
                                            text='good one',
                                            size_hint=(0.7, 1),
                                            buttons=[close_button_fourword, move_to_next_four_button]
                                             )
            self.dialog_four_word.open()

        else:
            self.dialog_four_word = MDDialog(title='Check Vocab',
                                            text= self.word1turkish + ' would have been right',
                                            size_hint=(0.7, 1),
                                            buttons=[move_to_next_four_button]
                                             )
            self.dialog_four_word.open()

    def close_dialog_four(self, obj):
        self.dialog_four_word.dismiss()

    def move_forward_four(self, obj):
        self.update_four()

        self.dialog_four_word.dismiss()

    def update_four(self, *args):
        self.random_number_solution_fourword = random.randint(0, len(self.englishvocab_readable) - 1)
        self.random_numbers_answers_fourword = random.sample(range(0, len(self.turkishvocab_readable) - 1),4)  # get index #works on its own


        self.word1 = self.englishvocab_readable[self.random_numbers_answers_fourword[0]]  # get word
        self.word2 = self.englishvocab_readable[self.random_numbers_answers_fourword[1]]
        self.word3 = self.englishvocab_readable[self.random_numbers_answers_fourword[2]]
        self.word4 = self.englishvocab_readable[self.random_numbers_answers_fourword[3]]

        self.wordlistenglish = [self.word1, self.word2, self.word3, self.word4]
        # receiving only the index 0-3
        self.eng_compare1 = self.wordlistenglish.index(self.word1)
        self.eng_compare2 = self.wordlistenglish.index(self.word2)
        self.eng_compare3 = self.wordlistenglish.index(self.word3)
        self.eng_compare4 = self.wordlistenglish.index(self.word4)

        self.eng_list = [self.eng_compare1, self.eng_compare2, self.eng_compare3, self.eng_compare4]

        # needed to get index for turkish index
        self.word1index = self.englishvocab_readable.index(self.word1)  # gets index of the value from the long array index
        self.word2index = self.englishvocab_readable.index(self.word2)
        self.word3index = self.englishvocab_readable.index(self.word3)
        self.word4index = self.englishvocab_readable.index(self.word4)

        self.wordlistenglishindex = [self.word1index, self.word2index, self.word3index, self.word4index]

        self.word1turkish = self.turkishvocab_readable[self.word1index]  # word
        self.word2turkish = self.turkishvocab_readable[self.word2index]  # word
        self.word3turkish = self.turkishvocab_readable[self.word3index]  # word
        self.word4turkish = self.turkishvocab_readable[self.word4index]  # word

        self.wordlistturkish = [self.word1turkish, self.word2turkish, self.word3turkish, self.word4turkish]
        # receiving only the index 0-3
        self.trk_compare1 = self.wordlistturkish.index(self.word1turkish)
        self.trk_compare2 = self.wordlistturkish.index(self.word2turkish)
        self.trk_compare3 = self.wordlistturkish.index(self.word3turkish)
        self.trk_compare4 = self.wordlistturkish.index(self.word4turkish)

        self.trk_list = [self.trk_compare1, self.trk_compare2, self.trk_compare3, self.trk_compare4]

        self.word1turkishindex = self.turkishvocab_readable.index(self.word1turkish)  # index of word from long array with english index value
        self.word2turkishindex = self.turkishvocab_readable.index(self.word2turkish)
        self.word3turkishindex = self.turkishvocab_readable.index(self.word3turkish)
        self.word4turkishindex = self.turkishvocab_readable.index(self.word4turkish)

        self.wordlistturkishindex = [self.word1turkishindex, self.word2turkishindex, self.word3turkishindex, self.word4turkishindex]

        self.inbetween1 = self.word1turkish
        self.inbetween2 = self.word2turkish
        self.inbetween3 = self.word3turkish
        self.inbetween4 = self.word4turkish

        self.inbetweenarray = [self.inbetween1, self.inbetween2, self.inbetween3, self.inbetween4]


        self.haa = [0, 1, 2, 3]

        random.shuffle(self.haa)

        self.fourwordbutton1_Text = self.inbetweenarray[self.haa[0]]
        self.fourwordbutton2_Text = self.inbetweenarray[self.haa[1]]
        self.fourwordbutton3_Text = self.inbetweenarray[self.haa[2]]
        self.fourwordbutton4_Text = self.inbetweenarray[self.haa[3]]


        self.fourwordslabel_Text = self.wordlistenglish[0] # wordlistenglishindex[0]

        '''help = self.index-1

        if self.wordlistturkishindex[help] == self.wordlistenglishindex[0]:
            print('solution')
            print(self.wordlistturkishindex[self.index-1])
            print(self.wordlistenglishindex[0])
            print(self.index-1)
            print(help)
        else:
            print('back to the drawing board')'''

        #if self.index == self.word1index: # self.englishvocab_readable[self.random_number_solution_fourword]:
         #   print('good')

        #else:
         #   print('not good')
          #  print(self.index)

            #print(self.englishvocab_readable.index(self.random_number_solution_fourword)-1) #not in list



class StatisticsScreen(Screen):
    # display vocabs you did wrong --> another rv ?
    # ranking list, how many vocabs have been compared overall
    pass


class SettingsScreen(Screen):
    # language menu to select overlay language
    # choose different txt files to practice
    # load your own txt files into the app

    pass


class DemoApp(MDApp):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(MenuScreen(name='dictionary'))
        sm.add_widget(MenuScreen(name='vocabulary'))
        sm.add_widget(MenuScreen(name='addvocabulary'))
        sm.add_widget(MenuScreen(name='deletevocabulary'))
        sm.add_widget(MenuScreen(name='exercises'))
        sm.add_widget(MenuScreen(name='comparison'))
        sm.add_widget(MenuScreen(name='oneword'))
        sm.add_widget(MenuScreen(name='fourword'))

        sm.add_widget(MenuScreen(name='statistics'))
        sm.add_widget(MenuScreen(name='settings'))
        screen = Builder.load_string(screen_helper)
        return screen

    def on_start(self):
        self.fps_monitor_start()


DemoApp().run()
