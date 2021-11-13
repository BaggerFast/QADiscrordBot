from channels import Base


class Test(Base):

    async def run(self):
        if self.message.content.startswith('!test'):
            result_string = ''
            await self.message.delete()
            if self.message.content.find('result____') != -1:
                await self.message.channel.send('В вашем коде обнаружена переменная с именем "result____".'
                                                ' Переименуйте её для проверки')
                return

            if self.message.content.find('func(') != -1:
                await self.message.channel.send('В вашем коде обнаружена функция или метод "func". Исправь пж')
            text = self.message.content.split('\n')
            task_name = self.get_task_name(text[0], '!test')
            code = text[1:]
            task = self.bot.db.get_task_by_name(task_name)
            if code:
                await self.message.channel.send("Тестирую. Попей чаю 🍵")
                code = self.bot.transform_code(code, task)
                for i in range(len(code)):
                    if self.bot.run_code(code[i], task.tests[i].output):
                        result_string += f'✅ Тест {i} - успешно\n'
                    else:
                        result_string += f'❌ Тест {i} - неверный ответ\n'

                await self.message.channel.send(f'```\n{result_string}```')
