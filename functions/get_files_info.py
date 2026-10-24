import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        is_valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        if not is_valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        result_string = ""
        directory_list = os.listdir(target_dir)

        for item in directory_list:
            item_path = os.path.join(target_dir, item)
            item_string = f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
            result_string = result_string + item_string

        result_string = f"Result for {directory} directory:\n" + result_string

        return result_string

    except Exception as e:
        return f"Error:{e}"
