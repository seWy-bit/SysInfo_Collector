import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))

from gui.main_window import MainWindow

def main():
    try:
        print("Запуск SysInfo Collector...")
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"Ошибка запуска: {e}")
        return 1
    
    print("Работа приложения завершена")
    return 0

if __name__ == "__main__":
    sys.exit(main())