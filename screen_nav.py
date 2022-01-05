screen_helper = """

ScreenManager:

    MenuScreen:
    DictionaryScreen:
    VocabularyScreen:
    ExercisesScreen:
    StatisticsScreen:
    OneWordScreen:
    FourWordsScreen:
    Pracwrngwords:
    DeleteVocabularyScreen:
    AddVocabularyScreen:

<MenuScreen>:
    name: 'menu'
    
    
    
    BoxLayout:

        orientation: 'vertical'


        MDToolbar:
            id: toolbar
            title: 'Welcome - Hoşgeldin'
            anchor_title: 'center'
            md_bg_color: 26/255, 117/255, 255/255, 1
            specific_text_color: 1/255, 1/255, 1/255, 1
            #255, 117, 26
            
        MDBottomNavigation:
            panel_color: 255/255, 117/255, 26/255, 1
            #text_color_active: 26/255, 117/255, 255/255, 1
            #text_color_normal: 255/255, 255/255, 1/255, 1
            
            MDBottomNavigationItem:
                name: 'screen1'
                text: 'Search'
                icon: 'magnify'
                
                DictionaryScreen
            
            MDBottomNavigationItem:
                name: 'screen2'
                text: 'Vocabs'
                icon: 'playlist-edit'
                
                VocabularyScreen
                
            MDBottomNavigationItem:
                name: 'screen3'
                text: 'Practice'
                icon: 'heart-pulse'
                
                ExercisesScreen
                
            
                
            MDBottomNavigationItem:
                name: 'screen5'
                text: 'Score'
                icon: 'format-list-numbered'
                
                StatisticsScreen
            
       
<DictionaryScreen>:
    name: 'dictionary'

    BoxLayout:

        orientation: 'vertical'
        
        MDLabel:
            text: 'Search a word in english'
            halign: 'center'
        
        MDTextField:
            id: search_vocab
            mode: 'rectangle'
            halign: 'center'
            
        
        MDLabel:
            text: root.label_searchengineeng
            halign:'center'
        
        MDLabel:
            text: root.label_searchengine
            halign: 'center'
            
        Button:
            text: 'Search'
            on_press: root.searchforword()

<VocabularyScreen>:
    name: 'vocabulary'

    BoxLayout:
        orientation: 'vertical'

        MDLabel:
            text: 'Feel free to add and delete vocabulary'
            halign: 'center'
            
        Button:
            text: 'Add New Word'
            on_release: 
                app.root.current = 'addvocabulary'
                app.root.transition.direction = 'left'
                
        Button:
            text: 'Delete Words'
            on_release: 
                app.root.current = 'deletevocabulary'
                app.root.transition.direction = 'left'

        

<AddVocabularyScreen>        
    name: 'addvocabulary'

    BoxLayout:
        orientation: 'vertical'
        
        MDLabel:
            text: 'Enter the english vocabulary'
            halign: 'center'
            
        MDTextFieldRect:
            id: english_input
            size_hint: 1, None
            height: '30dp'
            
        MDLabel:
            text: 'Enter the turkish vocabulary'
            halign: 'center'        
                
        MDTextFieldRect:
            id: turkish_input
            size_hint: 1, None
            height: '30dp'
    
        Button:
            text: 'Add vocabulary'
            on_release: root.add_vocabulary()


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
        on_release: root.add_word()

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

<ExercisesScreen>:
    name: 'exercises'

    BoxLayout:

        orientation: 'vertical'

        MDLabel:
            text: 'Exercise and get better by the day'
            halign: 'center'
        
        Button:
            text: 'One Word Translation'
            on_release: 
                app.root.current = 'oneword'
                app.root.transition.direction = 'left'
             
             
        Button:
            text: '4 Words'
            on_release: 
                app.root.current = 'fourword'
                app.root.transition.direction = 'left'
             
                
        Button:
            text: 'Practice Wrong Words'
            on_release:
                app.root.current = 'pracwrngwords'
                app.root.transition.direction = 'left'

        
                
                
      #  Button:
           # text: 'Back'
          #  on_release: 
             #   root.manager.current = 'menu'
              #  root.manager.transition.direction = 'right'                


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
            on_release: root.compare_data()

        #Button:
            #text: 'Back'
            #on_release: 
               # root.manager.current = 'comparison'
               # root.manager.transition.direction = 'right'
            
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
                on_release: root.compare_fourword_data(1)

            Button:
                text: root.fourwordbutton2_Text
                on_release: root.compare_fourword_data(2)

            Button:
                text: root.fourwordbutton3_Text
                on_release: root.compare_fourword_data(3)

            Button:
                text: root.fourwordbutton4_Text
                on_release: root.compare_fourword_data(4)

        #Button:
            #text: 'Back'
            #on_release: 
               # root.manager.current = 'menu'
                #root.manager.transition.direction = 'right'

<Pracwrngwords>:
    name: 'pracwrngwords'
    
    BoxLayout:
        orientation: 'vertical'
        
        MDLabel:
            text: root.wrngengwrd_text
            halign: 'center'

        MDLabel:
            text: root.wrngtrkwrd_text
            halign: 'center'

        Button:
            text: 'Next'
            on_release: root.show_next()

<StatisticsScreen>:
    name: 'statistics'

    BoxLayout:
        orientation: 'vertical'
        
        MDLabel:
            text: 'All your stats at one glimpse'
            halign: 'center'
        
        GridLayout:
            cols: 2
        
            MDLabel:
                text: 'Wrong Word Counter'
                halign: 'center'
            MDLabel:
                id: wrong_number_counter
                text: root.label_counter
                halign: 'center'
        
        GridLayout:
            cols: 2
            
            MDLabel:
                text: 'Overall Word Counter'
                halign: 'center'
            MDLabel:
                id: good_number_counter
                text: root.label_counter_good
                halign: 'center'
        
        GridLayout:
            cols: 2
            rows: 2
            
            Button:
                text: 'refresh_score'
                on_release: root.refresh_counter()
                
            Button:
                text: 'Reset both counters'
                on_release: root.reset_counter()
            
        
        
        #Button:
            #text: 'Back'
           # on_release: 
               # root.manager.current = 'menu'
               # root.manager.transition.direction = 'right'
"""
