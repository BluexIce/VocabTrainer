screen_helper = """

ScreenManager:

    MenuScreen:
    DictionaryScreen:
    VocabularyScreen:
    ExercisesScreen:
    ComparisonScreen:
    StatisticsScreen:
    SettingsScreen:
    OneWordScreen:
    FourWordsScreen:
    AddVocabularyScreen:
    DeleteVocabularyScreen:


<MenuScreen>:
    name: 'menu'

    BoxLayout:

        orientation: 'vertical'

        Button:
            text: 'Dictionary' 
            on_press: root.manager.current = 'dictionary'

        Button:
            text: 'Vocabulary' 
            on_press: root.manager.current = 'vocabulary'

        Button:
            text: 'Exercises' 
            on_press: root.manager.current = 'exercises'

        Button:
            text: 'Statistics'
            on_press: root.manager.current = 'statistics'

        Button:
            text: 'Settings'
            on_press: root.manager.current = 'settings'        

<DictionaryScreen>:
    name: 'dictionary'

    BoxLayout:

        Button:
            text: 'Back'
            on_press: 
                #root.manager.transition.direction = 'right'  #moves 'back', but all screens after accessed
                root.manager.current = 'menu'


<VocabularyScreen>:
    name: 'vocabulary'

    BoxLayout:
        orientation: 'vertical'

        Button:
            text: 'Vocab List'

        Button:
            text: 'Phrases'

        Button:
            text: 'Add New Word'
            on_press: root.manager.current = 'addvocabulary'

        Button:
            text: 'Delete Words'
            on_press: root.manager.current = 'deletevocabulary'

        Button:
            text: 'Back'
            on_press: root.manager.current = 'menu'


<AddVocabularyScreen>
    name: 'addvocabulary'

    BoxLayout:
        orientation: 'vertical'

        MDLabel:
            text: 'Enter the english vocab'

        MDTextField:
            id: adding_english_vocab
            mode: 'rectangle'

        MDLabel:
            text: 'Enter the turkish vocab'

        MDTextField:
            id: adding_turkish_vocab
            mode: 'rectangle'

        Button:
            text: 'Add'
            on_press: root.add_vocabulary()

        Button:
            text: 'Back'
            on_press: root.manager.current = 'vocabulary'







<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    label1_text: 'label 1 text'
    label2_text: 'label 2 text'
    label3_text: 'label 3 text'
    pos: self.pos
    size: self.size
    Label:
        id: id_label1
        text: root.label1_text
    Label:
        id: id_label2
        text: root.label2_text
    Label:
        id: id_label3
        text: root.label3_text
        
    Button:
        text: 'Refresh'
        on_press: root.add_word()

<RV>:
    viewclass: 'SelectableLabel'
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: False



<DeleteVocabularyScreen>        
    name: 'deletevocabulary'
    id: screendeleteword

    BoxLayout:
        orientation: 'vertical'

        RV:
            id:'rv_test'
            effect_cls: "ScrollEffect"
            scroll_y: 0


        Button:
            text: 'Back'
            size_hint: 1, .2
            on_press: root.manager.current = 'vocabulary'




<ExercisesScreen>:
    name: 'exercises'

    BoxLayout:

        orientation: 'vertical'

        Button:
            text: 'Translation'

        Button:
            text: 'Compare'
            on_press: root.manager.current = 'comparison'

        Button:
            text: 'Time Trial'

        Button:
            text: '4 Words'
            on_press: root.manager.current = 'fourword'

        Button:
            text: 'Back'
            on_press: root.manager.current = 'menu'

<ComparisonScreen>:
    name: 'comparison'

    BoxLayout:

        orientation: 'vertical'

        Button:
            text: 'One Word'
            on_press: root.manager.current = 'oneword'

        Button:
            text: 'Multi Words'
            

        Button:
            text: 'Back'
            on_press: root.manager.current = 'exercises'

<OneWordScreen>:
    name: 'oneword'

    BoxLayout:
        orientation: 'vertical'

        MDLabel:
            text: root.label_Text
            halign: 'center'

        MDTextField:
            id: turkish_input
            helper_text: 'please write the turkish equivalent'
            helper_text_mode: 'on_focus'
            mode: 'rectangle'
            #halign: 'center'
            #padding: [0,70]  # maybe just for single words?

        Button:
            text: 'Compare'
            on_press: root.compare_data()
            
<FourWordsScreen>
    name: 'fourword'
    
    BoxLayout:
        orientation: 'vertical'
        
        MDLabel:
            text: root.fourwordslabel_Text
            halign: 'center'

        GridLayout:
            rows:2
            cols:2
        
            Button:
                text: root.fourwordbutton1_Text
                on_press: root.compare_fourword_data(1)
                
            Button:
                text: root.fourwordbutton2_Text
                on_press: root.compare_fourword_data(2)
                
            Button:
                text: root.fourwordbutton3_Text
                on_press: root.compare_fourword_data(3)
                
            Button:
                text: root.fourwordbutton4_Text
                on_press: root.compare_fourword_data(4)




<StatisticsScreen>:
    name: 'statistics'

    BoxLayout:
        orientation: 'vertical'
        
        MDLabel:
            text: 'Word Counter'
            halign: 'center'

        MDLabel:
            id: wrong_number_counter
            text: root.label_counter
            halign: 'center'

        Button:
            text: 'Back'
            on_press: root.manager.current = 'menu'

<SettingsScreen>:
    name: 'settings'

    BoxLayout:
        orientation: 'vertical'

        Button:
            text: 'Language'

        Button:
            text: 'Choose File'

        Button:
            text: 'Back'
            on_press: root.manager.current = 'menu'

"""
