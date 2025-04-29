import datetime
import flet as ft
import requests
import json
import os


def main(page: ft.Page):
    page.theme_mode = 'dark'
    page.scroll = ft.ScrollMode.AUTO
    url = os.getenv('URL')

    def authentication(e, u=url):
        u += os.getenv('U_LOGIN')
        auth = {
            'login': os.getenv('LOGIN_ONLINE'),
            'password': os.getenv('PASSWORD_ONLINE')
        }
        resp = requests.post(u, data=auth, verify=False)
        return resp.json()['data']['access_token']

    def search_vehicles_function(e, u=url):
        search_vehicles_result_field.content.controls[0].value = 'Пошел процесс...'
        page.update()
        u += os.getenv('U_ESBD')
        method = {
            "methodName": "SearchVehicles",
            "params": {
                "aTF_NUMBER": search_vehicles_input.controls[0].value,
                "aTF_REG_CERTIF": search_vehicles_input.controls[1].value,
                "aTF_ID": 0
            }
        }

        headers = {'Authorization': 'Bearer ' + authentication(e)}
        resp = requests.post(u, headers=headers, json=method, verify=False)

        if resp.status_code == 200:
            search_vehicles_result_field.content.controls[0].value = 'С данными ТС все корректно: \n\n' + json.dumps(resp.json()['data']['SearchVehiclesResult']['Vehicle'], indent=4, ensure_ascii=False)

            page.update()
        else:
            search_vehicles_result_field.content.controls[0].value = resp.json()
            page.update()

    def set_client_function(e, u=url):
        u += os.getenv('U_ESBD')

        # if switch:
        #     pass
        # else:
        method = {
            "methodName": "SetClient",
            "params": {
                "aClient": {
                    "First_Name": [content.value for content in set_client_input_fields_fiz.content.controls if getattr(content, "helper_text", None) == 'Имя'][0],
                    "Last_Name": [content.value for content in set_client_input_fields_fiz.content.controls if getattr(content, "helper_text", None) == 'Фамилия'][0],
                    "Middle_Name": [content.value for content in set_client_input_fields_fiz.content.controls if getattr(content, "helper_text", None) == 'Отчество'][0],
                    "IIN": [content.value for content in set_client_input_fields_fiz.content.controls if getattr(content, "helper_text", None) == 'ИИН'][0],
                    "Natural_Person_Bool": 1,
                    "Class_ID": 0,
                    "Born": [content.value for content in set_client_input_fields_fiz.content.controls if getattr(content, "helper_text", None) == 'Дата рождения'][0],
                    "Sex_ID": [1 if content.value == True else 2 for content in set_client_input_fields_fiz.content.controls if getattr(content, "label", None) == 'Мужчина | Женщина'][0],
                    "SETTLEMENT_ID": 0,
                    "DOCUMENT_TYPE_ID": [content.value for content in set_client_input_fields_fiz.content.controls if getattr(content, "helper_text", None) == 'Тип документа'][0],
                    "DOCUMENT_NUMBER": [content.value for content in set_client_input_fields_fiz.content.controls if getattr(content, "helper_text", None) == 'Номер документа'][0],
                    "DOCUMENT_GIVED_DATE": [content.value for content in set_client_input_fields_fiz.content.controls if getattr(content, "helper_text", None) == 'Дата выдачи'][0],
                    "ACTIVITY_KIND_ID": 250,
                    "RESIDENT_BOOL": [1 if content.value == True else 0 for content in set_client_input_fields_fiz.content.controls if getattr(content, "label", None) == 'Резидент'][0],
                    "ECONOMICS_SECTOR_ID": 10,
                    "COUNTRY_ID": 2,
                    "verify_bool": [1 if content.value == True else 0 for content in set_client_input_fields_fiz.content.controls if getattr(content, "label", None) == 'Резидент'][0]
                }
            }
        }

        # headers = {'Authorization': 'Bearer ' + authentication(e)}
        # resp = requests.post(u, headers=headers, json=method, verify=False)
        #
        # if resp.status_code == 200:
        #     search_vehicles_result_field.content.controls[0].value = ('С данным ТС все корректно.\n\n' + json.dumps(resp.json()['data']['SearchVehiclesResult']['Vehicle'], indent=4, ensure_ascii=False))
        #     page.update()
        # else:
        #     search_vehicles_result_field.content.controls[0].value = resp.json()
        print(method)

        page.update()

    def set_client_fiz_ur(e):
        page.clean()
        if e.control.value == False:
            page.add(set_client_input_fields_fiz)
        elif e.control.value == True:
            page.add(set_client_input_fields_ur)
        page.update()

    def popup_select(e):
        page.clean()
        if e.control.text == 'Search Vehicles':
            page.add(search_vehicles)
        else:
            page.add(set_client)
        page.update()

    search_vehicles_input = ft.Column(
        [
            ft.TextField(helper_text=value, color='white', border_color='white', width=300)
            for value in ['госномер', 'номер техпаспорта']
        ]
    )

    search_vehicles_button = ft.Button(text='Поиск', width=100, height=50, bgcolor='green',
                                       on_click=search_vehicles_function)

    search_vehicles_result_field = ft.Container(
        content=ft.Column(
            [
                ft.TextField('Результат', read_only=True, multiline=True),
            ],
            scroll=ft.ScrollMode.ALWAYS
        ),
        width=600,
        height=600,
        border=ft.border.all(1, 'white'),
        padding=10
    )

    popup_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(icon=ft.Icons.SEARCH, text='Search Vehicles', on_click=popup_select),
            ft.PopupMenuItem(icon=ft.Icons.PEOPLE, text='Изменить данные клиента в ЕСБД (SetClient)',
                             on_click=popup_select)
        ],
    )

    switch = ft.Switch(label='Физическое лицо | Юридическое лицо', value=False, on_change=set_client_fiz_ur)
    set_client_input_fields_fiz = ft.Container(
        content=ft.Column(
            [
                switch
            ] + [
                ft.TextField(helper_text=value, color='white', border_color='white', width=300)
                for value in ['ИИН', 'Имя', 'Фамилия', 'Отчество', 'Дата рождения', 'Номер документа', 'Дата выдачи']
            ] + [
                ft.Switch(
                    label="Мужчина | Женщина"
                ),
                ft.Dropdown(
                    width=250,
                    options=[
                        ft.dropdown.Option('1', 'Удостоверение личности гражданина РК'),
                        ft.dropdown.Option('3', 'Свидетельство о рождении'),
                        ft.dropdown.Option('4', 'Вид на жительство иностранца'),
                        ft.dropdown.Option('7',
                                           'Свидетельство о государственной регистрации (перерегистрации) юридического лица'),
                        ft.dropdown.Option('8', 'Удостоверение лица без гражданства'),
                        ft.dropdown.Option('11', 'Паспорт гражданина РК'),
                        ft.dropdown.Option('12', 'Заграничный паспорт(иностранца)'),
                    ],
                    helper_text='Тип документа'
                ),
                    ft.Checkbox(label='Резидент', value=False)
            ] + [
                ft.ElevatedButton('Создать клиента', on_click=set_client_function, width=200, height=75),
            ]
        ),
        expand=True,
    )

    set_client_input_fields_ur = ft.Container(
        content=ft.Column(
            [
                switch,
                ft.TextField(helper_text='БИН', color='white', border_color='white', width=300),
                ft.ElevatedButton('Создать клиента', on_click=set_client_function, width=200, height=75),
            ]
        ),
        expand=True,
    )


    search_vehicles = ft.Column(
        [
            popup_menu,
            search_vehicles_input,
            search_vehicles_button,
            search_vehicles_result_field
        ]
    )

    def handle_change(e):
        page.add(ft.Text(f"Date changed: {e.control.value.strftime('%Y-%m-%d')}"))

    def handle_dismissal(e):
        page.add(ft.Text(f"DatePicker dismissed"))

    set_client = ft.Column(
        [
            popup_menu,
            set_client_input_fields_fiz,
            ft.ElevatedButton(
                "Pick date",
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=lambda e: page.open(
                    ft.DatePicker(
                        first_date=datetime.datetime(year=2023, month=10, day=1),
                        last_date=datetime.datetime(year=2024, month=10, day=1),
                        on_change=handle_change,
                        on_dismiss=handle_dismissal,
                    )
                ),
            )
        ]
    )

    page.add(set_client)


ft.app(main)
