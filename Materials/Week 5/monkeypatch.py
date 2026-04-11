from src.to_do_list import main, tasks

def test_main_choice_1_add_task(monkeypatch):
    """Test choice 1: Add a task"""
    tasks.clear()
    inputs = iter(["1", "Buy groceries", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main()
    assert "Buy groceries" in tasks

def test_main_choice_2_view_tasks(monkeypatch, capsys):
    """Test choice 2: View tasks"""
    tasks.clear()
    tasks.append("Task 1")
    tasks.append("Task 2")
    inputs = iter(["2", "4"])
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
    inputs = iter(["3", "2", "4"])  # remove task 2, view, quit
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main()
    assert "Task 2" not in tasks

def test_main_invalid_choice(monkeypatch, capsys):
      """Test that an invalid choice does not crash"""
      tasks.clear()
      inputs = iter(["9", "4"])
      monkeypatch.setattr('builtins.input', lambda _: next(inputs))
      main()
      captured = capsys.readouterr()
      assert "Invalid choice" in captured.out

      