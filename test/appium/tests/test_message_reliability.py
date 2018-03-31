# import matplotlib
# import matplotlib.pyplot as plt
import random
import string
import time

from itertools import cycle
from timeit import timeit
from selenium.common.exceptions import TimeoutException

from tests import info, marks
from tests.base_test_case import MultipleDeviceTestCase
from views.sign_in_view import SignInView


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped


def create_chart(user_1: dict, user_2: dict):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 7))
    time_1 = sorted(user_1['message_time'])
    ax.plot([i / 60 for i in time_1], [user_1['message_time'][i] for i in time_1],
            'o-', color='#0c0fea', label=user_1['name'])
    time_2 = sorted(user_2['message_time'])
    ax.plot([i / 60 for i in time_2], [user_2['message_time'][i] for i in time_2],
            'o-', color='#f61e06', label=user_2['name'])
    sent_messages = user_1['sent_messages'] + user_2['sent_messages']
    title = "User A: sent messages: {}, received messages: {}" \
            "\nUser B: sent messages: {}, received messages: {}".format(user_1['sent_messages'],
                                                                        len(user_1['message_time']),
                                                                        user_2['sent_messages'],
                                                                        len(user_2['message_time']))
    if sent_messages:
        title += "\nReceived messages: {}%".format(
            round((len(user_1['message_time']) + len(user_2['message_time'])) / sent_messages * 100, ndigits=2))
    plt.title(title)
    plt.xlabel('chat session duration, minutes')
    plt.ylabel('time to receive a message, seconds')
    plt.legend()
    fig.savefig('chart.png')


def create_chart_public_chat(sent_messages: int, received_messages: int, message_timing: dict):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 7))
    sorted_time = sorted(message_timing)
    ax.plot([i / 60 for i in sorted_time], [message_timing[i] for i in sorted_time], 'o-', color='#0c0fea')
    title = "Sent messages: {}\nReceived messages: {}".format(sent_messages, received_messages)
    plt.title(title)
    plt.xlabel('chat session duration, minutes')
    plt.ylabel('time to receive a message, seconds')
    plt.legend()
    fig.savefig('chart.png')


@marks.message_reliability
class TestMessageReliability(MultipleDeviceTestCase):

    def test_message_reliability_1_1_chat(self, messages_number, message_wait_time):
        user_a_sent_messages = 0
        user_a_received_messages = 0
        user_b_sent_messages = 0
        user_b_received_messages = 0
        user_a_message_timing = dict()
        user_b_message_timing = dict()
        try:
            self.create_drivers(2, max_duration=10800, custom_implicitly_wait=2)
            device_1, device_2 = SignInView(self.drivers[0]), SignInView(self.drivers[1])
            device_1.create_user(username='user_a')
            device_2.create_user(username='user_b')
            device_1_home, device_2_home = device_1.get_home_view(), device_2.get_home_view()
            device_2_public_key = device_2_home.get_public_key()
            device_2_home.home_button.click()
            device_1_home.add_contact(device_2_public_key)
            device_1_chat = device_1_home.get_chat_view()
            device_2_chat = device_2_home.get_chat_with_user('user_a').click()
            device_2_chat.add_to_contacts.click()
            device_2_chat.chat_message_input.send_keys('hello')
            device_2_chat.send_message_button.click()
            device_1_chat.wait_for_element_starts_with_text('hello', wait_time=message_wait_time)

            start_time = time.time()
            for i in range(int(messages_number / 2)):
                message_1 = ''.join(random.sample(string.ascii_lowercase, k=10))
                device_1_chat.chat_message_input.send_keys(message_1)
                device_1_chat.send_message_button.click()
                user_a_sent_messages += 1
                try:
                    user_b_receive_time = timeit(wrapper(device_2_chat.wait_for_element_starts_with_text,
                                                         message_1, message_wait_time),
                                                 number=1)
                    duration_time = round(time.time() - start_time, ndigits=2)
                    user_b_message_timing[duration_time] = user_b_receive_time
                    user_b_received_messages += 1
                except TimeoutException:
                    info("Message with text '%s' was not received by user_b" % message_1)
                message_2 = ''.join(random.sample(string.ascii_lowercase, k=10))
                device_2_chat.chat_message_input.send_keys(message_2)
                device_2_chat.send_message_button.click()
                user_b_sent_messages += 1
                try:
                    user_a_receive_time = timeit(wrapper(device_1_chat.wait_for_element_starts_with_text,
                                                         message_2, message_wait_time),
                                                 number=1)
                    duration_time = round(time.time() - start_time, ndigits=2)
                    user_a_message_timing[duration_time] = user_a_receive_time
                    user_a_received_messages += 1
                except TimeoutException:
                    info("Message with text '%s' was not received by user_a" % message_2)
        finally:
            create_chart(
                user_1={'name': 'user_a', 'message_time': user_a_message_timing, 'sent_messages': user_a_sent_messages},
                user_2={'name': 'user_b', 'message_time': user_b_message_timing, 'sent_messages': user_b_sent_messages})

    def test_message_reliability_public_chat(self, messages_number, message_wait_time, participants_number):
        sent_messages = int()
        received_messages = int()
        message_timing = dict()
        try:
            self.create_drivers(participants_number, max_duration=10800, custom_implicitly_wait=2)
            users = list()
            chat_views = list()
            chat_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(7))
            for i in range(participants_number):
                device = SignInView(self.drivers[i])
                users.append(device.create_user())
                home_view = device.get_home_view()
                home_view.join_public_chat(chat_name)
                chat_views.append(home_view.get_chat_view())

            start_time = time.time()
            repeat = cycle(range(participants_number))
            for i in repeat:
                message_text = ''.join(random.sample(string.ascii_lowercase, k=10))
                chat_views[i].chat_message_input.send_keys(message_text)
                chat_views[i].send_message_button.click()
                sent_messages += 1
                try:
                    user_b_receive_time = timeit(wrapper(chat_views[next(repeat)].wait_for_element_starts_with_text,
                                                         message_text, message_wait_time),
                                                 number=1)
                    duration_time = round(time.time() - start_time, ndigits=2)
                    message_timing[duration_time] = user_b_receive_time
                    received_messages += 1
                except TimeoutException:
                    pass
                if sent_messages == messages_number:
                    break
        finally:
            create_chart_public_chat(sent_messages, received_messages, message_timing)

    def test_message_reliability_offline_public_chat(self, messages_number, message_wait_time):
        sent_messages_number = int()
        received_messages = int()
        message_timing = dict()
        try:
            self.create_drivers(1, max_duration=10800, custom_implicitly_wait=2, offline_mode=True)
            driver = self.drivers[0]
            sign_in_view = SignInView(driver)
            sign_in_view.create_user()
            home_view = sign_in_view.get_home_view()
            chat_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(7))
            home_view.join_public_chat(chat_name)

            start_time = time.time()
            iterations = int(messages_number / 10 if messages_number > 10 else messages_number)
            for _ in range(iterations):
                home_view.get_back_to_home_view()
                driver.set_network_connection(1)  # airplane mode

                sent_messages_texts = self.network_api.start_chat_bot(chat_name=chat_name, messages_number=10)
                sent_messages_number += 10

                driver.set_network_connection(2)  # turning on WiFi connection

                home_view.get_chat_with_user('#' + chat_name).click()
                chat_view = home_view.get_chat_view()
                for message in sent_messages_texts:
                    try:
                        user_b_receive_time = timeit(wrapper(chat_view.wait_for_element_starts_with_text,
                                                             message, message_wait_time),
                                                     number=1)
                        duration_time = round(time.time() - start_time, ndigits=2)
                        message_timing[duration_time] = user_b_receive_time
                        received_messages += 1
                    except TimeoutException:
                        pass
        finally:
            create_chart_public_chat(sent_messages_number, received_messages, message_timing)
