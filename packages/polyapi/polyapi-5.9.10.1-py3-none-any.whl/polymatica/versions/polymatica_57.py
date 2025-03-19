#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Реализация методов бизнес-сценариев Полиматики версии 5.7 """
import json
import time
import requests
from urllib.parse import urljoin
from ..executor import Executor
from ..exceptions import *
from ..common import raise_exception, MULTISPHERE_ID, json_type, business_logic


class Polymatica57:
    API_VERSION = 'v2'
    ROOT_PARENT = "00000000"

    """ Реализация методов, заточенная под Полиматику версии 5.7 """

    def __init__(self, base_bs: business_logic):
        self.base_bs = base_bs
        self._raise_exception = raise_exception(self.base_bs)

    def create_multisphere_from_cube(self, **kwargs):
        """
        Создать мультисферу из куба.
        """
        result = self.base_bs.execute_manager_command(
            command_name="user_iface",
            state="create_module",
            layer_id=self.base_bs.active_layer_id,
            cube_id=self.base_bs.cube_id,
            module_id=kwargs.get('module_id'),
            after_module_id=kwargs.get('after_module_id'),
            module_type=kwargs.get('module_type')
        )
        return result

    def get_scripts_description_list(self) -> json_type:
        """
        Получить описание всех сценариев.
        :return: (json) информация по каждому сценарию в формате JSON (список словарей).
        """

        def _rec_get_scripts_in_dir(curr_path: str = None, parent_id: str = self.ROOT_PARENT) -> list:
            results = self.base_bs.exec_request.execute_request(
                params=urljoin(self.base_bs.base_url, f"api/{self.API_VERSION}/script_folders?parent={parent_id}"),
                method='GET')
            folders: list = results.json()['results']

            results = self.base_bs.exec_request.execute_request(
                params=urljoin(self.base_bs.base_url, f"api/{self.API_VERSION}/scripts?parent={parent_id}"),
                method='GET')
            scripts: list = results.json()['results']
            for script in scripts:
                script['path'] = curr_path

            for folder in folders:
                folder_id, folder_name = folder['id'], folder['name']
                scripts += _rec_get_scripts_in_dir(curr_path=f'{curr_path}/{folder_name}' if curr_path else folder_name,
                                                   parent_id=folder_id)

            return scripts

        scripts = _rec_get_scripts_in_dir()

        return scripts

    def get_scenario_cube_ids(self, **kwargs) -> set:
        """
        Возвращает идентификаторы всех мультисфер, входящих в заданный сценарий.
        """
        result = self.base_bs.execute_manager_command(
            command_name="scripts", state="get_script_description", script_id=kwargs.get('scenario_id'))
        script_info = self.base_bs.h.parse_result(result, 'script')
        used_cubes = script_info.get('used_cubes', [])
        return {cube.get('id') for cube in used_cubes}

    def _wait_scenario_loaded(self, layer_id: str):
        """
        Дождаться полной загрузки сценария на слое.
        """

        def _raise(message, with_traceback=False):
            """
            Генерация исключения ScenarioError с заданным сообщением.
            """
            return self._raise_exception(ScenarioError, message, with_traceback=with_traceback)

        status_codes = {'Loaded': 1, 'Running': 2, 'Finished': 3, 'Paused': 4, 'Interrupted': 5, 'Failure': 6}
        need_check_progress = True
        while need_check_progress:
            # периодичностью раз в полсекунды запрашиваем результат с сервера и проверяем статус загрузки слоя
            # если не удаётся получить статус - скорее всего нет ответа от сервера - сгенерируем ошибку
            # в таком случае считаем, что сервер не ответил и генерируем ошибку
            time.sleep(0.5)
            try:
                progress = self.base_bs.execute_manager_command(
                    command_name="scripts", state="get_script_status", runtime_id=layer_id)
                status = self.base_bs.h.parse_result(result=progress, key="script_status") or {}
                status_code = status.get('status', -1)
            except Exception as ex:
                # если упала ошибка - не удалось получить ответ от сервера: возможно, он недоступен
                return _raise('Failed to load script! Possible server is unavailable.', True)

            # проверяем код статуса
            if status_code in [status_codes.get('Loaded'), status_codes.get('Running')]:
                # сценарий в процессе воспроизведения
                need_check_progress = True
            elif status_code == status_codes.get('Finished'):
                # сценарий полностью выполнен
                need_check_progress = False
            elif status_code in [status_codes.get('Interrupted'), status_codes.get('Paused')]:
                # ошибка: сценарий прерван либо был поставлен на паузу
                return _raise('Script loading was interrupted!')
            elif status_code == status_codes.get('Failure'):
                # ошибка выполнения
                err_details = status.get('error', 'Unknown error!')
                return _raise('Script loading was failured! Details: {}'.format(err_details))
            elif status_code == -1:
                # ошибка: не удалось получить код текущего статуса
                return _raise('Unable to get status code!')
            else:
                # прочие ошибки
                return _raise('Unknown error!')

    def run_scenario_impl(self, **kwargs):
        """
        Запуск сценария.
        """
        scenario_id, scenario_name = kwargs.get('scenario_id'), kwargs.get('scenario_name')

        # Получаем идентификаторы существующих слоёв
        exists_layers = self.base_bs._get_session_layers()
        exists_layer_ids = [layer.get('uuid') for layer in exists_layers]

        # Создаём новый слой, на котором будет запущен наш сценарий, и добавляем его в список существующих слоёв
        new_layer_data = self.base_bs.execute_manager_command(command_name="user_layer", state="create_layer")
        layer_uuid = (self.base_bs.h.parse_result(new_layer_data, 'layer') or dict()).get("uuid")
        if not layer_uuid:
            return self._raise_exception(ScenarioError, 'New layer has been no created!')
        exists_layer_ids.append(layer_uuid)

        # Переименовываем слой - он будет называться также, как запускаемый сценарий
        self.base_bs.execute_manager_command(
            command_name="user_layer", state="rename_layer", layer_id=layer_uuid, name=scenario_name)

        # Запуск сценария на слое
        self.run_scenario_on_layer_impl(layer_id=layer_uuid, scenario_id=scenario_id)

        # Сделать слой активным
        self.base_bs.execute_manager_command(command_name="user_layer", state="set_active_layer", layer_id=layer_uuid)

        # Инициализация слоя, содержащего сценарий
        self.base_bs.execute_manager_command(command_name="user_layer", state="init_layer", layer_id=layer_uuid)

        # Сохранение интерфейсных настроек
        settings = {"wm_layers2": {"lids": exists_layer_ids, "active": layer_uuid}}
        self.base_bs.execute_manager_command(
            command_name="user_iface",
            state="save_settings",
            module_id=self.base_bs.authorization_uuid,
            settings=settings
        )

        # Сохранение переменных окружения
        self.base_bs.layers_list = exists_layer_ids
        self.base_bs.active_layer_id = layer_uuid
        layer_settings = self.base_bs.execute_manager_command(
            command_name="user_layer", state="get_layer", layer_id=layer_uuid)
        module_descs = self.base_bs.h.parse_result(
            result=layer_settings, key="layer", nested_key="module_descs") or list()
        if not module_descs:
            self.base_bs.set_multisphere_module_id(str())
            self.base_bs.cube_id = str()
        else:
            for module in module_descs:
                # берём первую по счёту мультисферу
                if module.get('type_id') == MULTISPHERE_ID:
                    self.base_bs.set_multisphere_module_id(module.get('uuid', str()))
                    self.base_bs.cube_id = module.get('cube_id', str())
                    break

        # Обновление числа строк активной мультисферы
        if self.base_bs.multisphere_module_id:
            self.base_bs.update_total_row()
        self.base_bs.func_name = 'run_scenario'

    def run_scenario_on_layer_impl(self, **kwargs):
        """
        Запуск сценария на заданном слое
        """

        scenario_id, layer_id = kwargs.get('scenario_id'), kwargs.get('layer_id')

        # Получаем информацию о запускаемом сценарии
        script_data = self.base_bs.execute_manager_command(
            command_name="scripts", state="get_script_description", script_id=scenario_id)
        script_info = self.base_bs.h.parse_result(script_data, 'script')

        self.base_bs.execute_manager_command(
            command_name="scripts",
            state="load_on_layer",
            script_id=scenario_id,
            runtime_id=layer_id,
            on_load_action=0
        )
        self.base_bs.execute_manager_command(
            command_name="scripts",
            state="play_to_position",
            script_id=scenario_id,
            runtime_id=layer_id,
            play_to_position=script_info.get('steps_count') - 1,
            clear_workspace=True
        )

        self._wait_scenario_loaded(layer_id)

        # сохраняем текущий слой как активный
        self.base_bs.active_layer_id = layer_id

        self.base_bs.func_name = 'run_scenario_on_layer'
