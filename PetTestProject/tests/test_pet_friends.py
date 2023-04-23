from api import PetFriends
from settings import non_valid_email, non_valid_password
import os
from dotenv import load_dotenv

load_dotenv()
valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Пончик', animal_type='кошка',
                                     age='4', pet_photo='images/cat.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Черри', animal_type='кот', age=3):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
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


def test_successful_add_pet_photo(pet_photo='images/cat.jpg'):
    """Проверяем возможность добавления фото питомца для питомцев без фото"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового без фото и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_pet_simple(auth_key, "Мурка", "кошка", "6")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото питомца
    if len(my_pets['pets']) > 0:
        status, _ = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 200
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_new_pet_simple_with_valid_data(name='Моржик', animal_type='бульдог',
                                            age='3'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_get_api_key_for_non_valid_user_and_email(email=non_valid_email, password=non_valid_password):
    """ Проверяем что запрос api ключа с невалидными данными возвращает статус 403 и в тезультате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result

def test_add_new_pet_simple_with_non_valid_type_data(name='Моржик', animal_type='бульдог',
                                            age='dfdjfs'):
    """Проверяем что нельзя добавить питомца с некорректным типом данных для параметра age =str"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

def test_add_new_pet_simple_without_name(name='', animal_type='змейка',
                                            age='1'):
    """Проверяем что нельзя добавить питомца с пустым параметром name"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

def test_add_new_pet_simple_without_animal_type(name='Ася', animal_type='',
                                            age='4'):
    """Проверяем что нельзя добавить питомца с пустым параметром animal_type"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

def test_add_new_pet_simple_without_age(name='Тиша', animal_type='белка',
                                            age=''):
    """Проверяем что нельзя добавить питомца с пустым параметром age"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

def test_add_new_pet_simple_with_non_valid_api_key(name='Тиша', animal_type='белка',
                                            age='7'):
    """Проверяем что нельзя добавить питомца без фото с невалидным ключом"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(non_valid_email, non_valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

def test_add_new_pet_simple_with_name_255_symbols(name='KyELkoHO2GJ6R3faXvOCOoyL0GrCQlZgn5a3u3RxV9QcHexQ3ZOmTv3Z15Jukcn4FyrE6vGmIojFFArOs6dUJyNNzXEXZxY42x2eQh3E2bZkBis3HusddYGsqzGinEUpakqmdctGeJKMpR6UJH4ouhbONJ58VZN7adSFvM9DniuFtYv2g4YmbOWdEq6ZkK1HSsTS7rBozVYojwgtgdJ9gWc4XsGwHq4PQq1Q4EecKtCsuYPMeNZlIUBJnIxoW2O', animal_type='змейка',
                                            age='1'):
    """Проверяем что нельзя добавить питомца с невалидным именем"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

def test_add_new_pet_simple_with_anymal_type_255_symbols(name='Соня', animal_type='KyELkoHO2GJ6R3faXvOCOoyL0GrCQlZgn5a3u3RxV9QcHexQ3ZOmTv3Z15Jukcn4FyrE6vGmIojFFArOs6dUJyNNzXEXZxY42x2eQh3E2bZkBis3HusddYGsqzGinEUpakqmdctGeJKMpR6UJH4ouhbONJ58VZN7adSFvM9DniuFtYv2g4YmbOWdEq6ZkK1HSsTS7rBozVYojwgtgdJ9gWc4XsGwHq4PQq1Q4EecKtCsuYPMeNZlIUBJnIxoW2O',
                                            age='1'):
    """Проверяем что нельзя добавить питомца с невалидным типом животного"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

def test_add_new_pet_simple_with_non_valid_age(name='Генрих', animal_type='доберман',
                                            age='!2345'):
    """Проверяем что нельзя добавить питомца с невалидным возрастом"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400