import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy import Config
Config.set('graphics', 'multisamples', '0')
from kivy.uix.floatlayout import FloatLayout
from kivy.core.text import LabelBase
from kivy.uix.textinput import TextInput

LabelBase.register(name="BebasNeue-Regular", fn_regular="BebasNeue-Regular.otf")

class MyFloatInput(TextInput):

    def right_adjust(self, text):
        max_width = self.width - self.padding[0] - self.padding[2]
        new_text = text
        text_width = self._get_text_width(new_text, self.tab_width, self._label_cached)
        while text_width < max_width:
            new_text = ' ' + new_text
            text_width = self._get_text_width(new_text, self.tab_width, self._label_cached)
        while text_width >= max_width:
            if new_text[0] != ' ':
                break
            else:
                new_text = new_text[1:]
                text_width = self._get_text_width(new_text, self.tab_width, self._label_cached)
        return new_text

    def insert_text(self, the_text, from_undo=False):
        cc, cr = self.cursor
        cur_text = self._lines[cr]
        initial_len = len(cur_text)
        new_text = self.right_adjust(cur_text[:cc] + the_text + cur_text[cc:])
        try:
            num = float(new_text) # throw exception if new_text is invalid float
        except ValueError:
            return
        self._lines[cr] = ''
        super(MyFloatInput, self).insert_text(new_text, from_undo=from_undo)
        final_len = len(self._lines[cr])
        self.cursor = self.get_cursor_from_index(final_len - (initial_len-cc))

    def on_size(self, instance, value):
        super(MyFloatInput, self).on_size(instance, value)
        if len(self._lines) == 0:
            return True
        cc, cr = self.cursor
        cur_text = self._lines[cr]
        initial_len = len(cur_text)
        super(MyFloatInput, self)._refresh_text(self.right_adjust(cur_text))
        final_len = len(self._lines[cr])
        self.cursor = self.get_cursor_from_index(final_len - (initial_len - cc))
        return True

    def set_right_adj_text(self, text):
        num = float(text)  # throws exception if text is invalid float
        self._refresh_text(self.right_adjust(text))

    def on_text(self, instance, text):
        #num = float(text)  # throws exception if text is invalid float
        self._refresh_text(self.right_adjust(text))



class CalcLayout(FloatLayout):

    def evaluate(self, correct):
        if correct:
            try:
                self.display.text = str(eval(self.display.text))
            except Exception:
                self.display.text = "Error"

    def backspace(self):
        a = len(self.display.text)
        b = str(a-1)
        c = self.display.text
        d = c[int(0):int(b)]

        self.display.text = str(d)

    def mplus(self):
        num = str(self.display.text)
        num2 = str(self.displaym.text)
        num3 = str(num) + "+" + str(num2)
        numf = eval(num3)
        self.displaym.text = str(numf)
        self.display.text = ""

    def mminus(self):
        num = str(self.display.text)
        num2 = str(self.displaym.text)
        num3 = str(num2) + "-" + str(num)
        numf = eval(num3)
        self.displaym.text = str(numf)
        self.display.text = ""

    def mrelease(self):
        num = str(self.display.text)
        num2 = str(self.displaym.text)
        self.display.text = ""
        self.display.text = str(num2)

    def mclear(self):
        num = str(self.display.text)
        num2 = str(self.displaym.text)
        self.displaym.text = "0"

class PicturesApp(App):
    def build(self):
        return CalcLayout()

if __name__ == "__main__":
    PicturesApp().run()