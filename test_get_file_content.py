from functions.get_file_content import get_file_content


def tests():
    test_file("calculator", "lorem.txt")
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


def test_file(working_directory: str, file_path: str):
    result = get_file_content(working_directory, file_path)
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")


if __name__ == "__main__":
    tests()
