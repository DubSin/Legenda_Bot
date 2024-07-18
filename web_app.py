import flet as ft
from db import BoT_DB
from math import ceil

bot_db = BoT_DB('/data/courses.db')


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#141221"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    text_num = ft.TextField(value='0', text_align='left', width=300)
    page.add(ft.Text('Введите цену товара \n (Если товаров несколько то перчислите через запятую)'),
             text_num)
    result_label = ft.Text('0', width=300, height=120, size=100)

    def count_yuan(e):
        try:
            result_label.value = ceil(int(text_num.value) / float(bot_db.get_yuan()[0]))
            page.update()
        except ValueError:
            pass

    def count_dollar(e):
        try:
            result_label.value = ceil(int(text_num.value) / float(bot_db.get_dollar()[0]))
            page.update()
        except ValueError:
            pass

    def count_euro(e):
        try:
            result_label.value = ceil(int(text_num.value) / float(bot_db.get_euro()[0]))
            page.update()
        except ValueError:
            pass


    yuan_btn = ft.ElevatedButton(text='¥', bgcolor='orange400', color='white', on_click=count_yuan)
    dollar_btn = ft.ElevatedButton(text='$', bgcolor='orange400', color='white', on_click=count_dollar)
    euro_btn = ft.ElevatedButton(text='€', bgcolor='orange400', color='white', on_click=count_euro)
    page.add(ft.Row([yuan_btn, dollar_btn, euro_btn], alignment=ft.MainAxisAlignment.CENTER),
             result_label)


ft.app(target=main, view=None, port='8000')
