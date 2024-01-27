# from app.api import PetFriends
from api import PetFriends
from settings import valid_email, valid_psw
import os
# инициализируем нашу библиотеку в переменную
pf = PetFriends()

# проверка получения авторизационного ключа
def test_get_api_key_for_valid_user(email=valid_email, password=valid_psw):
    status, result = pf.get_api_key(email, password)  # получили результат запроса
    # сверяем полученный рез-т с ожидаемым
    assert status == 200  # проверка статуса
    assert 'key' in result  # проверка, что ключ содержится в полученном ответе
# проверка получения списка петомцев
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_psw)  # статус нам не нужен - ставим прочерк. сохраняем аут.ключ
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200  # проверка статуса
    assert len(result['pets']) > 0  # питомцы передаются не сразу, а в ключе "pets", используем этот параметр
#проверка добавления питомца с корретными данными.
def test_add_new_pet_with_valid_data(name='MG', animal_type='Cat', age='10', pet_photo='image/MG_cat.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
#проверка возможности удаления питомца
def test_successful_delete_self_pet():
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "MG", "cat", "10", "image/MG_cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
#проверка обновления информации о питомце
def test_successful_update_self_pet_info(name='Мишель', animal_type='Кошка', age=11):
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#####################################################################################################################
#1 - проверка добавления питомца (без фото)
def test_add_new_pet_no_photo(name='Котик', animal_type='котик', age='1'):
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    # Добавляем питомца
    status, result = pf.create_new_pet_simple(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] == ''
#2 - проверка добавления/изменения фото
def test_add_pet_new_photo(pet_photo='images/MG_cat_fooler.jpeg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Добавляем(если без фото)/изменяем фото питомца
    status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] != ''
#3 - проверка получения ключа с неверным эл.адресом (негативный тест)
def test_get_api_key_with_invalid_email(email='123456mail.ru', password=valid_psw):
        status, result = pf.get_api_key(email, password)
        assert status == 403
#4 - проверка получения ключа с неверным паролем (негативный тест)
def test_get_api_key_with_invalid_password(email=valid_email, password='123'):
    status, result = pf.get_api_key(email, password)
    assert status == 403
#5 - проверка добавления питомца с некорретным именем (негативный тест)
def test_add_new_pet_with_invalid_name(name=12345, animal_type='Мышь', age='1500', pet_photo='images/mouse.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    # Добавляем питомца c обработкой исключения
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except AttributeError:
        print('Неверное имя')
#6 - проверка добавления питомца без имени (негативный тест).
def test_add_new_pet_without_name(name='', animal_type='Дракон', age='10000', pet_photo='images/drako.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except AttributeError:
        print('Неверное имя')
    else:
        assert status == 200
        print("Баг - питомец добавлен без имени")
#7 - проверка невозможности удаления питомца с пустым ID  (негативный тест)
def test_try_unsuccessful_delete_empty_pet_id():
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    pet_id = ''
    status, _ = pf.delete_pet(auth_key, pet_id)
    assert status == 400 or 404
    print('удалить питомца без id нельзя')
#8 - проверка невозможности добавления фото некорректного формата (негативный тест)
def test_add_new_pet_with_invalid_animal_type(name='Дракончик', animal_type=12345, age='1000', pet_photo='images/drako.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except AttributeError:
        print('Неверный вид питомца')
#9 - проверка невозможности добавление питомца с пустым полем вида (негативный кейс)
def test_add_new_pet_with_none_value_animal_type(name='Дракончик', animal_type='', age='10000', pet_photo='images/drako.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except AttributeError:
        print('не указан вид питомца')
    else:
        assert status == 200
        print("Баг - питомец добавлен без вида")
#10 - проверка невозможности добавления питомца с неверным значением возраста (негативный кейс)
def test_add_new_pet_with_invalid_age(name='Дракончик', animal_type='Дракон', age='тысяча', pet_photo='images/drako.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_psw)
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except AttributeError:
        print('неверно указан возраст питомца')
    else:
        assert status == 200
        print("Баг - питомец добавлен с некоректным возрастом")

