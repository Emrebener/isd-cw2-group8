from src.to_do_list import main, tasks

CHOICE_ADD = "1"
CHOICE_VIEW = "2"
CHOICE_REMOVE = "3"
CHOICE_QUIT = "4"

def test_main_choice_1_add_task(monkeypatch):
    """Test choice 1: Add a task"""
    tasks.clear()
    inputs = iter([CHOICE_ADD, "Buy groceries", CHOICE_QUIT])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main()
    assert "Buy groceries" in tasks

def test_main_choice_2_view_tasks(monkeypatch, capsys):
    """Test choice 2: View tasks"""
    tasks.clear()
    tasks.append("Task 1")
    tasks.append("Task 2")
    inputs = iter([CHOICE_VIEW, CHOICE_QUIT])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main()
    captured = capsys.readouterr()
    assert "Task 1" in captured.out
    assert "Task 2" in captured.out
    assert "Total tasks: 2" in captured.out

def test_main_choice_3_remove_tasks(monkeypatch, capsys):
    """Test choice 3: Remove tasks"""
    tasks.clear()
    tasks.append("Task 1")
    tasks.append("Task 2")
    inputs = iter([CHOICE_REMOVE, "2", CHOICE_QUIT])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main()
    assert "Task 2" not in tasks