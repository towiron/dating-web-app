from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        db_table = 'chat_messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ('-date',)

        
    # функция получает все сообщения между "двумя" пользователями (требуется ваш pk и pk другого пользователя)
    def get_all_messages(id_1, id_2):
        messages = []
        # получить сообщения между двумя пользователями, отсортировывает их по дате (обратной) и добавляет их в список
        message1 = Message.objects.filter(sender_id=id_1, recipient_id=id_2).order_by('-date') # получать сообщения от отправителя к получателю
        for x in range(len(message1)):
            messages.append(message1[x])
			
		# получать сообщения от получателя к отправителю
        message2 = Message.objects.filter(sender_id=id_2, recipient_id=id_1).order_by('-date')
        for x in range(len(message2)):
            messages.append(message2[x])

        # поскольку функция вызывается при просмотре чата, мы вернем все сообщения как прочитанные
        for x in range(len(messages)):
            messages[x].is_read = True
        # sort the messages by date
        messages.sort(key=lambda x: x.date, reverse=False)
        return messages

    # функция получает все сообщения между "любыми" двумя пользователями (требуется ваш pk)
    def get_message_list(u):
        # получать все сообщения
        m = []  # сохраняет все сообщения, отсортированные по принципу "последнее - первое"
        j = []  # сохраняет все имена пользователей из сообщений выше после удаления дубликатов
        k = []  # сохраняет последнее сообщение из отсортированных выше имен пользователей
        for message in Message.objects.all():
            for_you = message.recipient == u  # сообщения, полученные пользователем
            from_you = message.sender == u  # сообщения, отправленные пользователем
            if for_you or from_you:
                m.append(message)
                m.sort(key=lambda x: x.sender.username)  # сортировать сообщения по отправителям
                m.sort(key=lambda x: x.date, reverse=True)  # сортировать сообщения по дате

        """ удалить дубликаты имен пользователей и получить одно сообщение (последнее сообщение)
		на имя пользователя (другого пользователя) (между вами и другим пользователем)"""
        for i in m:
            if i.sender.username not in j or i.recipient.username not in j:
                j.append(i.sender.username)
                j.append(i.recipient.username)
                k.append(i)

        return k