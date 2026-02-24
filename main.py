from nicegui import ui


def apply_styles():
    ui.query('body').style('background: radial-gradient(circle at top right, #2e1065, #020617); min-height: 100vh;')
    ui.add_head_html('''
        <style>
            /* Стеклянная карточка с неоновой обводкой */
            .glass-card {
                background: rgba(255, 255, 255, 0.02) !important;
                backdrop-filter: blur(25px);
                border: 1px solid rgba(168, 85, 247, 0.4) !important;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
            }
            /* Фиолетовый неон для всех кнопок */
            .neon-btn {
                background: linear-gradient(45deg, #7c3aed, #db2777) !important;
                box-shadow: 0 0 20px rgba(139, 92, 246, 0.6) !important;
                border: none !important;
                color: white !important;
            }
            /* Подсветка активного таба */
            .q-tab--active {
                color: #d8b4fe !important;
                text-shadow: 0 0 10px rgba(168, 85, 247, 0.8);
            }
        </style>
    ''')


@ui.page('/')
def main():
    apply_styles()
    ui.dark_mode().enable()

    with ui.column().classes('w-full max-w-5xl mx-auto py-10 px-4 gap-8'):
        # --- ABOUT ME ---
        with ui.dialog() as about_dialog:
            with ui.card().classes('glass-card p-8 w-96 items-center text-center'):
                ui.avatar('person', color='purple-900', text_color='white', size='80px').classes(
                    'shadow-lg border-2 border-purple-500')
                ui.label('Junior QA Engineer').classes('text-2xl font-black mt-2 text-white')
                ui.label('Студент SkyPro | Январь 2025').classes('text-purple-300 text-sm italic mb-4')

                ui.label('Специализируюсь на Python и ручном тестировании. '
                         'Создаю инструменты для автоматизации документации.').classes('text-slate-300 text-sm mb-6')

                with ui.row().classes('gap-4'):
                    ui.button('GitHub', on_click=lambda: ui.navigate.to('https://github.com/Mumunich', new_tab=True)).props(
                        'flat color=purple-300')
                    ui.button('Telegram', on_click=lambda: ui.navigate.to('https://t.me/Mumunich', new_tab=True)).props(
                        'flat color=blue-300')
                    ui.button('HH.ru', on_click=lambda: ui.navigate.to('https://novosibirsk.hh.ru/resume/ac654e1aff0ff5b7c30039ed1f375154783151', new_tab=True)).props(
                        'flat color=red-300')

                ui.button('CLOSE', on_click=about_dialog.close).props('flat').classes('mt-6 text-slate-500')

        # --- HEADER ---
        with ui.row().classes('w-full items-center justify-between'):
            with ui.column():
                ui.label('QA Workstation').classes(
                    'text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-500 neon-text')
                ui.label('SYSTEMATIC QUALITY ASSURANCE').classes('text-blue-500/40 text-xs tracking-[0.5em] font-bold')
            ui.button(icon='account_circle', on_click=about_dialog.open).props('flat round color=purple-400').classes(
                'scale-150')

        # --- TABS ---
        with ui.tabs().classes('w-full bg-white/5 rounded-2xl p-1 border border-white/10 shadow-2xl') as tabs:
            t1 = ui.tab('BUG REPORT', icon='bug_report')
            t2 = ui.tab('TEST CASE', icon='assignment')
            t3 = ui.tab('CHECKLIST', icon='fact_check')
            t4 = ui.tab('DESIGN TECHNIQUES', icon='architecture')

        with ui.tab_panels(tabs, value=t1).classes('w-full bg-transparent mt-6'):

            # --- BUG REPORT ---
            with ui.tab_panel(t1):
                with ui.card().classes('glass-card p-8 gap-4'):
                    with ui.row().classes('w-full gap-4'):
                        b_title = ui.input('Summary (Что? Где? Когда?)').classes('flex-grow').props('standout dark')
                        b_status = ui.select(['NEW', 'ASSIGNED', 'OPEN', 'FIXED', 'RETEST', 'CLOSED', 'REOPENED'],
                                             value='NEW', label='Status').classes('w-32').props('standout dark')

                    with ui.row().classes('w-full gap-4'):
                        b_sev = ui.select({'S1': 'S1 Blocker', 'S2': 'S2 Critical', 'S3': 'S3 Major', 'S4': 'S4 Minor',
                                           'S5': 'S5 Trivial'}, value='S3', label='Severity').classes(
                            'flex-grow').props('standout dark')
                        b_pri = ui.select({'P1': 'P1 High', 'P2': 'P2 Medium', 'P3': 'P3 Low'}, value='P2',
                                          label='Priority').classes('w-32').props('standout dark')
                        b_env = ui.input('Environment').classes('flex-grow').props('standout dark')

                    # --- Секция динамических шагов ---
                    ui.label('Steps to Reproduce').classes('text-blue-300 font-bold mt-4')
                    bug_steps_data = []  # Список для хранения текста шагов

                    with ui.row().classes('w-full gap-2 items-end mb-2'):
                        step_in = ui.input(placeholder='Введите шаг и нажмите +').classes('flex-grow').props(
                            'standout dark')

                        def add_bug_step():
                            if not step_in.value: return
                            with bug_steps_cont:
                                # Показываем шаг пользователю
                                ui.label(f"{len(bug_steps_data) + 1}. {step_in.value}").classes(
                                    'text-xs text-slate-300 p-1')
                                bug_steps_data.append(step_in.value)
                            step_in.value = '';
                            step_in.focus()

                        ui.button(icon='add', on_click=add_bug_step).classes('neon-btn h-[56px] w-[56px] shadow-lg rounded-xl')

                    bug_steps_cont = ui.column().classes('w-full gap-1 mb-4 ml-2')  # Контейнер для отображения списка

                    with ui.row().classes('w-full gap-4 mt-4'):
                        b_exp = ui.input('Expected Result').classes('flex-grow').props('standout dark')
                        b_act = ui.input('Actual Result').classes('flex-grow').props('standout dark')

                    def copy_bug():
                        # Собираем шаги в нумерованный список Markdown
                        formatted_steps = "\n".join([f"{i + 1}. {s}" for i, s in enumerate(bug_steps_data)])

                        md = (
                            f"# 🐞 BUG: {b_title.value}\n\n"
                            f"**Status:** `{b_status.value}`  \n"
                            f"**Severity:** `{b_sev.value}`  \n"
                            f"**Priority:** `{b_pri.value}`  \n"
                            f"**Environment:** {b_env.value}\n\n"
                            f"### 📑 Steps to Reproduce\n"
                            f"{formatted_steps}\n\n"
                            f"**✅ Expected Result:**  \n{b_exp.value}\n\n"
                            f"**❌ Actual Result:**  \n{b_act.value}"
                        )
                        ui.run_javascript(f'navigator.clipboard.writeText({repr(md)})')
                        ui.notify('Баг-репорт скопирован!', type='positive')

                    ui.button('COPY MARKDOWN', on_click=copy_bug).classes('neon-btn px-10 py-3')

            # --- TEST CASE ---
            with ui.tab_panel(t2):
                with ui.card().classes('glass-card p-8'):
                    with ui.row().classes('w-full gap-4 mb-4'):
                        tc_title = ui.input('Test Case Title').classes('flex-grow').props('standout dark')
                        tc_pri = ui.select(['High', 'Medium', 'Low'], value='Medium', label='Priority').classes(
                            'w-32').props('standout dark')
                        tc_status = ui.select(['DRAFT', 'READY', 'PASS', 'FAIL', 'RE-TEST'], value='DRAFT',
                                              label='Status').classes('w-32').props('standout dark')

                    tc_pre = ui.input('Pre-conditions (Предусловия)').classes('w-full mb-4').props('standout dark')
                    tc_desc = ui.textarea('Description (Optional)').classes('w-full h-20 mb-4').props('standout dark')

                    tc_data = []
                    with ui.row().classes('w-full gap-2 items-end mb-4 mt-10'):
                        s_in = ui.input('Step').classes('flex-grow').props('standout dark')
                        e_in = ui.input('Step Expected Result').classes('flex-grow').props('standout dark')

                        def add_tc():
                            if not s_in.value: return
                            with tc_cont:
                                with ui.row().classes('w-full p-2 bg-white/5 rounded-lg'):
                                    ui.label(f"Step {len(tc_data) + 1}: {s_in.value}").classes('flex-grow text-xs')
                                    tc_data.append((s_in.value, e_in.value))
                            s_in.value = '';
                            e_in.value = '';
                            s_in.focus()

                        ui.button(icon='add', on_click=add_tc).classes('neon-btn h-14 w-14 rounded-xl')

                    tc_cont = ui.column().classes('w-full gap-1 mb-4')
                    tc_final_exp = ui.input('Final Expected Result (Общий результат)').classes('w-full mb-6').props(
                        'standout dark')

                    def copy_tc():
                        md = (
                                f"# 📋 TEST CASE: {tc_title.value}\n\n"
                                f"**Priority:** `{tc_pri.value}` | **Status:** `{tc_status.value}`\n\n"
                                f"### 🔗 Pre-conditions\n{tc_pre.value}\n\n"
                                f"### 📝 Description\n{tc_desc.value}\n\n"
                                f"### 🛠 Steps\n"
                                f"| # | Step | Step Expected |\n|---|---|---|\n" +
                                "\n".join([f"| {i + 1} | {s} | {e} |" for i, (s, e) in enumerate(tc_data)]) +
                                f"\n\n**🎯 Final Expected Result:**  \n{tc_final_exp.value}"
                        )
                        ui.run_javascript(f'navigator.clipboard.writeText({repr(md)})')
                        ui.notify('Тест-кейс скопирован!', type='positive')

                    ui.button('COPY FULL TEST CASE', on_click=copy_tc).classes('neon-btn w-full py-4')


            # --- CHECKLIST ---
            with ui.tab_panel(t3):
                with ui.card().classes('glass-card p-8'):
                    ui.label('Manual Checklist').classes('text-2xl font-bold mb-6 text-indigo-300')
                    tk_objs = []
                    with ui.row().classes('w-full gap-3 mb-6'):
                        tk_in = ui.input('Task description').classes('flex-grow').props('standout dark')

                        def add_tk():
                            if not tk_in.value: return
                            with tk_cont:
                                with ui.row().classes(
                                        'w-full justify-between items-center p-3 bg-white/5 rounded-xl group'):
                                    c = ui.checkbox(tk_in.value)
                                    tk_objs.append(c)
                                    ui.button(icon='delete', on_click=lambda e: (tk_objs.remove(c),
                                                                                 e.sender.parent_slot.parent.delete())).props(
                                        'flat color=grey').classes('opacity-0 group-hover:opacity-100')
                            tk_in.value = ''

                        ui.button(icon='add', on_click=add_tk).classes('neon-btn w-14 h-14 rounded-xl')
                    tk_cont = ui.column().classes('w-full gap-2 mb-6')
                    ui.button('COPY FULL CHECKLIST', on_click=lambda: ui.run_javascript(
                        f'navigator.clipboard.writeText({repr("### CHECKLIST\n" + "".join([f"- [{"x" if t.value else " "}] {t.text}\n" for t in tk_objs]))}')).classes(
                        'neon-btn w-full py-4')

            # --- DESIGN TECHNIQUES ---
            with ui.tab_panel(t4):
                with ui.row().classes('w-full gap-4 flex-wrap'):
                    techniques = [
                        ('Boundary Value Analysis',
                         'Проверка значений на границах: Min-1, Min, Min+1, Max-1, Max, Max+1.'),
                        ('Equivalence Partitioning',
                         'Разбиение данных на группы, где система ведет себя одинаково.'),
                        ('Decision Table', 'Таблица комбинаций условий для проверки сложной бизнес-логики.'),
                        ('State Transition',
                         'Тестирование переходов объекта из одного состояния в другое (напр. статус заказа).'),
                        ('Error Guessing',
                         'Поиск ошибок на основе опыта: пустые поля, спецсимволы, прерывание сети.')
                    ]
                    for name, desc in techniques:
                        with ui.card().classes('glass-card p-6 w-72 h-48'):
                            ui.label(name).classes('text-blue-400 font-bold text-lg mb-2')
                            ui.label(desc).classes('text-slate-300 text-xs leading-relaxed')


ui.run(title='QA Workstation Pro', port=8080, dark=True)