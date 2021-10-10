from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class Calculator(App):
    def build(self):
        self.operators = ['/','*','-','+']
        self.last_was_operator = None
        self.last_button = None
        self.has_dot = False
        main_layout = BoxLayout(orientation='vertical')
        self.solution = TextInput(
            multiline=False,
            readonly=True,
            halign='right',
            font_size=55
        )

        main_layout.add_widget(self.solution)

        buttons = [
            ['7','8','9','/'],
            ['4','5','6','*'],
            ['1','2','3','-'],
            ['.','0','C','+'],
        ]

        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text = label,
                    pos_hint={'center_x':.5,'center_y':.5},
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)
        equals_button = Button(
            text = '=',pos_hint={'center_x':.5,'center_y':.5}
        )

        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)


        return main_layout

    def on_button_press(self,instance):
        current = self.solution.text
        button_text = instance.text
        if button_text == 'C': #limpa os valores
            self.solution.text = ''
        else:
            if current and (self.last_was_operator and button_text in self.operators):
                #Não adicionar 2 operadores seguidos, tipo +* -+ /+ -/
                return
            elif self.last_was_operator and button_text == '.':
                #Não pode ter ponto após um sinal
                return  
            elif current == '' and button_text in self.operators or current == '' and button_text == '.' :
                #O primeiro valor não pode ser um operador ou um ponto '.'
                return            
            elif '.' in current and button_text == '.' and self.has_dot:
                #Não pode ter outro ponto até ter um sinal
                return
            else:
                if len(current) > 0 and current[-1] == '.' and button_text == '.':
                    #Não pode ter ponto após outro ponto
                    return
                if button_text == '.':
                    #Bloqueia após usar um ponto
                    self.has_dot = True
                if self.last_was_operator:
                    #Libera por outro ponto após usar um sinal
                    self.has_dot = False
                new_text = current + button_text
                self.solution.text = new_text
        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    def on_solution(self,instance):
        text = self.solution.text
        if text:
            if self.last_was_operator:
                return
            else:
                print(self.solution.text)
                solution = str(eval(self.solution.text))
                self.solution.text = solution

if __name__ == '__main__':
    calc = Calculator()
    calc.run()